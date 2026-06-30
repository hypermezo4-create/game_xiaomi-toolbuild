work_dir=$(pwd)
source "$work_dir/functions.sh"

RCLONE_CONFIG_1DRIVE="$work_dir/rclone.conf"
RCLONE_REMOTE_NAME="${RCLONE_REMOTE_NAME:-gdrive}"
RCLONE_UPLOAD_DIR="${RCLONE_UPLOAD_DIR:-DeadZoneBuilds/GamingPlus}"

os_type=$(cat "$work_dir/bin/ddevice/os_type.txt")
base_rom_code=$(cat "$work_dir/bin/ddevice/base_rom_code.txt")
androidVER=$(cat "$work_dir/bin/ddevice/androidver.txt")
rom_os=$(cat "$work_dir/bin/ddevice/rom_os.txt")
regionTYPE=$(cat "$work_dir/bin/ddevice/device_type.txt")
device_code=$(cat "$work_dir/bin/ddevice/device_code.txt")
baserom_type=$(cat "$work_dir/bin/ddevice/romtype.txt")
device_f=$(cat "$work_dir/bin/ddevice/device_f.txt")

if [ "$1" == "setup" ]; then
  if [ -z "${RCLONE_CONFIG_BASE64:-}" ]; then
    echo "[ERROR] - Missing RCLONE_CONFIG_BASE64"
    exit 1
  fi

  if ! printf '%s' "$RCLONE_CONFIG_BASE64" | base64 -d > "$work_dir/rclone.conf" 2>/dev/null; then
    echo "[ERROR] - Invalid RCLONE_CONFIG_BASE64"
    rm -f "$work_dir/rclone.conf"
    exit 1
  fi

  if [ ! -s "$work_dir/rclone.conf" ]; then
    echo "[ERROR] - Failed to create rclone.conf"
    exit 1
  fi

  echo "[OK] - rclone.conf created from RCLONE_CONFIG_BASE64"
  exit 0
fi

if [[ $(git branch --show-current) == "beta" ]]; then
    polyxver="$(cat Version)"
    status="Development"
else
    polyxver="$(cat Version)"
    status="Official"
fi

if [[ $rom_os == "MIUI" ]]; then
    os_type="MIUI"
else
    os_type="HyperOS"
fi

version="$polyxver"
if [[ $version == v* ]]; then
    version="V${version:1}"
fi

codename=$(printf '%s' "$device_f" | tr '[:lower:]' '[:upper:]')

case "$regionTYPE" in
    China) region_stable="ChinaStable" ;;
    Global) region_stable="GlobalStable" ;;
    EEAGlobal) region_stable="EEAStable" ;;
    INGlobal) region_stable="IndiaStable" ;;
    IDGlobal) region_stable="IndonesiaStable" ;;
    RUGlobal) region_stable="RussiaStable" ;;
    TWGlobal) region_stable="TaiwanStable" ;;
    TRGlobal) region_stable="TurkeyStable" ;;
    JPGlobal) region_stable="JapanStable" ;;
    "") region_stable="UnknownStable" ;;
    *) region_stable="$regionTYPE" ;;
esac

android_raw="$androidVER"
if [[ $android_raw == A* ]]; then
    android_tag="$android_raw"
else
    android_tag="A${android_raw%%.*}"
fi

final_zip="DeadZone_GamingPlus_${version}_${codename}_${base_rom_code}_${region_stable}-${android_tag}.zip"
output_file="out/${final_zip}"
chip="$(cat "$work_dir/bin/script2flash/META-INF/Data/Chip" 2>/dev/null || echo "")"

repack "Generating flashing script"

OUT_DIR="$work_dir/out/${os_type}_${device_code}_${base_rom_code}"
OUT_IMAGES_DIR="$OUT_DIR/images"
mkdir -p "$OUT_IMAGES_DIR"

if [[ "$chip" == "Mediatek" ]]; then
    repack "MediaTek detected. Building MTK fastboot final ZIP."

    if [ ! -f "$work_dir/build/baserom/images/super.img" ]; then
        repack "Unable to find super.img before MTK package generation"
        exit 1
    fi

    if [ ! -d "$work_dir/bin/script2flash/mtk_template/bin" ] || [ ! -d "$work_dir/bin/script2flash/mtk_template/META-INF" ]; then
        repack "MTK template is missing. Expected bin/script2flash/mtk_template/bin and META-INF"
        exit 1
    fi

    cp -rf "$work_dir/bin/script2flash/mtk_template/bin" "$OUT_DIR/"
    cp -rf "$work_dir/bin/script2flash/mtk_template/META-INF" "$OUT_DIR/"

    mkdir -p "$OUT_DIR/META-INF/Data"
    if [ -d "$work_dir/bin/script2flash/META-INF/Data" ]; then
        cp -rf "$work_dir/bin/script2flash/META-INF/Data/"* "$OUT_DIR/META-INF/Data/" 2>/dev/null || true
    fi
    echo "$device_f" > "$OUT_DIR/META-INF/Data/DeviceCode"

    mv -f "$work_dir/build/baserom/images/super.img" "$OUT_IMAGES_DIR/super.img"

    SUPER_PARTS="system vendor product odm system_ext mi_ext system_dlkm vendor_dlkm odm_dlkm product_dlkm"
    for img in "$work_dir/build/baserom/images/"*.img "$work_dir/build/baserom/images/"*.bin; do
        [ -e "$img" ] || continue
        name="$(basename "$img")"
        part="${name%.*}"
        skip="false"
        for p in $SUPER_PARTS; do
            if [ "$part" = "$p" ]; then
                skip="true"
                break
            fi
        done
        if [ "$skip" = "true" ]; then
            continue
        fi
        mv -f "$img" "$OUT_IMAGES_DIR/"
    done

    if [ -f "$work_dir/bin/script2flash/cust.img" ]; then
        cp -f "$work_dir/bin/script2flash/cust.img" "$OUT_IMAGES_DIR/"
    fi

    python3 "$work_dir/bin/script2flash/generate_mtk_fastboot.py" "$work_dir" "$OUT_DIR" || {
        repack "Unable to generate MTK fastboot scripts"
        exit 1
    }
