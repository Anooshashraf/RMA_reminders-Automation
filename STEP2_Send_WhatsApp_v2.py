# """
# =====================================================================
#   STEP 2 — SEND WHATSAPP MESSAGES
#   RMA / XBM / Trade-in Pending Shipments
  
#   UPDATED: Sends to WhatsApp groups with proper DM tagging
  
#   HOW IT WORKS:
#   - Reads group metadata from _group_list.json
#   - Handles different send modes:
#     * tag_all_dms: Sends to group and tags each DM
#     * send_to_group: Just sends screenshot
#     * send_to_both_groups: Sends to multiple groups (Dallas, etc)
#   - Opens WhatsApp Desktop and sends via chat interface
  
#   IMPORTANT: Keep WhatsApp Desktop open!
#   Run STEP 1 first, then this script.
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

# pyautogui.FAILSAFE = True      # move mouse to top-left corner to stop
# pyautogui.PAUSE    = 0.5

# # ─────────────────────────────────────────────────────────────
# #  CLIPBOARD HELPERS
# # ─────────────────────────────────────────────────────────────

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

# def open_chat(group_name):
#     """Search for and open a WhatsApp group by name."""
#     # Open search bar
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)

#     # Clear whatever is in the search box
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.5)
#     pyautogui.press('backspace')
#     time.sleep(0.5)

#     # Type the group name via clipboard
#     copy_text(group_name)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.5)

#     # Press Tab to move focus to the search results list
#     pyautogui.press('tab')
#     time.sleep(0.5)

#     # Press Down arrow to select the first result
#     pyautogui.press('down')
#     time.sleep(0.5)

#     # Press Enter to open the selected chat
#     pyautogui.press('enter')
#     time.sleep(2.0)

#     # Close search with Escape (after opening the chat)
#     pyautogui.press('escape')
#     time.sleep(0.5)

# # ─────────────────────────────────────────────────────────────
# #  SEND ONE GROUP REMINDER
# #  Image sent FIRST (with caption in preview dialog)
# # ─────────────────────────────────────────────────────────────

# def send_reminder(group_data, idx, total):
#     name    = group_data.get('whatsapp_group', '')
#     img     = group_data.get('image', '')
#     count   = group_data.get('record_count', 0)
#     markets = group_data.get('markets', [])
#     send_mode = group_data.get('send_mode', 'send_to_group')

#     print(f"\n[{idx}/{total}] {name}")
#     print(f"  Mode    : {send_mode}")
#     print(f"  Markets : {', '.join(markets)}")
#     print(f"  Records : {count}")

#     caption = format_caption(group_data)
    
#     # Show which DMs will be tagged
#     dms = group_data.get('dms', [])
#     tagged = [dm.get('dmNameRep') for dm in dms if dm.get('dmNameRep') and dm.get('dmNameRep') != '-' and dm.get('dmNameRep') != 'null']
#     if tagged:
#         print(f"  Tagging : {', '.join(tagged)}")
#     else:
#         print(f"  Tagging : None")

#     # ── Handle different send modes ──────────────────────────
    
#     if send_mode == "send_to_both_groups":
#         # Dallas mode - send to both groups
#         groups_to_send = ["Dallas Team South", "Dallas Team North"]
#         print(f"  📌 Sending to both Dallas groups")
        
#         for target_group in groups_to_send:
#             print(f"\n    → Opening: {target_group}")
#             open_chat(target_group)
#             time.sleep(1.0)
            
#             if img and os.path.exists(img):
#                 copy_image(img)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(3.0)
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(1.0)
#                 pyautogui.press('enter')
#                 time.sleep(3.0)
#             else:
#                 print(f"  ⚠️  No image — sending text only")
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(1.0)
#                 pyautogui.press('enter')
#                 time.sleep(2.0)
            
#             print(f"    ✅ Sent to {target_group}")
#             time.sleep(2.0)
        
#         print(f"  ✅ Completed both groups")
#         return True
    
#     else:
#         # Normal mode - send to single group
#         open_chat(name)
#         time.sleep(1.0)

#         if img and os.path.exists(img):
#             # ── send image with caption ──────────────────────
#             copy_image(img)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(3.0)
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
#             pyautogui.press('enter')
#             time.sleep(3.0)
#         else:
#             # ── no image: send caption as plain text ──────────
#             print(f"  ⚠️  No image — sending text only")
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
#             pyautogui.press('enter')
#             time.sleep(2.0)

