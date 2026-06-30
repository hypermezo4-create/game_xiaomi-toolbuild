<div align="center">

# DeadZone GamingPlus

### Xiaomi HyperOS / MIUI ROM Build System  
#### By MEZO

![DeadZone](https://img.shields.io/badge/DeadZone-GamingPlus-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Xiaomi-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-13%20%7C%2014%20%7C%2015%20%7C%2016-green?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-GitHub%20Actions-black?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

---

## Overview

**DeadZone GamingPlus** is a Xiaomi ROM build system created by **MEZO** for building customized HyperOS and MIUI ROM packages.

The project automates the full ROM workflow: downloading the base ROM, extracting partitions, applying modifications, repacking images, generating a flashable ZIP package, uploading the final build, and publishing build information through Telegram workflows.

---

## Project Identity

- **Project Name:** DeadZone GamingPlus
- **Creator:** MEZO
- **Brand:** DeadZone
- **Default Style:** GamingPlus
- **Target Devices:** Xiaomi / Redmi / POCO
- **Target Systems:** HyperOS and MIUI
- **Build Type:** Automated custom ROM build system
- **Language:** English only

---

## Main Features

- Automated ROM download from direct OTA links
- Payload-based ROM extraction
- Support for `payload.bin`
- Support for dynamic partitions and `super.img`
- Xiaomi device codename detection
- HyperOS / MIUI metadata detection
- Android version detection
- EROFS and EXT image handling
- DeadZone GamingPlus patch workflow
- Final flashable ZIP generation
- Google Drive upload support
- Per-device upload folders
- Telegram private build notifications
- Telegram release workflow support
- GamingPlus branding by default

---

## Supported ROM Types

DeadZone GamingPlus is designed to work with Xiaomi ROM packages such as:

- Recovery OTA ROMs
- Payload-based ROMs
- HyperOS ROM packages
- MIUI ROM packages
- Dynamic partition ROMs
- ROMs containing `super.img`

---

## Build Flow

~~~text
ROM Link
  ↓
Download Base ROM
  ↓
Detect ROM Type
  ↓
Extract payload.bin / super.img
  ↓
Extract Dynamic Partitions
  ↓
Apply DeadZone GamingPlus Mods
  ↓
Repack Partitions
  ↓
Generate super.img
  ↓
Create Flashable ZIP
  ↓
Upload to Google Drive
  ↓
Send Telegram Build Status
~~~

---

## Output Naming

Final builds are generated using the DeadZone GamingPlus naming style:

~~~text
DeadZone_GamingPlus_<VERSION>_<CODENAME>_<ROM_VERSION>_<REGION>-A<ANDROID>.zip
~~~

Example:

~~~text
DeadZone_GamingPlus_V1.06_ZIRCON_OS3.0.303.0.WNOCNXM_ChinaStable-A16.zip
~~~

---

## Upload Structure

Final ROM files are uploaded using a per-device folder structure:

~~~text
DeadZoneBuilds/GamingPlus/<DEVICE_CODENAME>/
~~~

Example:

~~~text
DeadZoneBuilds/GamingPlus/ZIRCON/
DeadZoneBuilds/GamingPlus/PRAGUE/
DeadZoneBuilds/GamingPlus/FUXI/
~~~

---

## Requirements

This project is intended to run inside a Linux-based build environment such as GitHub Actions.

Required tools include:

- Bash
- Python 3
- Java
- 7z
- zip / unzip
- aria2c
- curl
- zstd
- lpmake
- lpunpack
- mkfs.erofs
- Android image tools
- rclone

---

## GitHub Actions Usage

The project can be triggered through GitHub Actions by providing a Xiaomi ROM link as input.

Typical workflow input:

~~~text
ROM_URL=<direct Xiaomi ROM link>
~~~

The build system will automatically process the ROM and generate a DeadZone GamingPlus flashable package.

---

## Telegram Workflow

DeadZone GamingPlus supports Telegram-based workflow integration for:

- Public ROM build requests
- Private build status notifications
- Final success or failure messages
- Release channel publishing
- Build metadata delivery

---

## Important Notes

- Use only trusted ROM sources.
- Use direct downloadable ROM links whenever possible.
- Do not flash builds on unsupported devices.
- Always verify the device codename before flashing.
- The bootloader must be unlocked before flashing custom ROM builds.
- Flashing custom ROMs is done at your own risk.

---

## Disclaimer

This project is provided for educational and development purposes only.

The developer is not responsible for:

- Bricked devices
- Data loss
- Bootloops
- Failed flashes
- Incorrect ROM usage
- Unsupported device flashing

Always back up your data before flashing any custom ROM.

---

## Credits

Created and maintained by **MEZO**.

Project branding:

~~~text
DeadZone By MEZO
~~~

---

<div align="center">

### DeadZone GamingPlus  
#### Built for Xiaomi HyperOS / MIUI ROM customization

</div>