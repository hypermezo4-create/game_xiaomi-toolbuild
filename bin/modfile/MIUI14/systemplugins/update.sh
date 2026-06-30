WORK_DIR=$(pwd)
MAIN_FOLDER="$WORK_DIR/build/baserom/images"
rom_os=$(cat $WORK_DIR/bin/ddevice/rom_os.txt)
androidVER=$(cat $WORK_DIR/bin/ddevice/androidver.txt)

MIUISystemUIPluginDIR=$(find "$MAIN_FOLDER" -type d -name "MIUISystemUIPlugin")


if [[ $rom_os == "MIUI" ]];then
    rm -rf $MIUISystemUIPluginDIR/*.apk
    cp -rf $WORK_DIR/bin/modfile/MIUI14/systemplugins/MIUISystemUIPlugin.apk $MIUISystemUIPluginDIR
fi