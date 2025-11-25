#!/bin/bash
# HELP: EmuDrop ROM downloader for muOS
# ICON: emudrop

set -euo pipefail

# Source muOS helper functions
. /opt/muos/script/var/func.sh

echo app >/tmp/act_go

ROOT_DIR="$(GET_VAR "device" "storage/rom/mount")"
APP_DIR="${ROOT_DIR}/MUOS/application/EmuDrop"
LOG_DIR="${APP_DIR}/logs"
ICON_DIR="/opt/muos/default/MUOS/theme/active/glyph/muxapp"
FONTS_DIR="/usr/share/fonts/emudrop"

mkdir -p "${LOG_DIR}"
exec >"${LOG_DIR}/launch.log" 2>&1

# Keep the launcher icon visible in the system theme
mkdir -p "${ICON_DIR}"
cp "${APP_DIR}/icon.png" "${ICON_DIR}/emudrop.png"

# Ensure the font we ship is available system-wide for SDL2/Pillow
mkdir -p "${FONTS_DIR}"
cp "${APP_DIR}/assets/fonts/arial.ttf" "${FONTS_DIR}/arial.ttf"

cd "${APP_DIR}" || exit 1

# Load controller mappings from muOS if available
if [ -f "${ROOT_DIR}/MUOS/PortMaster/muos/control.txt" ]; then
    # shellcheck disable=SC1090
    source "${ROOT_DIR}/MUOS/PortMaster/muos/control.txt"
    get_controls
fi

# Runtime environment
export LOG_FILE="${LOG_DIR}/$(date +'%Y-%m-%d').log"
export PYTHONPATH="${APP_DIR}/deps:${PYTHONPATH:-}"
SDL2_DLL_DIR="${APP_DIR}/deps/sdl2dll/dll"
ALT_SDL2_DLL_DIR="${APP_DIR}/deps/pysdl2_dll"

if [ -d "${SDL2_DLL_DIR}" ]; then
    export PYSDL2_DLL_PATH="${SDL2_DLL_DIR}"
    export LD_LIBRARY_PATH="${SDL2_DLL_DIR}:${APP_DIR}/libs:${LD_LIBRARY_PATH:-}"
elif [ -d "${ALT_SDL2_DLL_DIR}" ]; then
    export PYSDL2_DLL_PATH="${ALT_SDL2_DLL_DIR}"
    export LD_LIBRARY_PATH="${ALT_SDL2_DLL_DIR}:${APP_DIR}/libs:${LD_LIBRARY_PATH:-}"
else
    export LD_LIBRARY_PATH="${APP_DIR}/libs:${LD_LIBRARY_PATH:-}"
fi
export SDL_AUDIODRIVER=alsa
export SDL_VIDEODRIVER=kmsdrm
export HOME="${APP_DIR}"

# App-specific paths
export ROMS_DIR="${ROOT_DIR}/ROMS/"
export IMGS_DIR="${ROOT_DIR}/ROMS/{SYSTEM}/images/{IMAGE_NAME}-image.png"
export EXECUTABLES_DIR="${APP_DIR}/assets/executables/"

# Ensure executables are runnable
chmod -R 755 "${APP_DIR}/assets/executables" || true

PYTHON_BIN="$(command -v python3 || command -v /opt/muos/python/bin/python3 || true)"
if [ -z "${PYTHON_BIN}" ]; then
    echo "python3 not found on device" | tee -a "${LOG_FILE}"
    exit 1
fi

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
