.PHONY: prepare deps package dist clean clean_build

APP_NAME := EmuDrop
BUILD_ROOT := .build
APP_BUILD := $(BUILD_ROOT)/$(APP_NAME)
DIST_DIR := dist
DIST_DIR_READY := $(DIST_DIR)/.dirstamp
TARGET_PLATFORM ?= manylinux_2_17_aarch64
TARGET_PYTHON_VERSION ?= 3.11
TARGET_PYTHON_ABI ?= cp$(subst .,,$(TARGET_PYTHON_VERSION))

# Try git tag, fallback to version.txt, then dev
VERSION ?= $(shell (git describe --tags --always --dirty 2>/dev/null || true) | head -n1)
ifeq ($(strip $(VERSION)),)
VERSION := $(shell (head -n1 version.txt 2>/dev/null || echo dev) | tr -d '\n')
endif

PYTHON ?= python3
PIP_INSTALL := $(PYTHON) -m pip install --no-cache-dir --platform $(TARGET_PLATFORM) --only-binary=:all: --implementation cp --python-version $(TARGET_PYTHON_VERSION) --abi $(TARGET_PYTHON_ABI)

RUNTIME_REQUIREMENTS := $(BUILD_ROOT)/requirements.muos.txt

SOURCE_DIRS := assets data ui utils
SOURCE_FILES := app.py main.py requirements.txt README.md

RSYNC_EXCLUDES := --exclude __pycache__ --exclude '*.pyc' --exclude '.git*' --exclude 'dist' --exclude '.build' --exclude 'tools/toolchain/workspace' --exclude 'screenshots'

$(BUILD_ROOT):
	mkdir -p $@

$(APP_BUILD):
	mkdir -p $@

$(RUNTIME_REQUIREMENTS): requirements.txt | $(BUILD_ROOT)
	grep -viE '^(pyinstaller|pysdl2-dll)' $< > $@

prepare: clean_build $(APP_BUILD) $(RUNTIME_REQUIREMENTS)
	rsync -a $(RSYNC_EXCLUDES) $(SOURCE_DIRS) $(SOURCE_FILES) $(APP_BUILD)/
	rsync -a platform/muos/EmuDrop/ $(APP_BUILD)/
	cp -f "platform/Trimui Smart Pro/EmuDrop/icon.png" "$(APP_BUILD)/icon.png"
	chmod +x "$(APP_BUILD)/mux_launch.sh"

deps: prepare
	$(PYTHON) -m pip install --upgrade pip
	$(PIP_INSTALL) -r $(RUNTIME_REQUIREMENTS) --target "$(APP_BUILD)/deps"
	mkdir -p "$(APP_BUILD)/libs"
	if [ -d "$(APP_BUILD)/deps/pillow.libs" ]; then mv "$(APP_BUILD)/deps/pillow.libs" "$(APP_BUILD)/libs"; fi
	find "$(APP_BUILD)/deps" -type d -name '*.dist-info' -prune -exec rm -rf {} +
	find "$(APP_BUILD)/deps" -type d -name '__pycache__' -prune -exec rm -rf {} +

ARTIFACT := $(APP_NAME)-muOS-$(VERSION).muxapp

package: deps $(DIST_DIR_READY)
	(cd $(BUILD_ROOT) && zip -rq "../$(DIST_DIR)/$(ARTIFACT)" "$(APP_NAME)")

dist: package

$(DIST_DIR_READY):
	mkdir -p $(DIST_DIR)
	touch $@

clean_build:
	rm -rf "$(APP_BUILD)"

clean:
	rm -rf "$(BUILD_ROOT)" "$(DIST_DIR)"
