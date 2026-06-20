# """
# =====================================================================
#   STEP 2 — TEST SEND TO PERSONAL NUMBER
#   Sends to YOUR WhatsApp number only for review.
  
#   HOW TO RUN:
#   1. Open WhatsApp Desktop and make sure it is visible
#   2. Run this script
#   3. When countdown starts, CLICK on WhatsApp Desktop
#   4. Keep hands off mouse/keyboard until done
# =====================================================================
# """

# import pyautogui
# import pyperclip
# import time
# import os
# import json
# from PIL import Image
# import win32clipboard
# import win32con
# import io

# # ─────────────────────────────────────────────────────────────
# #  CONFIGURATION
# # ─────────────────────────────────────────────────────────────

# BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
# OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
# METADATA_FILE = os.path.join(OUTPUT_FOLDER, "_group_list.json")

# YOUR_NUMBER = "923108486366"   # your WhatsApp number without +

# pyautogui.FAILSAFE = True      # move mouse to top-left corner to stop
# pyautogui.PAUSE    = 0.5


# def copy_text(text):
#     pyperclip.copy(text)
#     time.sleep(0.5)


# def copy_image(image_path):
#     img = Image.open(image_path).convert("RGB")
#     buf = io.BytesIO()
#     img.save(buf, "BMP")
#     bmp = buf.getvalue()[14:]
#     buf.close()
#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardData(win32con.CF_DIB, bmp)
#     win32clipboard.CloseClipboard()
#     time.sleep(0.5)

# def format_caption(group_data):
#     dms = group_data.get('dms', [])
    
#     # Build tag lines using dmNameRep
#     tag_lines = []
#     for dm in dms:
#         rep_name = dm.get('dmNameRep')
#         # Only tag if dmNameRep exists and is not None/null/empty/dash
#         if rep_name and rep_name != '-' and rep_name != 'null' and str(rep_name).strip():
#             tag_lines.append(f"@{rep_name}")
    
#     tag_block = "\n".join(tag_lines)
#     if tag_block:
#         tag_block += "\n\n"

#     return (
#         f"{tag_block}"
#         "  🚨 URGENT REMINDER 🚨\n\n"
#         "Important reminder that the RMA, XBM & TRADE-IN shipments listed are still pending and are approaching the deadline ⏳\n\n"
#         "⚠️ Delayed shipment may result in chargebacks, so we kindly request you to prioritize shipping these devices as soon as possible 🚚📦\n\n"
#         "If you need any support, clarification, or assistance, please feel free to reach out — we're here to help 🤝\n\n"
#         "✨"
#     )

# def open_chat(number):
#     # Open search bar
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)

#     # Clear whatever is in the search box
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.5)
#     pyautogui.press('backspace')
#     time.sleep(0.5)

#     # Type the number via clipboard (handles special chars)
#     copy_text(number)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.0)

#     # Select first result and open
#     pyautogui.press('down')
#     time.sleep(1.5)
#     pyautogui.press('enter')
#     time.sleep(2.0)

# # ─────────────────────────────────────────────────────────────
# #  SEND ONE GROUP REMINDER
# #  Image sent FIRST (with caption in preview dialog), 
# #  matching exactly how your screenshot looks
# # ─────────────────────────────────────────────────────────────

# def send_reminder(group_data, idx, total):
#     name    = group_data.get('whatsapp_group', '')
#     img     = group_data.get('image', '')
#     count   = group_data.get('record_count', 0)
#     markets = group_data.get('markets', [])

#     print(f"\n[{idx}/{total}] {name}")
#     print(f"  Markets : {', '.join(markets)}")
#     print(f"  Records : {count}")

#     caption = format_caption(group_data)

#     # Open personal chat
#     open_chat(YOUR_NUMBER)
#     time.sleep(1.0)

#     if img and os.path.exists(img):
#         # ── send image with caption (one combined message) ────
#         # 1. Copy image to clipboard
#         copy_image(img)

#         # 2. Paste into WhatsApp input → preview dialog opens
#         pyautogui.hotkey('ctrl', 'v')
#         time.sleep(3.0)

#         # 3. Caption field in preview dialog is now active
#         #    Paste the caption text there
#         copy_text(caption)
#         pyautogui.hotkey('ctrl', 'v')
#         time.sleep(1.0)

#         # 4. Press Enter to send
#         pyautogui.press('enter')
#         time.sleep(3.0)

#     else:
#         # ── no image: send caption as plain text ──────────────
#         print(f"  ⚠️  No image — sending text only")
#         copy_text(caption)
#         pyautogui.hotkey('ctrl', 'v')
#         time.sleep(1.0)
#         pyautogui.press('enter')
#         time.sleep(2.0)

#     print(f"  ✅ Sent")

