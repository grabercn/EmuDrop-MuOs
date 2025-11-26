#!/bin/bash
# HELP: EmuDrop ROM downloader for muOS
# ICON: emudrop

# Source muOS helper functions
. /opt/muos/script/var/func.sh

echo app >/tmp/act_go

ROOT_DIR="$(GET_VAR "device" "storage/rom/mount")"
APP_DIR="${ROOT_DIR}/MUOS/application/EmuDrop"
LOG_DIR="${APP_DIR}/logs"
export LOG_FILE="${LOG_DIR}/$(date +'%Y-%m-%d').log"
ICON_DIR="/opt/muos/default/MUOS/theme/active/glyph/muxapp"
FONTS_DIR="/usr/share/fonts/emudrop"
SDL_FBDEV=${SDL_FBDEV:-/dev/fb0}
export SDL_FBDEV

mkdir -p "${LOG_DIR}"
exec >"${LOG_DIR}/launch.log" 2>&1

# Keep the launcher icon visible in the system theme
mkdir -p "${ICON_DIR}"
cp "${APP_DIR}/icon.png" "${ICON_DIR}/emudrop.png"

# Ensure the font we ship is available system-wide for SDL2/Pillow
mkdir -p "${FONTS_DIR}"
cp "${APP_DIR}/assets/fonts/arial.ttf" "${FONTS_DIR}/arial.ttf"

cd "${APP_DIR}" || exit 1

# Resolve Python path early for bootstrap/download steps
PYTHON_BIN="$(command -v python3 || command -v /opt/muos/python/bin/python3 || true)"
if [ -z "${PYTHON_BIN}" ]; then
    echo "python3 not found on device" | tee -a "${LOG_FILE}"
    exit 1
fi

# Load controller mappings from muOS if available
if [ -f "${ROOT_DIR}/MUOS/PortMaster/muos/control.txt" ]; then
    # shellcheck disable=SC1090
    source "${ROOT_DIR}/MUOS/PortMaster/muos/control.txt" || true
    get_controls || true
fi

echo "Starting Python application..." >> "${LOG_FILE}"

# Runtime environment
export PYTHONPATH="${APP_DIR}/deps:${PYTHONPATH:-}"
export SDL_GAMECONTROLLERCONFIG_FILE="/usr/lib/gamecontrollerdb.txt"
SDL2_DLL_DIR="${APP_DIR}/deps/sdl2dll/dll"
ALT_SDL2_DLL_DIR="${APP_DIR}/deps/pysdl2_dll"
PILLOW_LIB_DIR="${APP_DIR}/libs/pillow.libs"

LD_PATHS="${APP_DIR}/libs"
if [ -d "${PILLOW_LIB_DIR}" ]; then
    LD_PATHS="${PILLOW_LIB_DIR}:${LD_PATHS}"
fi
if [ -d "${SDL2_DLL_DIR}" ]; then
    export PYSDL2_DLL_PATH="${SDL2_DLL_DIR}"
    LD_PATHS="${SDL2_DLL_DIR}:${LD_PATHS}"
elif [ -d "${ALT_SDL2_DLL_DIR}" ]; then
    export PYSDL2_DLL_PATH="${ALT_SDL2_DLL_DIR}"
    LD_PATHS="${ALT_SDL2_DLL_DIR}:${LD_PATHS}"
else
    unset PYSDL2_DLL_PATH
fi
export LD_LIBRARY_PATH="${LD_PATHS}:${LD_LIBRARY_PATH:-}"
export SDL_AUDIODRIVER=alsa
export HOME="${APP_DIR}"
# Ensure SDL has a runtime dir for DRM devices (muOS may not set this)
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}"
mkdir -p "${XDG_RUNTIME_DIR}"

# App-specific paths
export ROMS_DIR="${ROOT_DIR}/ROMS/"
export IMGS_DIR="${ROOT_DIR}/ROMS/{SYSTEM}/images/{IMAGE_NAME}-image.png"
export EXECUTABLES_DIR="${APP_DIR}/assets/executables/"
export MUOS_CATALOG_DIR="${ROOT_DIR}/MUOS/info/catalogue"

