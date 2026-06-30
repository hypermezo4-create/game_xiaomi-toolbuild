#!/usr/bin/env python3
import glob
import os
import sys
from pathlib import Path

SUPER_PARTS = {
    "system", "vendor", "product", "odm", "system_ext", "mi_ext",
    "system_dlkm", "vendor_dlkm", "odm_dlkm", "product_dlkm",
}

BOOT_IMAGES = ["boot.img", "init_boot.img", "vendor_boot.img"]
SPECIAL_SKIP = {"super.img", "cust.img", "md1img.img", "md1img_ww.img"}


def read_text(path, default=""):
    try:
        p = Path(path)
        if p.exists():
            val = p.read_text(encoding="utf-8", errors="ignore").strip()
            return val if val else default
    except Exception:
        pass
    return default


def write_text(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")


def list_images(images_dir):
    return sorted([p.name for p in Path(images_dir).glob("*") if p.is_file()])


def build_plan(images_dir):
    names = list_images(images_dir)

    preloader = None
    for name in names:
        lower = name.lower()
        if lower.startswith("preloader") and (lower.endswith(".bin") or lower.endswith(".img")):
            preloader = name
            break

    plan = {
        "preloader": preloader,
        "has_md1img": "md1img.img" in names,
        "has_md1img_ww": "md1img_ww.img" in names,
        "super": "super.img" in names,
        "cust": "cust.img" in names,
        "boot": [],
        "firmware_ab": [],
    }

    skip = set(SPECIAL_SKIP)
    if preloader:
        skip.add(preloader)

    for image in BOOT_IMAGES:
        if image in names:
            plan["boot"].append(image)
            skip.add(image)

    for image in names:
        if not image.endswith(".img"):
            continue
        if image in skip:
            continue
        part = image[:-4]
        if part in SUPER_PARTS:
            continue
        plan["firmware_ab"].append((part, image))

    return plan


def bat_header(device, format_data):
    mode = "flashed and the data partition will be formatted" if format_data else "flashed without formatting the data partition"
    warning = "You will lose your apps, settings and files on internal storage." if format_data else "You will keep your apps, settings and files on internal storage."
    reason = "Continue if you are flashing this ROM for the first time or downgrading." if format_data else "Continue if you are upgrading from an older compatible ROM."
    return f'''@echo off
cd %~dp0
set fastboot=bin\\windows\\fastboot.exe
if not exist %fastboot% echo %fastboot% not found. & pause & exit /B 1
echo Waiting for device...
set device=
for /f "tokens=2" %%A in ('%fastboot% getvar product 2^>^&1 ^| findstr "\\<product:"') do set device=%%A
if "%device%" equ "" echo Your device could not be detected. & pause & exit /B 1
echo Your device: %device%
if /i "%device%" neq "{device}" echo Compatible devices: {device} & pause & exit /B 1
set hwc=
for /f "tokens=2" %%A in ('%fastboot% getvar hwc 2^>^&1 ^| findstr "\\<hwc:"') do set hwc=%%A

echo Your device will be {mode}.
echo {warning}
echo {reason}
set /p choice=Do you want to continue? [y/N] 
if /i "%choice%" neq "y" exit /B 0

echo ##############################################################
echo Please wait. The device will reboot once flashing is complete.
echo ##############################################################
%fastboot% set_active a
'''


def bat_commands(plan, format_data):
    lines = []

    if plan["preloader"]:
        preloader = plan["preloader"]
        lines.append(f"%fastboot% flash preloader_a images\\{preloader}")
        lines.append(f"%fastboot% flash preloader_b images\\{preloader}")

    for part, image in plan["firmware_ab"]:
        lines.append(f"%fastboot% flash {part}_ab images\\{image}")

    if plan["has_md1img"] and plan["has_md1img_ww"]:
        lines.extend([
            'if "%hwc%" equ "CN" (',
            "%fastboot% flash md1img_ab images\\md1img.img",
            ") else (",
            "%fastboot% flash md1img_ab images\\md1img_ww.img",
            ")",
        ])
    elif plan["has_md1img"]:
        lines.append("%fastboot% flash md1img_ab images\\md1img.img")
    elif plan["has_md1img_ww"]:
        lines.append("%fastboot% flash md1img_ab images\\md1img_ww.img")

    for image in plan["boot"]:
        part = image[:-4]
        lines.append(f"%fastboot% flash {part}_ab images\\{image}")

    if plan["cust"]:
        lines.append("%fastboot% flash cust images\\cust.img")

    if plan["super"]:
        lines.append("%fastboot% flash super images\\super.img")

    if format_data:
        lines.extend([
            "%fastboot% erase metadata",
            "%fastboot% erase userdata",
            "%fastboot% erase expdb",
        ])

    lines.extend([
        "%fastboot% oem cdms",
        "%fastboot% reboot",
        "pause",
    ])
    return "\n".join(lines) + "\n"


def sh_header(device, format_data, platform):
    mode = "flashed and the data partition will be formatted" if format_data else "flashed without formatting the data partition"
    warning = "You will lose your apps, settings and files on internal storage." if format_data else "You will keep your apps, settings and files on internal storage."
    reason = "Continue if you are flashing this ROM for the first time or downgrading." if format_data else "Continue if you are upgrading from an older compatible ROM."
    return f'''#!/bin/sh
cd "$(dirname "$0")"
fastboot=bin/{platform}/fastboot
if [ ! -f $fastboot ]; then echo "$fastboot not found."; exit 1; fi
if [ ! -x $fastboot ] && ! chmod +x $fastboot; then echo "$fastboot cannot be executed."; exit 1; fi
echo "Waiting for device..."
device=$($fastboot getvar product 2>&1 | grep "\\bproduct:" | awk '{{print $2}}')
if [ -z "$device" ]; then echo "Your device could not be detected."; exit 1; fi
echo "Your device: $device"
if [ "$device" != "{device}" ]; then echo "Compatible devices: {device}"; exit 1; fi
hwc=$($fastboot getvar hwc 2>&1 | grep "\\bhwc:" | awk '{{print $2}}')

echo "Your device will be {mode}."
echo "{warning}"
echo "{reason}"
printf "Do you want to continue? [y/N] "
read -r choice
if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then exit 0; fi

echo "##############################################################"
echo "Please wait. The device will reboot once flashing is complete."
echo "##############################################################"
$fastboot set_active a
'''


def sh_commands(plan, format_data):
    lines = []

    if plan["preloader"]:
        preloader = plan["preloader"]
        lines.append(f"$fastboot flash preloader_a images/{preloader}")
        lines.append(f"$fastboot flash preloader_b images/{preloader}")

    for part, image in plan["firmware_ab"]:
        lines.append(f"$fastboot flash {part}_ab images/{image}")

    if plan["has_md1img"] and plan["has_md1img_ww"]:
        lines.extend([
            'if [ "$hwc" = "CN" ]; then',
            "$fastboot flash md1img_ab images/md1img.img",
            "else",
            "$fastboot flash md1img_ab images/md1img_ww.img",
            "fi",
        ])
    elif plan["has_md1img"]:
        lines.append("$fastboot flash md1img_ab images/md1img.img")
    elif plan["has_md1img_ww"]:
        lines.append("$fastboot flash md1img_ab images/md1img_ww.img")

    for image in plan["boot"]:
        part = image[:-4]
        lines.append(f"$fastboot flash {part}_ab images/{image}")

    if plan["cust"]:
        lines.append("$fastboot flash cust images/cust.img")

    if plan["super"]:
        lines.append("$fastboot flash super images/super.img")

    if format_data:
        lines.extend([
            "$fastboot erase metadata",
            "$fastboot erase userdata",
            "$fastboot erase expdb",
        ])

    lines.extend([
        "$fastboot oem cdms",
        "$fastboot reboot",
    ])
    return "\n".join(lines) + "\n"


def format_data_bat():
    return '''@echo off
cd %~dp0
set fastboot=bin\\windows\\fastboot.exe
if not exist %fastboot% echo %fastboot% not found. & pause & exit /B 1
echo Waiting for device...
%fastboot% devices
echo This will format userdata, metadata and expdb.
set /p choice=Do you want to continue? [y/N] 
if /i "%choice%" neq "y" exit /B 0
%fastboot% erase metadata
%fastboot% erase userdata
%fastboot% erase expdb
%fastboot% oem cdms
%fastboot% reboot
pause
'''


def format_data_sh(platform):
    return f'''#!/bin/sh
cd "$(dirname "$0")"
fastboot=bin/{platform}/fastboot
if [ ! -f $fastboot ]; then echo "$fastboot not found."; exit 1; fi
if [ ! -x $fastboot ] && ! chmod +x $fastboot; then echo "$fastboot cannot be executed."; exit 1; fi
echo "Waiting for device..."
$fastboot devices
echo "This will format userdata, metadata and expdb."
printf "Do you want to continue? [y/N] "
read -r choice
if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then exit 0; fi
$fastboot erase metadata
$fastboot erase userdata
$fastboot erase expdb
$fastboot oem cdms
$fastboot reboot
'''


def updater_script(device, plan):
    lines = []
    lines.append('ui_print("Your device: " + getprop("ro.product.device"));')
    lines.append(f'getprop("ro.product.device") == "{device}" || abort("Compatible devices: {device}");')
    lines.append("")
    lines.append('show_progress(0.200000, 0);')
    lines.append('ui_print("Flashing firmware partitions...");')

    if plan["preloader"]:
        p = plan["preloader"]
        lines.append(f'package_extract_file("images/{p}", "/dev/block/bootdevice/by-name/preloader_raw_a");')
        lines.append(f'package_extract_file("images/{p}", "/dev/block/bootdevice/by-name/preloader_raw_b");')

    for part, image in plan["firmware_ab"]:
        lines.append(f'package_extract_file("images/{image}", "/dev/block/bootdevice/by-name/{part}_a");')
        lines.append(f'package_extract_file("images/{image}", "/dev/block/bootdevice/by-name/{part}_b");')

    if plan["has_md1img"] and plan["has_md1img_ww"]:
        lines.extend([
            'ifelse(getprop("ro.boot.hwc") == "CN", (',
            'package_extract_file("images/md1img.img", "/dev/block/bootdevice/by-name/md1img_a");',
            'package_extract_file("images/md1img.img", "/dev/block/bootdevice/by-name/md1img_b");',
            '), (',
            'package_extract_file("images/md1img_ww.img", "/dev/block/bootdevice/by-name/md1img_a");',
            'package_extract_file("images/md1img_ww.img", "/dev/block/bootdevice/by-name/md1img_b");',
            '));',
        ])
    elif plan["has_md1img"]:
        lines.append('package_extract_file("images/md1img.img", "/dev/block/bootdevice/by-name/md1img_a");')
        lines.append('package_extract_file("images/md1img.img", "/dev/block/bootdevice/by-name/md1img_b");')
    elif plan["has_md1img_ww"]:
        lines.append('package_extract_file("images/md1img_ww.img", "/dev/block/bootdevice/by-name/md1img_a");')
        lines.append('package_extract_file("images/md1img_ww.img", "/dev/block/bootdevice/by-name/md1img_b");')

    lines.append('set_progress(1.000000);')
    lines.append("")
    lines.append('show_progress(0.100000, 0);')
    lines.append('ui_print("Flashing boot partitions...");')
    for image in plan["boot"]:
        part = image[:-4]
        lines.append(f'package_extract_file("images/{image}", "/dev/block/bootdevice/by-name/{part}_a");')
        lines.append(f'package_extract_file("images/{image}", "/dev/block/bootdevice/by-name/{part}_b");')
    lines.append('set_progress(1.000000);')

    if plan["cust"]:
        lines.append("")
        lines.append('show_progress(0.100000, 0);')
        lines.append('ui_print("Flashing cust partition...");')
        lines.append('package_unsparse_file("images/cust.img", "/dev/block/bootdevice/by-name/cust");')
        lines.append('set_progress(1.000000);')

    if plan["super"]:
        lines.append("")
        lines.append('show_progress(0.600000, 0);')
        lines.append('ui_print("Flashing super partition...");')
        lines.append('package_unsparse_file("images/super.img", "/dev/block/bootdevice/by-name/super");')
        lines.append('set_progress(1.000000);')

    return "\n".join(lines) + "\n"


def write_metadata(work_dir, out_dir, device):
    base_rom_code = read_text(Path(work_dir) / "bin/ddevice/base_rom_code.txt", "Unknown")
    sdk = read_text(Path(work_dir) / "bin/ddevice/sdkLevel.txt", "0")
    android_ver = read_text(Path(work_dir) / "bin/ddevice/androidver.txt", "")
    security_patch = read_text(Path(work_dir) / "bin/ddevice/security_patch.txt", "unknown")
    timestamp = read_text(Path(work_dir) / "bin/ddevice/build_timestamp.txt", "0")

    metadata = f'''ota-required-cache=0
ota-type=AB
post-build=DeadZone/{device}/{device}:{android_ver}/DeadZone/{base_rom_code}:user/release-keys
post-build-incremental={base_rom_code}
post-sdk-level={sdk}
post-security-patch-level={security_patch}
post-timestamp={timestamp}
pre-device={device}
'''
    write_text(Path(out_dir) / "META-INF/com/android/metadata", metadata)


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_mtk_fastboot.py <work_dir> <out_dir>")
        sys.exit(1)

    work_dir = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve()
    images_dir = out_dir / "images"

    device = read_text(work_dir / "bin/ddevice/device_f.txt", "unknown").strip().lower()
    plan = build_plan(images_dir)

    if not plan["super"]:
        print("[MTK_GENERATOR] ERROR: images/super.img is missing")
        sys.exit(1)

    write_text(out_dir / "windows_install_upgrade.bat", bat_header(device, False) + bat_commands(plan, False))
    write_text(out_dir / "windows_install_and_format_data.bat", bat_header(device, True) + bat_commands(plan, True))
    write_text(out_dir / "windows_format_data_only.bat", format_data_bat())

    write_text(out_dir / "linux_install_upgrade.sh", sh_header(device, False, "linux") + sh_commands(plan, False))
    write_text(out_dir / "linux_install_and_format_data.sh", sh_header(device, True, "linux") + sh_commands(plan, True))
    write_text(out_dir / "linux_format_data_only.sh", format_data_sh("linux"))

    write_text(out_dir / "macos_install_upgrade.sh", sh_header(device, False, "macos") + sh_commands(plan, False))
    write_text(out_dir / "macos_install_and_format_data.sh", sh_header(device, True, "macos") + sh_commands(plan, True))
    write_text(out_dir / "macos_format_data_only.sh", format_data_sh("macos"))

    write_text(out_dir / "META-INF/com/google/android/updater-script", updater_script(device, plan))
    write_metadata(work_dir, out_dir, device)

    for sh_file in glob.glob(str(out_dir / "*.sh")):
        os.chmod(sh_file, 0o755)

    print(f"[MTK_GENERATOR] Generated MTK fastboot scripts for {device}")
    print(f"[MTK_GENERATOR] Images: {', '.join(list_images(images_dir))}")


if __name__ == "__main__":
    main()
