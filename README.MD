<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:020617,35:111827,70:7F1D1D,100:DC2626&height=260&section=header&text=DeadZone%20GamingPlus&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=34&desc=Premium%20Xiaomi%20HyperOS%20%2F%20MIUI%20ROM%20Automation%20%E2%80%A2%20By%20MEZO&descSize=16&descAlignY=57" />
</p>

<h1 align="center">🔥 DeadZone GamingPlus 🔥</h1>

<h3 align="center">
  Xiaomi HyperOS / MIUI ROM Build System • Automated ROM Factory • By MEZO
</h3>

<p align="center">
  <a href="https://t.me/xDeadZoneh">
    <img src="https://img.shields.io/badge/DeadZone-Updates-DC2626?style=for-the-badge&logo=telegram&logoColor=white" />
  </a>
  <a href="https://github.com/hypermezo4-create/game_xiaomi-toolbuild">
    <img src="https://img.shields.io/badge/GitHub-Repository-111827?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/Edition-GamingPlus-F43F5E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Creator-MEZO-2563EB?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/HyperOS-Supported-38BDF8?style=flat-square" />
  <img src="https://img.shields.io/badge/MIUI-Supported-F97316?style=flat-square" />
  <img src="https://img.shields.io/badge/Android-13%20%7C%2014%20%7C%2015%20%7C%2016-22C55E?style=flat-square" />
  <img src="https://img.shields.io/badge/Build-GitHub%20Actions-111827?style=flat-square" />
  <img src="https://img.shields.io/badge/Upload-Google%20Drive-4285F4?style=flat-square" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=800&size=22&duration=2600&pause=800&color=F43F5E&center=true&vCenter=true&width=980&lines=DeadZone+GamingPlus+ROM+Automation;Xiaomi+%7C+HyperOS+%7C+MIUI+Build+System;Payload+Extraction+%7C+Super+Repack+%7C+Cloud+Upload;Fast.+Clean.+Organized.+By+MEZO" />
</p>

---

## 🧬 Project DNA

<table>
<tr>
<td width="50%">

### 🔥 Brand

```txt
DeadZone By MEZO
```

A clean and powerful ROM automation identity focused on speed, structure, and reliable release delivery.

</td>
<td width="50%">

### 🎮 Default Edition

```txt
GamingPlus
```

A performance-focused build style designed for users who want a clean, enhanced Xiaomi ROM experience.

</td>
</tr>
<tr>
<td width="50%">

### 📱 Target Devices

```txt
Xiaomi / Redmi / POCO
```

Built for Xiaomi ecosystem devices using HyperOS or MIUI base packages.

</td>
<td width="50%">

### ⚙️ Build System

```txt
GitHub Actions + Linux Toolchain
```

Automated extraction, patching, repacking, upload, and notification workflow.

</td>
</tr>
</table>

---

## 🧠 Overview

**DeadZone GamingPlus** is a Xiaomi ROM build and automation system created by **MEZO**.

It is designed to process Xiaomi HyperOS / MIUI base ROM packages, extract system partitions, apply DeadZone GamingPlus modifications, repack the ROM, generate a flashable ZIP, upload the final build to Google Drive, and send build status through Telegram workflows.

> **Build clean. Patch smart. Release with confidence.**

---

## 🚀 Build Pipeline

```mermaid
flowchart LR
    A[ROM Link] --> B[Download Base ROM]
    B --> C[Detect ROM Type]
    C --> D[Extract Payload / Super]
    D --> E[Extract Dynamic Partitions]
    E --> F[Apply GamingPlus Mods]
    F --> G[Patch Framework / SystemUI]
    G --> H[Repack Images]
    H --> I[Generate Flashable ZIP]
    I --> J[Upload to Google Drive]
    J --> K[Telegram Notification]
```

---

## ✨ Feature Matrix

<table>
<tr>
<td width="33%">

### 📦 ROM Input

- Direct OTA ROM links
- Payload-based ROM packages
- `payload.bin` support
- `super.img` support
- HyperOS / MIUI packages

</td>
<td width="33%">

### 🛠️ Processing

- Device codename detection
- Android version detection
- ROM region parsing
- EROFS / EXT support
- Dynamic partition extraction

</td>
<td width="33%">

### ☁️ Release

- Final ZIP generation
- SHA256 output
- Google Drive upload
- Per-device folders
- Telegram build status

</td>
</tr>
</table>

---

## 🎮 GamingPlus Direction

