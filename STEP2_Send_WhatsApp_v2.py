"""
=====================================================================
  STEP 2 — SEND WHATSAPP MESSAGES
  RMA / XBM / Trade-in Pending Shipments
  
  UPDATED: Sends to WhatsApp groups with proper DM tagging
  
  HOW IT WORKS:
  - Reads group metadata from _group_list.json
  - Handles different send modes:
    * tag_all_dms: Sends to group and tags each DM
    * send_to_group: Just sends screenshot
    * send_to_both_groups: Sends to multiple groups (Dallas, etc)
  - Opens WhatsApp Desktop and sends via chat interface
  
  IMPORTANT: Keep WhatsApp Desktop open!
  Run STEP 1 first, then this script.
=====================================================================
"""

import pyautogui
import pyperclip
import time
import os
import json
import win32clipboard
import win32con

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
METADATA_FILE = os.path.join(OUTPUT_FOLDER, "_group_list.json")

# PyAutoGUI settings
pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = False

# WhatsApp Desktop search field location (approximate - may need adjustment)
WHATSAPP_SEARCH_X = 100
WHATSAPP_SEARCH_Y = 50

# Time delays (seconds)
DELAY_SEARCH_OPEN = 0.5
DELAY_GROUP_SELECT = 1.5
DELAY_MESSAGE_SEND = 1.0
DELAY_BETWEEN_DMS = 2.0

# ─────────────────────────────────────────────────────────────

def focus_whatsapp():
    """Bring WhatsApp window to foreground."""
    pyautogui.click(WHATSAPP_SEARCH_X, WHATSAPP_SEARCH_Y)
    time.sleep(0.5)

def search_group(group_name):
    """
    Search for WhatsApp group using Ctrl+F.
    Returns True if group was found and selected.
    """
    print(f"    Searching for: {group_name}")
    
    focus_whatsapp()
    time.sleep(DELAY_SEARCH_OPEN)
    
    # Open search with Ctrl+F
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # Clear existing search and type group name
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyperclip.copy(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # Press Down arrow to select first result
    pyautogui.press('down')
    time.sleep(DELAY_GROUP_SELECT)
    
    # Press Enter to open group
    pyautogui.press('return')
    time.sleep(DELAY_MESSAGE_SEND)
    
    # Close search with Escape
    pyautogui.press('escape')
    time.sleep(0.5)
    
    return True

def send_image(image_path):
    """Send image file to currently open chat."""
    if not os.path.exists(image_path):
        print(f"      ❌ Image not found: {image_path}")
        return False
    
    print(f"      Sending image: {os.path.basename(image_path)}")
    
    # Copy the actual file to the clipboard so WhatsApp attaches it
    copy_file_to_clipboard(image_path)

    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height - 60)
    time.sleep(0.2)
    
    # Ctrl+V to paste image
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    
    # Press Enter to send
    pyautogui.press('return')
    time.sleep(DELAY_MESSAGE_SEND)
    
    print(f"      ✅ Image sent")
    return True

def send_message(message_text):
    """Send text message to currently open chat."""
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height - 60)
    time.sleep(0.2)
    pyperclip.copy(message_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.press('return')
    time.sleep(DELAY_MESSAGE_SEND)

def copy_file_to_clipboard(file_path):
    """Copy a file to the Windows clipboard so WhatsApp pastes it as an attachment."""
    absolute_path = os.path.abspath(file_path)
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_HDROP, [absolute_path])
    finally:
        win32clipboard.CloseClipboard()

def build_reminder_caption(dms):
    """Build the reminder text to match the provided reference."""
    tag_lines = []
    for dm_info in dms:
        dm_name = dm_info.get('name', '').strip()
        if dm_name:
            tag_lines.append(f"@{dm_name}")

    tag_block = "\n".join(tag_lines)
    if tag_block:
        tag_block += "\n\n"

    return (
        f"{tag_block}"
        "  🚨 URGENT REMINDER 🚨\n\n"
        "Important reminder that the RMA, XBM & TRADE-IN shipments listed are still pending and are approaching the deadline ⏳\n\n"
        "⚠️ Delayed shipment may result in chargebacks, so we kindly request you to prioritize shipping these devices as soon as possible 🚚📦\n\n"
        "If you need any support, clarification, or assistance, please feel free to reach out — we’re here to help 🤝\n\n"
        "✨"
    )

