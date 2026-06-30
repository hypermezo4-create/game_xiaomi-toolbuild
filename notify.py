import os
import sys
import requests
import random
import string

# Ensure UTF-8 encoding for stdout and stderr to avoid crashes on the Windows terminal/Vietnamese language support is not available.
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def read_file_if_exists(path, default=""):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                val = f.read().strip()
                return val if val else default
        except Exception:
            return default
    return default

def get_status_info(status):
    status = status.lower()
    if status == 'start': 
        return "🚀", "INITIAL ENVIRONMENT", "Setting up ROM build environment..."
    if status == 'download': 
        return "📥", "DOWNLOAD BASE ROM", "Downloading the original ROM file to the server..."
    if status == 'unpack': 
        return "🔓", "EXTRACTING PARTITIONS", "Extracting payload.bin / file new.dat.br..."
    if status == 'build': 
        return "🛠️", "BUILD & PATCH ROM", "ROM building and system patching in progress..."
    if status == 'pack': 
        return "📦", "PACKAGING ROM ZIP", "Compressing partitions and packaging flashable files..."
    if status == 'upload': 
        return "📤", "UPDATE FINAL PRODUCT TO CLOUD", "Uploading ROM zip file to Google Drive..."
    if status == 'success': 
        return "✅", "BUILD COMPLETED SUCCESSFULLY", "ROM build request completed successfully! 🎉"
    if status == 'fail': 
        return "❌", "BUILD PROCESS FAILS", "A serious error occurred during the build process!"
    
    # If transmitting any status not in the above list
    return "ℹ️", "CẬP NHẬT TRẠNG THÁI", status.upper()

def get_progress_bar(status):
    stages = ['start', 'download', 'unpack', 'build', 'pack', 'upload', 'success']
    status = status.lower()
    
    current_index = -1
    if status in stages:
        current_index = stages.index(status)
        
    timeline = []
    for i, stage in enumerate(stages):
        if status == 'fail' and i == 6:
            timeline.append("❌")
        elif i < current_index:
            timeline.append("🟢")
        elif i == current_index:
            if status == 'success':
                timeline.append("✅")
            else:
                timeline.append("🔵")
        else:
            timeline.append("⚪")
            
    return " ➔ ".join(timeline)

def is_available(value):
    if not value:
        return False
    val_lower = value.strip().lower()
    if val_lower in ["", "unknown", "Unknown", "Determining...", "⏳ Scanning..."]:
        return False
    return True

