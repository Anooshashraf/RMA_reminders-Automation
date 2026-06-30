


"""
=====================================================================
  STEP 2 — SEND WHATSAPP MESSAGES (WITH RESUME)
  RMA / XBM / Trade-in Pending Shipments
  
  FEATURES:
  - Verified @mention tagging
  - Resume from any group number
  - Auto-saves progress
  - Test mode support
  
  IMPORTANT: Keep WhatsApp Desktop MAXIMIZED!
=====================================================================
"""

import pyautogui
import pyperclip
import time
import os
import json
import re
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
PROGRESS_FILE = os.path.join(OUTPUT_FOLDER, "_send_progress.json")

# ⚠️ RESUME SETTINGS
START_FROM = 1        # Change this to resume from a specific group number
TEST_MODE = False      # True = send to your number, False = send to groups
YOUR_NUMBER = "923108486366"

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.3

# ─────────────────────────────────────────────────────────────
#  PROGRESS TRACKING
# ─────────────────────────────────────────────────────────────

def load_progress():
    """Load saved progress"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"last_completed": 0, "failed_groups": []}


def save_progress(completed_idx):
    """Save progress after each successful send"""
    progress = {
        "last_completed": completed_idx,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


# ─────────────────────────────────────────────────────────────
#  CLIPBOARD
# ─────────────────────────────────────────────────────────────

def copy_text(text):
    pyperclip.copy(text)
    time.sleep(0.3)

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

# ─────────────────────────────────────────────────────────────
#  FORMAT CAPTION
# ─────────────────────────────────────────────────────────────

def format_caption():
    return (
        "🚨 URGENT REMINDER 🚨\n\n"
        "Important reminder that the RMA, XBM & TRADE-IN shipments "
        "listed are still pending and are approaching the deadline ⏳\n\n"
        "⚠️ Delayed shipment may result in chargebacks, so we kindly "
        "request you to prioritize shipping these devices as soon as "
        "possible 🚚📦\n\n"
        "If you need any support, clarification, or assistance, please "
        "feel free to reach out — we're here to help 🤝\n\n"
        "✨"
    )

# ─────────────────────────────────────────────────────────────
#  OPEN GROUP
# ─────────────────────────────────────────────────────────────

def open_group(group_name):
    """Open a WhatsApp group by searching for it"""
    print(f"  🔍 Opening: {group_name}")
    
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    copy_text(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    
    time.sleep(1.0)
    
    pyautogui.press('down')
    time.sleep(0.5)
    
    pyautogui.press('enter')
    time.sleep(3.0)
    
    print(f"  ✅ Opened: {group_name}")


# ─────────────────────────────────────────────────────────────
#  MENTION TAGGING
# ─────────────────────────────────────────────────────────────

def extract_last4(phone):
    """Extract last 4 digits from phone number"""
    if not phone:
        return None
    digits = re.sub(r'[^\d]', '', str(phone))
    return digits[-4:] if len(digits) >= 4 else None


# def type_verified_mention(dm):
#     """
#     Type a verified @mention tag.
#     Handles names with spaces by typing incrementally.
#     """
#     dm_name = dm.get('dmNameRep', '')
#     phone = dm.get('phone', '')
    
#     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
#         return False
    
#     clean_name = dm_name.strip().lstrip('~').strip()
#     if not clean_name:
#         return False
    
#     target_last4 = extract_last4(phone)
    
#     print(f"      Tagging: @{clean_name}", end="")
#     if target_last4:
#         print(f" (📱{target_last4})", end="")
#     print()
    
#     try:
#         # Step 1: Type @ to trigger popup
#         pyautogui.write('@', interval=0.05)
#         time.sleep(1.5)
        
#         # Step 2: Handle names with spaces
#         if ' ' in clean_name:
#             words = clean_name.split()
#             first_word = words[0]
#             pyautogui.write(first_word, interval=0.05)
#             time.sleep(1.0)
            