```txt
ROM Automation            ████████████████████
Gaming Experience         ███████████████████░
Performance Tweaks        ███████████████████░
HyperOS Customization     ███████████████████░
Cloud Release Pipeline    ███████████████████░
Telegram Workflow         ██████████████████░░
```

---

## 🧩 Supported ROM Layouts

| ROM Layout | Status | Notes |
|---|---:|---|
| Recovery OTA ZIP | ✅ | Standard Xiaomi OTA package |
| Payload ROM | ✅ | Extracts `payload.bin` |
| Dynamic Partitions | ✅ | Handles dynamic partition images |
| `super.img` ROM | ✅ | Supports super-based packages |
| HyperOS | ✅ | HyperOS ROM workflow |
| MIUI | ✅ | MIUI ROM workflow |

---

## 📁 Output Naming

Final builds follow the DeadZone GamingPlus naming format:

```txt
DeadZone_GamingPlus_<VERSION>_<CODENAME>_<ROM_VERSION>_<REGION>-A<ANDROID>.zip
```

Example:

```txt
DeadZone_GamingPlus_V1.06_ZIRCON_OS3.0.303.0.WNOCNXM_ChinaStable-A16.zip
```

---

## ☁️ Upload Structure

Final ROMs are organized by device codename:

```txt
DeadZoneBuilds/
└── GamingPlus/
    ├── ZIRCON/
    ├── PRAGUE/
    └── FUXI/
```

---

## 🛠️ Toolchain

<p align="center">
  <img src="https://skillicons.dev/icons?i=androidstudio,java,python,bash,linux,git,github,githubactions,docker,vscode" />
</p>

<table>
<tr>
<td width="50%">

### Core Tools

- Bash
- Python 3
- Java
- Git
- GitHub Actions
- zip / unzip
- 7z
- curl
- aria2c
- zstd

</td>
<td width="50%">

### Android Image Tools

- payload extractor
- lpmake
- lpunpack
- mkfs.erofs
- fs_config handling
- file_contexts handling
- dynamic partition tools
- image patch utilities

</td>
</tr>
</table>

---

## 📡 Telegram Workflow

<table>
<tr>
<td align="center" width="25%">

### 📥 Request

ROM link received from supported workflow input.

</td>
<td align="center" width="25%">

### ⚙️ Build

GitHub Actions starts the automated build process.

</td>
<td align="center" width="25%">

### ☁️ Upload

Final ZIP is uploaded to Google Drive.

</td>
<td align="center" width="25%">

### ✅ Release

Build metadata and link are sent through Telegram.

</td>
</tr>
</table>

---

## 🧾 Build Metadata

| Metadata | Purpose |
|---|---|
| Device codename | Verifies the correct target device |
| ROM version | Identifies the base package |
| Android version | Shows Android base |
| Region | Shows ROM release region |
| SHA256 | Verifies final ZIP integrity |
| File size | Helps users confirm the download |
| Drive link | Provides final build access |

---

## 🧪 Safety Notes

> Custom ROM building and flashing can be risky. Always verify the target device and base ROM before flashing.

- Use trusted ROM sources only.
- Prefer direct Xiaomi ROM links whenever possible.
- Always verify the device codename.
- Bootloader must be unlocked.
- Back up your data before flashing.
- Do not flash builds on unsupported devices.
- Flashing is always at your own risk.

---

## ⚠️ Disclaimer

This project is provided for educational, development, and ROM automation purposes only.

The developer is not responsible for bricked devices, bootloops, data loss, incorrect flashing, unsupported device usage, failed modifications, or damaged partitions.

---

## 👑 Credits

<table>
<tr>
<td align="center" width="50%">

### 🔥 Project

**DeadZone GamingPlus**

Premium Xiaomi HyperOS / MIUI ROM automation.

</td>
<td align="center" width="50%">

### 👑 Creator

**MEZO**

DeadZone ROM ecosystem builder and maintainer.

</td>
</tr>
</table>

---

<p align="center">
  <a href="https://t.me/xDeadZoneh">
    <img src="https://img.shields.io/badge/Telegram-DeadZone%20Updates-229ED9?style=for-the-badge&logo=telegram&logoColor=white" />
  </a>
  <a href="https://github.com/hypermezo4-create">
    <img src="https://img.shields.io/badge/GitHub-hypermezo4--create-111827?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

<p align="center">
  <b>DeadZone By MEZO</b>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:DC2626,50:111827,100:020617&height=140&section=footer" />
</p>