else
    repack "Compressing super.img"

    if [ ! -f "$work_dir/build/baserom/images/super.img" ]; then
        repack "Unable to find super.img before compression"
        exit 1
    fi

    zstd --rm "$work_dir/build/baserom/images/super.img" -o "$work_dir/build/baserom/images/super.img.zst" >/dev/null 2>&1 || {
        repack "Unable to compress super.img"
        exit 1
    }

    if [[ ${baserom_type} == 'payload' ]]; then
        mv -f "$work_dir/build/baserom/images/super.img.zst" "$OUT_DIR/"
        mv -f "$work_dir/build/baserom/images/"*.img "$OUT_IMAGES_DIR/" 2>/dev/null || true
    elif [[ ${baserom_type} == 'br' ]]; then
        mv -f "$work_dir/build/baserom/firmware-update/"* "$OUT_IMAGES_DIR/" 2>/dev/null || true
        mv -f "$work_dir/build/baserom/images/super.img.zst" "$OUT_DIR/"
    elif [[ ${baserom_type} == 'super' ]]; then
        mv -f "$work_dir/build/baserom/images/super.img.zst" "$OUT_DIR/"
        mv -f "$work_dir/build/baserom/images/"*.img "$OUT_IMAGES_DIR/" 2>/dev/null || true
    else
        repack "Unknown baserom_type: ${baserom_type}"
        exit 1
    fi

    cp -rf "$work_dir/bin/script2flash/META-INF" "$OUT_DIR/"
    cp -rf "$work_dir/bin/script2flash/"*.bat "$OUT_DIR/" 2>/dev/null || true
    cp -rf "$work_dir/bin/script2flash/"*.sh "$OUT_DIR/" 2>/dev/null || true

    if [ -f "$work_dir/bin/script2flash/cust.img" ]; then
        cp -f "$work_dir/bin/script2flash/cust.img" "$OUT_IMAGES_DIR/"
    fi

    mkdir -p "$OUT_DIR/META-INF/Data"
    echo "$device_f" > "$OUT_DIR/META-INF/Data/DeviceCode"
fi

repack "Done"

find "$OUT_DIR" -exec touch {} +

pushd "$OUT_DIR" >/dev/null || exit 1
zip -r "${os_type}_${device_code}_${base_rom_code}.zip" ./*
mv "${os_type}_${device_code}_${base_rom_code}.zip" "$work_dir/out/"
popd >/dev/null || exit 1

mv "$work_dir/out/${os_type}_${device_code}_${base_rom_code}.zip" "$work_dir/$output_file"
echo "$final_zip" > "$work_dir/bin/ddevice/output_zip.txt"

sha256_value="$(sha256sum "$output_file" | awk '{print $1}')"
echo "$sha256_value" > "$work_dir/bin/ddevice/output_sha256.txt"

python3 - "$output_file" > "$work_dir/bin/ddevice/output_size.txt" <<'PYEOF'
import os
import sys

file_path = sys.argv[1]
size = os.path.getsize(file_path)
units = ["B", "KB", "MB", "GB", "TB"]
value = float(size)

for unit in units:
    if value < 1024.0 or unit == units[-1]:
        if unit == "B":
            print(f"{int(value)} {unit}")
        else:
            print(f"{value:.2f} {unit}")
        break
    value /= 1024.0
PYEOF

repack "Build completed"
repack "Output: "
repack "$(pwd)/$output_file"

upload "Uploading"

UPLOAD_DEVICE_DIR="${RCLONE_UPLOAD_DIR}/${codename}"

rclone -v --config="$RCLONE_CONFIG_1DRIVE" copy "$output_file" "$RCLONE_REMOTE_NAME:$UPLOAD_DEVICE_DIR/" || {
    upload "Error uploading file to Google Drive: $output_file"
    exit 1
}

remote_file="$RCLONE_REMOTE_NAME:$UPLOAD_DEVICE_DIR/$final_zip"
drive_link="$(rclone --config="$RCLONE_CONFIG_1DRIVE" link "$remote_file" 2>/dev/null || true)"

if [ -n "$drive_link" ]; then
    echo "$drive_link" > "$work_dir/bin/ddevice/drive_link.txt"
    upload "Public Google Drive link generated"
else
    upload "Warning: file uploaded but public Google Drive link was not generated"
fi

upload "Clean Workflow.."
rm -rf "$work_dir/out"
rm -rf "$work_dir/build"

upload "Build ${final_zip} successfull!"