#             for word in words[1:]:
#                 pyautogui.write(' ', interval=0.05)
#                 time.sleep(0.3)
#                 pyautogui.write(word, interval=0.05)
#                 time.sleep(0.8)
            
#             time.sleep(1.5)
#         else:
#             pyautogui.write(clean_name, interval=0.05)
#             time.sleep(2.0)
        
#         # Step 3: Press Down to select first suggestion
#         pprint(f"        Pressing Tab to insert...")
#         pyautogui.press('tab')
#         time.sleep(0.5)
        
#         print(f"        ✅ Mention inserted: @{clean_name}")
#         return True
        
#     except Exception as e:
#         print(f"        ❌ Failed: {e}")
#         return False


# def type_verified_mention(dm):
#     """
#     Type a verified @mention tag.
    
#     HANDLES NAMES WITH SPACES:
#     - "Ayan Budhwani" -> types "Ayan" first, then continues with "Budhwani"
#     - "HAMED ALI SUFI" -> types "HAMED" first, waits for popup, continues
    
#     WhatsApp filters suggestions as you type, so typing incrementally works.
#     """
#     dm_name = dm.get('dmNameRep', '')
#     phone = dm.get('phone', '')
    
#     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
#         return False
    
#     clean_name = dm_name.strip().lstrip('~').strip()
#     if not clean_name:
#         return False
    
#     target_last4 = extract_last4(phone)
    
#     print(f"      Tagging: @{clean_name}", end="")
#     if target_last4:
#         print(f" (📱{target_last4})", end="")
#     print()
    
#     try:
#         # Step 1: Type @ to trigger popup
#         pyautogui.write('@', interval=0.05)
#         time.sleep(1.5)  # Wait for popup to appear
#         print(f"        @ typed, popup should appear")
        
#         # Step 2: Handle names with spaces
#         if ' ' in clean_name:
#             # Split name into words
#             words = clean_name.split()
#             print(f"        Multi-word name: {words}")
            
#             # Type first word
#             first_word = words[0]
#             print(f"        Typing first word: '{first_word}'")
#             pyautogui.write(first_word, interval=0.05)
#             time.sleep(1.0)  # Wait for initial filter
            
#             # Type remaining words one by one
#             for word in words[1:]:
#                 # Add space
#                 pyautogui.write(' ', interval=0.05)
#                 time.sleep(0.3)
#                 # Type the word
#                 print(f"        Typing: '{word}'")
#                 pyautogui.write(word, interval=0.05)
#                 time.sleep(0.8)  # Wait for filter to update
            
#             # Final wait for suggestions to settle
#             time.sleep(1.5)
#         else:
#             # Single word name - type all at once
#             print(f"        Single word: '{clean_name}'")
#             pyautogui.write(clean_name, interval=0.05)
#             time.sleep(2.0)  # Wait for suggestions
        
#         # Step 3: Select first suggestion with Down arrow
#         # print(f"        Pressing Down to select...")
#         # pyautogui.press('down')
#         # time.sleep(0.5)
        
#         # Step 4: Press TAB to insert the clickable mention
#         print(f"        Pressing Tab to insert...")
#         pyautogui.press('enter')  # Using Enter instead of Tab for better reliability
#         time.sleep(0.5)
        
#         print(f"        ✅ Mention inserted: @{clean_name}")
#         return True
        
#     except Exception as e:
#         print(f"        ❌ Failed: {e}")
#         return False