# # ─────────────────────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────────────────────

# def main():
#     print("=" * 60)
#     print("  STEP 2 TEST — Send to Personal Number")
#     print("=" * 60)
#     print(f"\n📱 Sending ALL reminders to: +{YOUR_NUMBER}")

#     if not os.path.exists(METADATA_FILE):
#         print(f"\n❌ Metadata not found. Run STEP1 first!")
#         input("\nPress Enter to exit...")
#         return

#     with open(METADATA_FILE) as f:
#         group_list = json.load(f)

#     total = len(group_list)
#     print(f"✅ Loaded {total} groups\n")

#     missing = sum(1 for g in group_list if g.get('image') and not os.path.exists(g['image']))
#     if missing:
#         print(f"⚠️  {missing} image(s) missing\n")

#     print("─" * 60)
#     print("INSTRUCTIONS:")
#     print("  1. Make sure WhatsApp Desktop is OPEN")
#     print("  2. Press Enter below")
#     print("  3. You have 5 seconds to CLICK on WhatsApp Desktop")
#     print("  4. Then keep hands off mouse and keyboard")
#     print("  5. Move mouse to TOP-LEFT corner at any time to stop")
#     print("─" * 60)
#     input("\nPress Enter to start...")

#     # Countdown — user clicks WhatsApp during this time
#     print("\nClick on WhatsApp Desktop NOW!")
#     for i in range(5, 0, -1):
#         print(f"  Starting in {i}...", end="\r")
#         time.sleep(1)
#     print("\n\nGO!\n")

#     ok = fail = 0

#     for idx, group in enumerate(group_list, 1):
#         try:
#             send_reminder(group, idx, total)
#             ok += 1
#             time.sleep(3.0)   # pause between groups

#         except pyautogui.FailSafeException:
#             print("\n🛑 Stopped by user (mouse moved to corner)")
#             break
#         except KeyboardInterrupt:
#             print("\n🛑 Stopped by Ctrl+C")
#             break
#         except Exception as e:
#             print(f"  ❌ Error: {e}")
#             import traceback; traceback.print_exc()
#             fail += 1
#             time.sleep(2)

#     print("\n" + "=" * 60)
#     print(f"✅ Sent   : {ok}")
#     print(f"❌ Failed : {fail}")
#     print(f"Total     : {total}")
#     print("=" * 60)
#     print(f"\n📱 Check WhatsApp on +{YOUR_NUMBER}")
#     input("\nPress Enter to exit...")


# if __name__ == "__main__":
#     main()









"""
=====================================================================
  STEP 2 — TEST SEND TO PERSONAL NUMBER (FOCUS FIX)
  Sends to YOUR WhatsApp number only for review.
  
  KEY FIX: Clicks on WhatsApp window first to ensure focus
  
  HOW TO RUN:
  1. Open WhatsApp Desktop and make sure it is visible
  2. Run this script
  3. When countdown starts, CLICK on WhatsApp Desktop
  4. Keep hands off mouse/keyboard until done
=====================================================================
"""

import pyautogui
import pyperclip
import time
import os
import json
from PIL import Image
import win32clipboard
import win32con
import io

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
METADATA_FILE = os.path.join(OUTPUT_FOLDER, "_group_list.json")

YOUR_NUMBER = "923108486366"   # your WhatsApp number without +

pyautogui.FAILSAFE = True      # move mouse to top-left corner to stop
pyautogui.PAUSE    = 0.5


def copy_text(text):
    pyperclip.copy(text)
    time.sleep(0.5)


def copy_image(image_path):
    img = Image.open(image_path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "BMP")
    bmp = buf.getvalue()[14:]
    buf.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, bmp)
    win32clipboard.CloseClipboard()
    time.sleep(0.5)

def format_caption(group_data):
    dms = group_data.get('dms', [])
    
    tag_lines = []
    for dm in dms:
        rep_name = dm.get('dmNameRep')
        if rep_name and rep_name != '-' and rep_name != 'null' and str(rep_name).strip():
            tag_lines.append(f"@{rep_name}")
    
    tag_block = "\n".join(tag_lines)
    if tag_block:
        tag_block += "\n\n"

    return (
        f"{tag_block}"
        "  🚨 URGENT REMINDER 🚨\n\n"
        "Important reminder that the RMA, XBM & TRADE-IN shipments listed are still pending and are approaching the deadline ⏳\n\n"
        "⚠️ Delayed shipment may result in chargebacks, so we kindly request you to prioritize shipping these devices as soon as possible 🚚📦\n\n"
        "If you need any support, clarification, or assistance, please feel free to reach out — we're here to help 🤝\n\n"
        "✨"
    )