# Debug info
echo "--- Debug Info ---" >> "${LOG_FILE}"
echo "Date: $(date)" >> "${LOG_FILE}"
echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}" >> "${LOG_FILE}"
echo "PYTHONPATH: ${PYTHONPATH}" >> "${LOG_FILE}"
echo "Listing libs:" >> "${LOG_FILE}"
ls -lh "${APP_DIR}/libs" >> "${LOG_FILE}" 2>&1 || echo "No libs dir" >> "${LOG_FILE}"
echo "Listing deps:" >> "${LOG_FILE}"
ls -lh "${APP_DIR}/deps" >> "${LOG_FILE}" 2>&1 || echo "No deps dir" >> "${LOG_FILE}"
echo "------------------" >> "${LOG_FILE}"

# Discover available SDL video drivers on the device
AVAILABLE_DRIVERS="$(
    SDL_VIDEODRIVER="" "${PYTHON_BIN}" - <<'PY' 2>/dev/null
import sdl2
drivers = [sdl2.SDL_GetVideoDriver(i).decode("utf-8") for i in range(sdl2.SDL_GetNumVideoDrivers())]
print(",".join(drivers))
PY
)"
echo "Available SDL drivers: ${AVAILABLE_DRIVERS}" >> "${LOG_FILE}"

# Pick an SDL video driver with runtime detection.
# RG35XX-SP (H700 + Mali) exposes only the "mali" SDL driver, so try that first,
# then kmsdrm on multiple cards, then fbcon, finally dummy.
VIDEO_DRIVER_CANDIDATES=("mali" "${SDL_VIDEODRIVER:-kmsdrm}:0" "${SDL_VIDEODRIVER:-kmsdrm}:1" "fbcon" "dummy")
VIDEO_DRIVER_SELECTED=""
SDL_KMS_INDEX_SELECTED=""
for drv_entry in "${VIDEO_DRIVER_CANDIDATES[@]}"; do
    IFS=":" read -r drv kms_index <<<"${drv_entry}"
    if [ "${drv}" = "kmsdrm" ]; then
        export SDL_KMSDRM_DEVICE_INDEX="${kms_index}"
    else
        unset SDL_KMSDRM_DEVICE_INDEX
    fi
    echo "Testing SDL_VIDEODRIVER=${drv} KMS_INDEX=${SDL_KMSDRM_DEVICE_INDEX:-none}" >> "${LOG_FILE}"
    if SDL_VIDEODRIVER="${drv}" "${PYTHON_BIN}" - <<'PY' >>"${LOG_FILE}" 2>&1; then
import sys, os
import sdl2
drv = os.environ.get("SDL_VIDEODRIVER")
if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
    err = sdl2.SDL_GetError().decode("utf-8")
    sys.stderr.write(f"SDL init failed for {drv}: {err}\n")
    sys.exit(1)
sdl2.SDL_Quit()
PY
        VIDEO_DRIVER_SELECTED="${drv}"
        if [ "${drv}" = "kmsdrm" ]; then
            SDL_KMS_INDEX_SELECTED="${kms_index}"
        fi
        break
    fi
done

if [ -z "${VIDEO_DRIVER_SELECTED}" ]; then
    echo "No usable SDL video driver found (tried ${VIDEO_DRIVER_CANDIDATES[*]})" | tee -a "${LOG_FILE}"
    exit 1
fi

export SDL_VIDEODRIVER="${VIDEO_DRIVER_SELECTED}"
if [ "${VIDEO_DRIVER_SELECTED}" = "kmsdrm" ] && [ -n "${SDL_KMS_INDEX_SELECTED}" ]; then
    export SDL_KMSDRM_DEVICE_INDEX="${SDL_KMS_INDEX_SELECTED}"
fi
echo "Selected SDL_VIDEODRIVER=${SDL_VIDEODRIVER}" >> "${LOG_FILE}"

# Ensure executables are runnable
chmod -R 755 "${APP_DIR}/assets/executables" || true

"${PYTHON_BIN}" -u main.py >"${LOG_FILE}" 2>&1

# Restore framebuffer in case SDL leaves it in an unexpected state
SCREEN_TYPE="internal"
DEVICE_MODE="$(GET_VAR "global" "boot/device_mode")"
if [[ ${DEVICE_MODE} -eq 1 ]]; then
    SCREEN_TYPE="external"
fi

DEVICE_WIDTH="$(GET_VAR "device" "screen/${SCREEN_TYPE}/width")"
DEVICE_HEIGHT="$(GET_VAR "device" "screen/${SCREEN_TYPE}/height")"
FB_SWITCH "${DEVICE_WIDTH}" "${DEVICE_HEIGHT}" 32
