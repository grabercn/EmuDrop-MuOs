# EmuDrop (muOS Fork)

EmuDrop is a controller-first ROM downloader built with Python and SDL2. This fork is tailored for muOS devices (RG35XX family, etc.), with packaging, SDL fixes, and first-boot controller mapping maintained by **Christian Graber**. Base project by Ahmad Teeb.

## Support Me
If you like this project, consider supporting on Buy Me a Coffee:

<p align="center">
  <a href="https://buymeacoffee.com/ahmadteeb" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-dark.png" alt="Buy Me A Coffee" width="200" />
  </a>
</p>

## Device Support

<div align="center">

<table>
  <thead>
    <tr>
      <th>Device</th>
      <th>OS</th>
    </tr>
  </thead>
  <tbody align="center">
    <tr><td>TrimUI Smart Pro</td><td><code>Stock</code> <code>Crossmix</code> <code>Knulli</code> <code>muOS</code></td></tr>
    <tr><td>TrimUI Brick</td><td><code>Stock</code> <code>Crossmix</code> <code>Knulli</code> <code>muOS</code></td></tr>
    <tr><td>RG35XX Original</td><td><code>Knulli</code></td></tr>
    <tr><td>RG35XX 2024</td><td><code>Knulli</code></td></tr>
    <tr><td>RG35XX Plus</td><td><code>Knulli</code></td></tr>
    <tr><td>RG35XX SP</td><td><code>Knulli</code></td></tr>
    <tr><td>RG35XX-H</td><td><code>Knulli</code></td></tr>
    <tr><td>RG35XX-V</td><td><code>Knulli</code></td></tr>
    <tr><td>RG-CubeXX</td><td><code>Knulli</code></td></tr>
  </tbody>
</table>

</div>

## Screenshots

<div align="center">

### Platform Selection
![Platforms View](screenshots/platforms.png)
Browse platforms with controller-friendly navigation.

### Game Selection
![Games View](screenshots/games.png)
Per-platform game browser with cover art.

### Search & Discovery
![Search Interface](screenshots/search.png)
Keyboard-driven search with instant filtering.

### Source Selection
![Sources View](screenshots/sources.png)
Switch between ROM sources per platform.

### Download Center
![Downloads View](screenshots/downloads.png)
Queue management with progress and speed indicators.

</div>

## Features

- Full controller support and on-screen keyboard
- Modern SDL2 UI tuned for handheld resolutions
- Platform and source aware game catalog
- Download queue with progress tracking and resume handling
- ROM image scraping with caching fallback
- SQLite catalog with FTS search
- Bundled SDL2/Pillow runtime for muOS

## Bugs Solved

- Fixed screen timeout when idle
- Resolved SDL2 texture leaks and controller input lag
- Corrected download progress accuracy and resume handling
- Fixed platform detection on Trimui Smart Pro
- Addressed screen tearing and scaling issues
- Improved search handling for special characters
- Hardened cache cleanup and database consistency

## Installation
1. Download the latest release for your OS: https://github.com/ahmadteeb/EmuDrop/releases
2. Deploy to device storage:
   - Stock/Crossmix: `/mnt/SDCARD/Apps/`
   - Knulli: `/userdata/roms/pygame/`
   - muOS: copy `EmuDrop-muOS-*.muxapp` to `/mnt/mmc/ARCHIVE/` (Archive will install into `/mnt/mmc/MUOS/application/EmuDrop`)
3. Optional: run EmuDropKeyConfig from the pygame menu to remap keys on Knulli.

## Requirements

- Target Python runtime: 3.11 on muOS (build tooling cross-installs wheels for `cp311` by default)
- SDL2 runtime (bundled in the muxapp via `sdl2dll`)
- Python packages in `requirements.txt`
- Game catalog SQLite database `assets/catalog.db` (generate with `tools/roms scrapper/migrate_to_sqlite.py`)

## Building for muOS

Linux/WSL:
```bash
make clean dist
# override defaults if needed:
# TARGET_PYTHON_VERSION=3.10 TARGET_PLATFORM=manylinux_2_31_aarch64 make clean dist
```
Requirements: `make`, `zip`, `rsync`, `python3`, `pip`.

Windows host via WSL helper:
```powershell
./build_wsl.ps1 [-Distro <name>] [-OutputCopyPath <path>] `
  [-TargetPythonVersion 3.11] [-TargetPlatform manylinux_2_28_aarch64]
```
Output: `dist/EmuDrop-muOS-<version>.muxapp` ready for `/mnt/mmc/ARCHIVE/`.

## Testing from source

```bash
python main.py
```
- Navigate with D-pad/arrow keys, `A` select, `B` back, `Y` keyboard, `X` downloads, `L/R` page.
- Logs are written to `EmuDrop.log` in the working directory.

## Project Structure

- `app.py` / `main.py`: application entry and loop
- `ui/`: SDL2 UI components
- `utils/`: configuration, logging, downloads, texture handling
- `data/`: SQLite access layer
- `platform/`: platform-specific launch scripts and overlays (muOS assets live here)
- `tools/roms scrapper`: build catalog and migrate to SQLite
- `assets/`: fonts, images, executables, settings

## Contributing
Contributions are welcome! Please submit PRs for fixes or device-specific improvements.

## Acknowledgments

- SDL2 and PySDL2 teams
- Contributors and maintainers