def focus_whatsapp():
    """
    Click on WhatsApp window to ensure it's focused.
    Clicks in the center of the screen where WhatsApp should be.
    """
    screen_width, screen_height = pyautogui.size()
    
    # Click in the center of WhatsApp (assuming it's maximized/full screen)
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(0.5)
    
    # Click again to be sure
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(0.5)
    
    print(f"  🎯 Focused WhatsApp")

def open_chat(number):
    """
    Search for and open a chat by number.
    Ensures WhatsApp is focused first.
    """
    # First focus WhatsApp
    focus_whatsapp()
    time.sleep(0.5)
    
    # Open search bar
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)

    # Clear whatever is in the search box
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('backspace')
    time.sleep(0.5)

    # Type the number via clipboard
    copy_text(number)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.0)

    # Select first result and open
    pyautogui.press('down')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2.0)
    
    print(f"  ✅ Opened chat")

# ─────────────────────────────────────────────────────────────
#  SEND ONE GROUP REMINDER
# ─────────────────────────────────────────────────────────────

def send_reminder(group_data, idx, total):
    name    = group_data.get('whatsapp_group', '')
    img     = group_data.get('image', '')
    count   = group_data.get('record_count', 0)
    markets = group_data.get('markets', [])
    dms     = group_data.get('dms', [])

    print(f"\n[{idx}/{total}] {name}")
    print(f"  Markets : {', '.join(markets)}")
    print(f"  Records : {count}")

    caption = format_caption(group_data)
    
    # Show which DMs will be tagged
    tagged = [dm.get('dmNameRep') for dm in dms if dm.get('dmNameRep') and dm.get('dmNameRep') != '-' and dm.get('dmNameRep') != 'null']
    if tagged:
        clean_tags = [t.replace('~', '').strip() for t in tagged]
        print(f"  Tagging in caption: {', '.join(clean_tags)}")

    # Open personal chat
    open_chat(YOUR_NUMBER)
    time.sleep(1.0)

    # Focus WhatsApp again before sending
    focus_whatsapp()
    time.sleep(0.5)

    # Send image with caption
    if img and os.path.exists(img):
        print(f"  📎 Sending image + caption...")
        copy_image(img)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(3.0)
        copy_text(caption)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.0)
        pyautogui.press('enter')
        time.sleep(3.0)
        print(f"  ✅ Image + caption sent")
    else:
        print(f"  ⚠️  No image — sending text only")
        copy_text(caption)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.0)
        pyautogui.press('enter')
        time.sleep(2.0)

    print(f"  ✅ Done")

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 2 TEST — Send to Personal Number (FOCUS FIX)")
    print("=" * 60)
    print(f"\n📱 Sending ALL reminders to: +{YOUR_NUMBER}")

    if not os.path.exists(METADATA_FILE):
        print(f"\n❌ Metadata not found. Run STEP1 first!")
        input("\nPress Enter to exit...")
        return

    with open(METADATA_FILE) as f:
        group_list = json.load(f)

    total = len(group_list)
    print(f"✅ Loaded {total} groups\n")

    missing = sum(1 for g in group_list if g.get('image') and not os.path.exists(g['image']))
    if missing:
        print(f"⚠️  {missing} image(s) missing\n")

    print("─" * 60)
    print("INSTRUCTIONS:")
    print("  1. Make sure WhatsApp Desktop is OPEN and MAXIMIZED")
    print("  2. Press Enter below")
    print("  3. You have 5 seconds to CLICK on WhatsApp Desktop")
    print("  4. Keep hands off mouse and keyboard")
    print("  5. Move mouse to TOP-LEFT corner at any time to stop")
    print("─" * 60)
    input("\nPress Enter to start...")

    # Countdown — user clicks WhatsApp during this time
    print("\nClick on WhatsApp Desktop NOW!")
    for i in range(5, 0, -1):
        print(f"  Starting in {i}...", end="\r")
        time.sleep(1)
    print("\n\nGO!\n")

    ok = fail = 0

    # Test with first 2 groups only
    test_groups = group_list[:2]
    print(f"🧪 Testing with first {len(test_groups)} groups\n")
    
    for idx, group in enumerate(test_groups, 1):
        try:
            send_reminder(group, idx, len(test_groups))
            ok += 1
            time.sleep(3.0)

        except pyautogui.FailSafeException:
            print("\n🛑 Stopped by user (mouse moved to corner)")
            break
        except KeyboardInterrupt:
            print("\n🛑 Stopped by Ctrl+C")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback; traceback.print_exc()
            fail += 1
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"✅ Sent   : {ok}")
    print(f"❌ Failed : {fail}")
    print(f"Total     : {len(test_groups)}")
    print("=" * 60)
    print(f"\n📱 Check WhatsApp on +{YOUR_NUMBER}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()