#         print(f"  ✅ Sent")
#         return True

# # ─────────────────────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────────────────────

# def main():
#     print("=" * 60)
#     print("  STEP 2 — Send WhatsApp Messages to Groups")
#     print("=" * 60)

#     if not os.path.exists(METADATA_FILE):
#         print(f"\n❌ Metadata not found. Run STEP1 first!")
#         input("\nPress Enter to exit...")
#         return

#     with open(METADATA_FILE) as f:
#         group_list = json.load(f)

#     total = len(group_list)
#     print(f"\n📊 Loaded {total} groups\n")

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
#             time.sleep(3.0)

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
#     print(f"\n📱 Check WhatsApp groups for messages")
#     input("\nPress Enter to exit...")


# if __name__ == "__main__":
#     main()




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

pyautogui.FAILSAFE = True      # move mouse to top-left corner to stop
pyautogui.PAUSE    = 0.5

# ─────────────────────────────────────────────────────────────
#  CLIPBOARD HELPERS
# ─────────────────────────────────────────────────────────────

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
    
    # Build tag lines using dmNameRep
    tag_lines = []
    for dm in dms:
        rep_name = dm.get('dmNameRep')
        # Only tag if dmNameRep exists and is not None/null/empty/dash
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

def open_chat(group_name):
    """
    Search for and open a WhatsApp group by name.
    Uses Escape to filter the chat list, then selects the first result.
    This ensures we open the exact match.
    """
    # Open search bar
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)

    # Clear whatever is in the search box
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('backspace')
    time.sleep(0.5)

    # Type the group name via clipboard
    copy_text(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)


    # The chat list is now filtered to show only matching groups
    # Press Down to select the first filtered result
    pyautogui.press('down')
    time.sleep(0.5)

    # Press Enter to open the selected chat
    pyautogui.press('enter')
    time.sleep(2.0)