def type_verified_mention(dm):
    """
    Type a verified @mention tag.
    Uses Tab to insert WITHOUT sending.
    """
    dm_name = dm.get('dmNameRep', '')
    phone = dm.get('phone', '')
    
    if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
        return False
    
    clean_name = dm_name.strip().lstrip('~').strip()
    if not clean_name:
        return False
    
    target_last4 = extract_last4(phone)
    
    print(f"      Tagging: @{clean_name}", end="")
    if target_last4:
        print(f" (📱{target_last4})", end="")
    print()
    
    try:
        # Type @ to trigger popup
        pyautogui.write('@', interval=0.05)
        time.sleep(1.5)
        
        # Handle names with spaces
        if ' ' in clean_name:
            words = clean_name.split()
            pyautogui.write(words[0], interval=0.05)
            time.sleep(1.0)
            for word in words[1:]:
                pyautogui.write(' ', interval=0.05)
                time.sleep(0.3)
                pyautogui.write(word, interval=0.05)
                time.sleep(0.8)
            time.sleep(1.5)
        else:
            pyautogui.write(clean_name, interval=0.05)
            time.sleep(2.0)
        
        # Press Tab to insert mention (DOES NOT SEND)
        pyautogui.press('tab')
        time.sleep(0.5)
        
        print(f"        ✅ Mention inserted: @{clean_name}")
        return True
        
    except Exception as e:
        print(f"        ❌ Failed: {e}")
        return False



# ─────────────────────────────────────────────────────────────
#  SEND ONE GROUP
# ─────────────────────────────────────────────────────────────