def process_group(group_data):
    """Process a single WhatsApp group."""
    whatsapp_group = group_data.get('whatsapp_group')
    send_mode = group_data.get('send_mode')
    image_path = group_data.get('image')
    dms = group_data.get('dms', [])
    record_count = group_data.get('record_count', 0)
    markets = group_data.get('markets', [])
    caption = build_reminder_caption(dms)
    
    print(f"\n{'─'*60}")
    print(f"Group: {whatsapp_group}")
    print(f"Mode: {send_mode}")
    print(f"Markets: {', '.join(markets)}")
    print(f"Records: {record_count}")
    print(f"DMs: {len(dms)}")
    print(f"{'─'*60}")
    
    # Handle different modes
    if send_mode == "tag_all_dms":
        # Mode: Send to group and tag each DM individually
        print(f"\n  Sending with DM tags (tag_all_dms mode)")
        
        # Search for and open group
        if not search_group(whatsapp_group):
            print(f"  ❌ Could not find group: {whatsapp_group}")
            return False
        
        # Send the reminder text first, then the screenshot
        send_message(caption)

        # Send image
        if image_path and os.path.exists(image_path):
            send_image(image_path)
        
        print(f"  ✅ Completed")
        return True
    
    elif send_mode == "send_to_group":
        # Mode: Just send screenshot to group
        print(f"\n  Sending to group (send_to_group mode)")
        
        # Search for and open group
        if not search_group(whatsapp_group):
            print(f"  ❌ Could not find group: {whatsapp_group}")
            return False
        
        # Send the reminder text first, then the screenshot
        send_message(caption)

        # Send image
        if image_path and os.path.exists(image_path):
            send_image(image_path)
        
        print(f"  ✅ Completed")
        return True
    
    elif send_mode == "send_to_both_groups":
        # Mode: Send same screenshot to multiple groups (Dallas case)
        print(f"\n  Sending to multiple groups (send_to_both_groups mode)")
        
        # For Dallas, we send to both South and North
        dal_groups = ["Dallas Team South", "Dallas Team North"]
        
        for dal_group in dal_groups:
            print(f"\n    → Sending to: {dal_group}")
            
            # Search for and open group
            if not search_group(dal_group):
                print(f"      ❌ Could not find group: {dal_group}")
                continue
            
            # Send the reminder text first, then the screenshot
            send_message(caption)

            # Send image
            if image_path and os.path.exists(image_path):
                send_image(image_path)
            
            time.sleep(2)  # Wait between groups
        
        print(f"  ✅ Completed")
        return True
    
    else:
        print(f"  ❌ Unknown send mode: {send_mode}")
        return False

def main():
    print("=" * 70)
    print("  STEP 2 — Sending WhatsApp Messages to Groups")
    print("=" * 70)
    
    # Load group metadata
    if not os.path.exists(METADATA_FILE):
        print(f"\n❌ Metadata file not found: {METADATA_FILE}")
        print("   Run STEP1_Generate_Screenshots_v2.py first!")
        input("\nPress Enter to exit...")
        return
    
    with open(METADATA_FILE, 'r') as f:
        group_list = json.load(f)
    
    print(f"\nLoaded {len(group_list)} groups from metadata")
    
    # Verify images exist
    missing = 0
    for group_data in group_list:
        img_path = group_data.get('image')
        if img_path and not os.path.exists(img_path):
            missing += 1
            print(f"  ⚠️  Missing image: {img_path}")
    
    if missing:
        print(f"\n⚠️  {missing} images missing. Continuing anyway...")
    
    # Show instructions
    print("\n" + "=" * 70)
    print("IMPORTANT INSTRUCTIONS:")
    print("=" * 70)
    print("""
1. Make sure WhatsApp Desktop is OPEN
2. Maximize the WhatsApp window
3. The script will use Ctrl+F to search for groups
4. Once groups are found, screenshots will be sent automatically
5. For DM tagging mode, individual @mentions will be sent
6. Press Ctrl+C at any time to abort (emergency exit)

Ready to start? Press Enter to continue...
    """)
    
    input()
    
    # Send to each group
    print("\n" + "=" * 70)
    print("STARTING MESSAGE DELIVERY")
    print("=" * 70)
    
    success_count = 0
    error_count = 0
    
    for idx, group_data in enumerate(group_list, 1):
        try:
            print(f"\n[{idx}/{len(group_list)}]")
            if process_group(group_data):
                success_count += 1
            else:
                error_count += 1
            
            # Wait between groups
            time.sleep(3)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Script aborted by user")
            break
        except Exception as e:
            print(f"\n❌ Error processing group: {e}")
            error_count += 1
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 70)
    print("DELIVERY COMPLETE")
    print("=" * 70)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {error_count}")
    print(f"Total: {len(group_list)}")
    print("=" * 70)
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