def click_input():
    """Click on the message input box to focus it."""
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height - 40)
    time.sleep(0.4)
    pyautogui.click(screen_width // 2, screen_height - 40)
    time.sleep(0.3)
    
def type_real_tag(dm_name_rep):
    """
    Type a real @mention that notifies the person.
    Uses the full cleaned name (without spaces) to trigger the suggestion popup.
    """
    if not dm_name_rep or str(dm_name_rep).strip() in ['', '-', 'null', 'None']:
        return

    # Clean the name: remove ~ prefix and extra spaces
    clean = dm_name_rep.strip().lstrip('~').strip()
    if not clean:
        return

    print(f"      Tagging @{clean}")

    # Click on the input box to focus it
    click_input()

    # Type @
    pyautogui.write('@', interval=0.05)
    time.sleep(0.8)  # Wait for popup to appear

    # Type the first 4 characters of the cleaned name (without spaces)
    # This is enough to trigger the correct suggestion in most cases
    search_chars = clean.replace(' ', '')[:4]
    for char in search_chars:
        pyautogui.write(char, interval=0.08)
    time.sleep(1.2)  # Wait for suggestions to filter

    # Press Down arrow to select the first suggestion (which should be the correct match)
    pyautogui.press('down')
    time.sleep(0.3)

    # Press Enter to insert the mention
    pyautogui.press('enter')
    time.sleep(0.5)
# ─────────────────────────────────────────────────────────────
#  SEND ONE GROUP REMINDER
#  Image sent FIRST (with caption in preview dialog)
#  Then a second message with real @mention tags
# ─────────────────────────────────────────────────────────────

def send_reminder(group_data, idx, total):
    name    = group_data.get('whatsapp_group', '')
    img     = group_data.get('image', '')
    count   = group_data.get('record_count', 0)
    markets = group_data.get('markets', [])
    send_mode = group_data.get('send_mode', 'send_to_group')
    dms     = group_data.get('dms', [])

    print(f"\n[{idx}/{total}] {name}")
    print(f"  Mode    : {send_mode}")
    print(f"  Markets : {', '.join(markets)}")
    print(f"  Records : {count}")

    caption = format_caption(group_data)
    
    # Show which DMs will be tagged
    tagged = [dm.get('dmNameRep') for dm in dms if dm.get('dmNameRep') and dm.get('dmNameRep') != '-' and dm.get('dmNameRep') != 'null']
    if tagged:
        # Clean tags for display (remove ~)
        clean_tags = [t.replace('~', '') for t in tagged]
        print(f"  Tagging : {', '.join(clean_tags)}")
    else:
        print(f"  Tagging : None")

    # ── Handle different send modes ──────────────────────────
    
    if send_mode == "send_to_both_groups":
        # Dallas mode - send to both groups
        groups_to_send = ["Dallas Team South", "Dallas Team North"]
        print(f"  📌 Sending to both Dallas groups")
        
        for target_group in groups_to_send:
            print(f"\n    → Opening: {target_group}")
            open_chat(target_group)
            time.sleep(1.0)
            
            # 1. Send image + caption (combined message)
            if img and os.path.exists(img):
                click_input()
                copy_image(img)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(3.0)
                copy_text(caption)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1.0)
                pyautogui.press('enter')
                time.sleep(3.0)
                print(f"    Image + caption sent to {target_group}")
            else:
                print(f"  ⚠️  No image — sending text only")
                click_input()
                copy_text(caption)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1.0)
                pyautogui.press('enter')
                time.sleep(2.0)

            # 2. Send real @mention tags as a separate message
            if tagged:
                click_input()
                time.sleep(0.3)
                for dm in dms:
                    rep_name = dm.get('dmNameRep')
                    if rep_name and rep_name != '-' and rep_name != 'null':
                        type_real_tag(rep_name)
                        pyautogui.hotkey('shift', 'enter')
                        time.sleep(0.3)
                pyautogui.press('enter')
                time.sleep(2.0)
                print(f"    Real @mention tags sent to {target_group}")
            
            print(f"  ✅ Done: {target_group}")
            time.sleep(2.0)
        
        print(f"  ✅ Completed both groups")
        return True
    
    else:
        # Normal mode - send to single group
        open_chat(name)
        time.sleep(1.0)

        # 1. Send image + caption (combined message)
        if img and os.path.exists(img):
            click_input()
            copy_image(img)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(3.0)
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)
            pyautogui.press('enter')
            time.sleep(3.0)
        else:
            print(f"  ⚠️  No image — sending text only")
            click_input()
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)
            pyautogui.press('enter')
            time.sleep(2.0)

        # 2. Send real @mention tags as a separate message
        if tagged:
            click_input()
            time.sleep(0.3)
            for dm in dms:
                rep_name = dm.get('dmNameRep')
                if rep_name and rep_name != '-' and rep_name != 'null':
                    type_real_tag(rep_name)
                    pyautogui.hotkey('shift', 'enter')
                    time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(2.0)
            print(f"    Real @mention tags sent")

        print(f"  ✅ Sent")
        return True

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 2 — Send WhatsApp Messages to Groups")
    print("=" * 60)

    if not os.path.exists(METADATA_FILE):
        print(f"\n❌ Metadata not found. Run STEP1 first!")
        input("\nPress Enter to exit...")
        return

    with open(METADATA_FILE) as f:
        group_list = json.load(f)

    total = len(group_list)
    print(f"\n📊 Loaded {total} groups\n")

    missing = sum(1 for g in group_list if g.get('image') and not os.path.exists(g['image']))
    if missing:
        print(f"⚠️  {missing} image(s) missing\n")

    print("─" * 60)
    print("INSTRUCTIONS:")
    print("  1. Make sure WhatsApp Desktop is OPEN")
    print("  2. Press Enter below")
    print("  3. You have 5 seconds to CLICK on WhatsApp Desktop")
    print("  4. Then keep hands off mouse and keyboard")
    print("  5. Move mouse to TOP-LEFT corner at any time to stop")
    print("─" * 60)
    input("\nPress Enter to start...")

    print("\nClick on WhatsApp Desktop NOW!")
    for i in range(5, 0, -1):
        print(f"  Starting in {i}...", end="\r")
        time.sleep(1)
    print("\n\nGO!\n")

    ok = fail = 0

    for idx, group in enumerate(group_list, 1):
        try:
            send_reminder(group, idx, total)
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
    print(f"Total     : {total}")
    print("=" * 60)
    print(f"\n📱 Check WhatsApp groups for messages")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()