def send_notification(status, repo_name, rom_link, channel_id, bot_token, msg_id=None, build_id="Unknown", builder_name="", builder_id=""):
    icon, status_title, status_desc = get_status_info(status)

    # Use GITHUB_RUN_ID to create a link pointing to the Action log.
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id:
        action_url = f"https://github.com/{repo_name}/actions/runs/{run_id}"
    else:
        action_url = f"https://github.com/{repo_name}/actions"

    # Read detailed device information from BuildTool files.
    device_name = read_file_if_exists("bin/ddevice/device_name.txt")
    if not device_name:
        device_name = read_file_if_exists("bin/ddevice/name_devices.txt")
        
    codename = read_file_if_exists("bin/ddevice/device_code.txt")
    if not codename:
        codename = read_file_if_exists("bin/ddevice/device_model.txt")
        
    device_model = read_file_if_exists("bin/ddevice/device_model.txt")
    
    rom_os = read_file_if_exists("bin/ddevice/rom_os.txt")
    if not rom_os:
        rom_os = read_file_if_exists("bin/ddevice/brand_os.txt")
    if not rom_os:
        rom_os = read_file_if_exists("bin/ddevice/brand.txt")
    if rom_os in ["OS1", "OS2", "OS3"]:
        rom_os = "HyperOS"
        
    version_rom = read_file_if_exists("bin/ddevice/rom_version.txt")
    if not version_rom:
        version_rom = read_file_if_exists("bin/ddevice/base_rom_code.txt")
    if not version_rom:
        version_rom = read_file_if_exists("bin/ddevice/base_build_id.txt")
        
    android_ver = read_file_if_exists("bin/ddevice/androidver.txt")
    sdk_level = read_file_if_exists("bin/ddevice/sdkLevel.txt")
    
    region = read_file_if_exists("bin/ddevice/rom_region.txt")
    if not region:
        region = read_file_if_exists("bin/ddevice/device_type.txt")
        
    chip = read_file_if_exists("bin/script2flash/META-INF/Data/Chip")
    structure = read_file_if_exists("bin/script2flash/META-INF/Data/Structure")
    fs_type = read_file_if_exists("bin/ddevice/fstype.txt")
    version_tool = read_file_if_exists("Version")
    output_zip = read_file_if_exists("bin/ddevice/output_zip.txt")

    builder_text = builder_name if builder_name else "🤖 System"

    message_lines = [
        f"🚀 *ROM BUILD PROCESS*",
        f"━━━━━━━━━━━━━━━━━━",
        f"👤 *Builder:* {builder_text}"
    ]

    # Display information only if the information has been retrieved and is not empty.
    if is_available(device_name):
        message_lines.append(f"📱 *Device:* `{device_name}`")
    if is_available(codename):
        message_lines.append(f"🔑 *Codename:* `{codename}`")
        
    os_parts = []
    if is_available(rom_os):
        os_parts.append(rom_os)
    if is_available(version_rom):
        os_parts.append(version_rom)
    if os_parts:
        message_lines.append(f"💿 *Operating system:* `{' | '.join(os_parts)}`")
        
    if is_available(region):
        message_lines.append(f"🌐 *Area (Region):* `{region}`")
        
    android_parts = []
    if is_available(android_ver):
        android_parts.append(f"Android {android_ver}")
    if is_available(sdk_level):
        android_parts.append(f"SDK {sdk_level}")
    if android_parts:
        message_lines.append(f"🤖 *Android:* `{' | '.join(android_parts)}`")
        
    fs_parts = []
    if is_available(fs_type):
        fs_parts.append(fs_type)
    if is_available(structure):
        fs_parts.append(structure)
    if fs_parts:
        message_lines.append(f"🗄️ *Structure / FS:* `{' | '.join(fs_parts)}`")
        
    if is_available(version_tool):
        message_lines.append(f"🛠️ *Tool version:* `{version_tool}`")
        
    message_lines.append(f"━━━━━━━━━━━━━━━━━━")
    message_lines.append(f"📊 *Status:* {icon} *{status_title}*")
    message_lines.append(f"📝 *Detail:* _{status_desc}_")
    message_lines.append(f"📈 *Process:* `{get_progress_bar(status)}`")
    message_lines.append("")

    if status.lower() == 'success' and output_zip:
        message_lines.append(f"📦 *Zip file name:* `{output_zip}`")
        message_lines.append("")

    message_lines.append(f"🆔 *Build ID:* `{build_id}`")
    message_lines.append(f"🚀 *Log build:* [See here]({action_url})")
    message_lines.append(f"🔗 *Base ROM (Source):* [Click here]({rom_link})")

    message = "\n".join(message_lines)

    if msg_id:
        # If we already have the msg_id, we can edit the old message.
        url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        payload = {
            "chat_id": channel_id,
            "message_id": msg_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
    else:
        # If it's not there yet, send a new message.
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        res_data = response.json()
        
        # Get the message_id of the message just sent.
        new_msg_id = res_data.get('result', {}).get('message_id')
        
        # Write the message_id to the GitHub Actions environment variable so that it can be reused in subsequent steps.
        if not msg_id and new_msg_id and "GITHUB_ENV" in os.environ:
            with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
                f.write(f"TELEGRAM_MSG_ID={new_msg_id}\n")
            print(f"Đã lưu TELEGRAM_MSG_ID={new_msg_id} Go to GITHUB_ENV to automatically update messages..")
            
        print("Notification sent/updated to the channel successfully.!")
        # Send a private message (PM) to the build person if the status is success or failure.
        if status.lower() in ['success', 'fail'] and builder_id:
            pm_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            if status.lower() == 'success':
                pm_text = (
                    f"🎉 *ROM BUILD REQUEST COMPLETED!*\n\n"
                    f"{message}\n"
                    f"⬇️ *Download ROM here:* [https://nothingsvn.vercel.app/](https://nothingsvn.vercel.app/)"
                )
            else:
                pm_text = (
                    f"⚠️ *ROM BUILD REQUEST FAILED!*\n\n"
                    f"{message}\n"
                    f"💡 *Hint:* Please click on the build log link above to see the error details.."
                )
                
            pm_payload = {
                "chat_id": builder_id,
                "text": pm_text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            try:
                requests.post(pm_url, json=pm_payload)
                print(f"A private message (PM) has been sent to the user. {builder_id}")
            except Exception as e:
                print(f"Private message sending error: {e}")

    except Exception as e:
        print(f"Error sending notification: {e}")
        if 'response' in locals():
            print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Use: python notify.py <status> <repo_name> <rom_link> [prefix_id] [builder_name] [builder_id]")
        sys.exit(1)

    status = sys.argv[1]
    repo_name = sys.argv[2]
    rom_link = sys.argv[3]
    
    # Prefix for build ID (e.g., xiaomi, xst, oplus)
    prefix = sys.argv[4] if len(sys.argv) > 4 else "build"
    
    # Information about the builder
    builder_name = sys.argv[5] if len(sys.argv) > 5 else ""
    builder_id = sys.argv[6] if len(sys.argv) > 6 else ""
    
    # Get the token, channel ID, message ID, and build ID from environment variables.
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
    msg_id = os.environ.get("TELEGRAM_MSG_ID") 
    build_id = os.environ.get("TELEGRAM_BUILD_ID")

    # Create a new Build ID if it doesn't exist
    if not build_id:
        random_digits = ''.join(random.choices(string.digits, k=8))
        build_id = f"{prefix}_{random_digits}"
        
        # Save to GITHUB_ENV for use in subsequent steps
        if "GITHUB_ENV" in os.environ:
            with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
                f.write(f"TELEGRAM_BUILD_ID={build_id}\n")

    if not bot_token or not channel_id:
        print("Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID in environment variables.")
        sys.exit(1)

    send_notification(status, repo_name, rom_link, channel_id, bot_token, msg_id, build_id, builder_name, builder_id)
