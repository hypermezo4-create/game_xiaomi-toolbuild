#!/bin/bash

baserom="$1"
work_dir=$(pwd)
source $work_dir/functions.sh
# Check whether it is a local package or a link
if [ ! -f "${baserom}" ] && [ "$(echo $baserom |grep http)" != "" ]; then
    info "Download link detected, starting a download..."
    aria2c --max-download-limit=1024M --file-allocation=none -s10 -x10 -j10 ${baserom}
    baserom=$(basename ${baserom} | sed 's/\?t.*//')
    if [ -f $work_dir/topaz-ota_full-OS3.0.2.0.WMGCNXM-user-16.0-b487e82659.zip ]; then
        baserom="topaz-ota_full-OS3.0.2.0.WMGCNXM-user-16.0-b487e82659.zip"
        info "BASEROM: ${baserom}"
    elif [ -f $work_dir/munch-ota_full-OS2.0.215.0.VLMCNXM-user-15.0-7df6d5ee94.zip ]; then
        baserom="munch-ota_full-OS2.0.215.0.VLMCNXM-user-15.0-7df6d5ee94.zip"
        info "BASEROM: ${baserom}"
    elif [ ! -f "${baserom}" ]; then
        error "Download error!"
    fi
elif [ -f "${baserom}" ]; then
    info "BASEROM: ${baserom}"
else
    error "BASEROM: Invalid parameter"
    exit
fi


# Get ROM Info
raw_device_code=""

if [ "$(echo "$baserom" | grep miui_)" != "" ]; then
    raw_device_code=$(basename "$baserom" | cut -d '_' -f 2)
    base_rom_code=$(basename "$baserom" | awk -F'_' '{print $3}')
elif [ "$(echo "$baserom" | grep xiaomi.eu_)" != "" ]; then
    raw_device_code=$(basename "$baserom" | cut -d '_' -f 3)
    base_rom_code=$(basename "$baserom" | awk -F'_' '{print $3}')
elif [ "$(echo "$baserom" | grep -E '.*-ota_full-.*')" != "" ]; then
    raw_device_code=$(basename "$baserom" | cut -d '-' -f 1)
    base_rom_code=$(basename "$baserom" | cut -d '-' -f 3)
else
    raw_device_code="YourDevice"
    base_rom_code="Unknown"
fi

raw_device_code=$(printf '%s' "$raw_device_code" | tr '[:upper:]' '[:lower:]')

# Split codename and region safely.
# Examples:
# moon_global       -> device_f=moon,   DEVICE_TYPE=Global
# tapas_eea_global  -> device_f=tapas,  DEVICE_TYPE=EEAGlobal
# houji_tw_global   -> device_f=houji,  DEVICE_TYPE=TWGlobal
# zircon            -> device_f=zircon, DEVICE_TYPE=China
case "$raw_device_code" in
    *_eea_global)
        device_f="${raw_device_code%_eea_global}"
        DEVICE_TYPE="EEAGlobal"
        ;;
    *_in_global)
        device_f="${raw_device_code%_in_global}"
        DEVICE_TYPE="INGlobal"
        ;;
    *_id_global)
        device_f="${raw_device_code%_id_global}"
        DEVICE_TYPE="IDGlobal"
        ;;
    *_ru_global)
        device_f="${raw_device_code%_ru_global}"
        DEVICE_TYPE="RUGlobal"
        ;;
    *_tw_global)
        device_f="${raw_device_code%_tw_global}"
        DEVICE_TYPE="TWGlobal"
        ;;
    *_tr_global)
        device_f="${raw_device_code%_tr_global}"
        DEVICE_TYPE="TRGlobal"
        ;;
    *_jp_global)
        device_f="${raw_device_code%_jp_global}"
        DEVICE_TYPE="JPGlobal"
        ;;
    *_global)
        device_f="${raw_device_code%_global}"
        DEVICE_TYPE="Global"
        ;;
    *)
        device_f="$raw_device_code"
        DEVICE_TYPE="China"
        ;;
esac

device_code=$(printf '%s' "$device_f" | tr '[:lower:]' '[:upper:]')

info "Get Device Type"#Check MIUI or Hyper
if echo "$base_rom_code" | grep -q "OS1"; then
    ROM_OS="OS1"
elif echo "$base_rom_code" | grep -q "OS2"; then
    ROM_OS="OS2"
elif echo "$base_rom_code" | grep -q "OS3"; then
    ROM_OS="OS3"
elif echo "$base_rom_code" | grep -q "V14"; then
    ROM_OS="MIUI"
elif echo "$base_rom_code" | grep -q "V13"; then
    ROM_OS="MIUI"
else
    echo "Unsupport ROM Exiting..."
    exit 1
fi

echo $base_rom_code > $work_dir/bin/ddevice/base_rom_code.txt
echo $base_rom_code > $work_dir/bin/ddevice/os_code.txt
echo $device_code > $work_dir/bin/ddevice/device_code.txt
echo $DEVICE_TYPE > $work_dir/bin/ddevice/device_type.txt
echo $ROM_OS > $work_dir/bin/ddevice/rom_os.txt