def send_reminder(group_data, idx, total):
    name      = group_data.get('whatsapp_group', '')
    img       = group_data.get('image', '')
    count     = group_data.get('record_count', 0)
    markets   = group_data.get('markets', [])
    send_mode = group_data.get('send_mode', 'send_to_group')
    dms       = group_data.get('dms', [])

    print(f"\n{'─'*55}")
    print(f"[{idx}/{total}] {name}  ({count} records)")
    print(f"  Mode: {send_mode} | Markets: {', '.join(markets)}")

    caption = format_caption()
    
    tagged_dms = [
        d for d in dms
        if d.get('dmNameRep') and str(d.get('dmNameRep')).strip() not in ['','-','null','None']
    ]
    
    if tagged_dms:
        names = [d['dmNameRep'] for d in tagged_dms]
        print(f"  Tagging: {', '.join(names)}")
    else:
        print(f"  No DMs to tag")

    if TEST_MODE:
        targets = [YOUR_NUMBER]
    elif send_mode == "send_to_both_groups":
        targets = ["Dallas Team South", "Dallas Team North"]
    else:
        targets = [name]

    for target in targets:
        print(f"\n  → Processing: {target}")
        
        open_group(target)
        time.sleep(1.0)
        
        # Click on the message input box to ensure focus
        w, h = pyautogui.size()
        pyautogui.click(w // 2, h - 100)  # Click near bottom where input box is
        time.sleep(0.5)
        
        if img and os.path.exists(img):
            print(f"    📎 Sending image...")
            
            copy_image(img)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(3.0)
            
            if tagged_dms:
                print(f"    👥 Adding verified mentions...")
                for i, dm in enumerate(tagged_dms):
                    type_verified_mention(dm)
                    # WhatsApp auto-adds space after Tab-inserted mention
                    time.sleep(0.5)
                
                # Add line break after all mentions
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.2)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.2)
            
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)
            
            pyautogui.press('enter')
            time.sleep(3.0)
            print(f"    ✅ Image + mentions + caption sent")
        else:
            print(f"    📝 No image - text only")
            
            if tagged_dms:
                print(f"    👥 Adding verified mentions...")
                for i, dm in enumerate(tagged_dms):
                    type_verified_mention(dm)
                    time.sleep(0.5)
                
                # Add line break after all mentions
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.2)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.2)
            
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
            pyautogui.press('enter')
            time.sleep(2.0)
            print(f"    ✅ Mentions + caption sent")
        
        print(f"  ✅ Done: {target}")
        time.sleep(2.0)
    
    save_progress(idx)
    return True

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 2 — Send WhatsApp Messages (with Resume)")
    print("=" * 60)

    if not os.path.exists(METADATA_FILE):
        print(f"\n❌ Metadata not found. Run STEP1 first!")
        input("\nPress Enter to exit...")
        return

    with open(METADATA_FILE) as f:
        group_list = json.load(f)

    total = len(group_list)
    
    # Load progress
    progress = load_progress()
    last_completed = progress.get("last_completed", 0)
    
    # Determine start point
    if START_FROM > 1:
        start_idx = START_FROM
        print(f"\n📊 {total} total groups — RESUMING from #{start_idx}")
    elif last_completed > 0 and last_completed < total:
        print(f"\n📊 {total} total groups")
        print(f"📌 Last completed: #{last_completed} on {progress.get('timestamp', 'unknown')}")
        resume = input(f"\nResume from #{last_completed + 1}? (y/n): ").strip().lower()
        if resume == 'y':
            start_idx = last_completed + 1
            print(f"✅ Resuming from #{start_idx}")
        else:
            start_idx = 1
            print(f"✅ Starting from #1 (progress reset)")
    else:
        start_idx = 1
        print(f"\n📊 {total} groups loaded")
    
    # Slice groups
    groups_to_send = group_list[start_idx - 1:]
    
    # Show what will be sent
    print(f"\n📋 Sending {len(groups_to_send)} groups:")
    for i, g in enumerate(groups_to_send[:5], start_idx):
        print(f"  {i}. {g['whatsapp_group']} ({g.get('record_count', 0)} records)")
    if len(groups_to_send) > 5:
        print(f"  ... and {len(groups_to_send) - 5} more")
    
    print(f"\n⚠️  Mode: {'🧪 TEST (to your number)' if TEST_MODE else '🚀 LIVE (actual groups)'}")
    
    # Check missing images
    missing = sum(1 for g in groups_to_send if g.get('image') and not os.path.exists(g['image']))
    if missing:
        print(f"⚠️  {missing} image(s) missing")

    print("\n" + "─" * 60)
    print("INSTRUCTIONS:")
    print("  1. Make sure WhatsApp Desktop is OPEN and MAXIMIZED")
    print("  2. Press Enter below")
    print("  3. You have 5 seconds to CLICK on WhatsApp Desktop")
    print("  4. Keep hands off mouse and keyboard")
    print("  5. Move mouse to TOP-LEFT corner at any time to stop")
    print("─" * 60)
    
    confirm = input(f"\nPress Enter to start (or 'q' to quit): ")
    if confirm.lower() == 'q':
        print("Cancelled.")
        return

    print("\nClick on WhatsApp Desktop NOW!")
    for i in range(5, 0, -1):
        print(f"  Starting in {i}...", end="\r")
        time.sleep(1)
    print("\n\nGO!\n")

    ok = fail = 0
    current_idx = start_idx

    for idx_offset, group in enumerate(groups_to_send):
        current_idx = start_idx + idx_offset
        
        try:
            send_reminder(group, current_idx, total)
            ok += 1
            time.sleep(3.0)

        except pyautogui.FailSafeException:
            print(f"\n🛑 ABORTED at group #{current_idx}")
            print(f"   To resume, set START_FROM = {current_idx} at top of script")
            save_progress(current_idx - 1)
            break
        except KeyboardInterrupt:
            print(f"\n🛑 ABORTED at group #{current_idx}")
            print(f"   To resume, set START_FROM = {current_idx} at top of script")
            save_progress(current_idx - 1)
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            fail += 1
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"✅ Sent   : {ok}")
    print(f"❌ Failed : {fail}")
    print(f"📊 From   : #{start_idx} to #{current_idx} of {total}")
    print(f"📱 Mode   : {'TEST' if TEST_MODE else 'LIVE'}")
    
    if current_idx <= total:
        print(f"\n💡 To resume later, set START_FROM = {current_idx}")
    
    print("=" * 60)
    print(f"\n📱 Check WhatsApp for messages!")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

