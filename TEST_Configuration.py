"""
=====================================================================
  STEP 2 — TEST SEND TO PERSONAL NUMBER  (v5)

  Sends image + caption as ONE message to your personal number.
  No manual coordinate calibration needed — finds WhatsApp window
  automatically and clicks relative to it.

  Run STEP1 first, then this script.
=====================================================================
"""

import pyautogui
import pyperclip
import time
import os
import json
import win32clipboard
import win32con
import win32gui
import win32con as wcon

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
METADATA_FILE = os.path.join(OUTPUT_FOLDER, "_group_list.json")

TEST_PHONE = "+92 310 8486366"

pyautogui.PAUSE    = 0.3
pyautogui.FAILSAFE = False

DELAY_SEARCH_OPEN    = 0.6
DELAY_GROUP_SELECT   = 2.0
DELAY_AFTER_OPEN     = 1.5
DELAY_BETWEEN_GROUPS = 4.0

# ─────────────────────────────────────────────────────────────
#  WHATSAPP WINDOW HELPERS
# ─────────────────────────────────────────────────────────────

def get_whatsapp_window():
    """Find the WhatsApp Desktop window and return its rect (left, top, right, bottom)."""
    hwnd = None

    def callback(h, _):
        nonlocal hwnd
        title = win32gui.GetWindowText(h)
        if 'WhatsApp' in title and win32gui.IsWindowVisible(h):
            hwnd = h
    
    win32gui.EnumWindows(callback, None)
    
    if hwnd is None:
        raise RuntimeError("WhatsApp window not found! Make sure WhatsApp Desktop is open.")
    
    rect = win32gui.GetWindowRect(hwnd)   # (left, top, right, bottom)
    return hwnd, rect


def bring_whatsapp_to_front():
    """Bring WhatsApp window to foreground."""
    try:
        hwnd, rect = get_whatsapp_window()
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        return rect
    except Exception as e:
        print(f"    ⚠️  Could not bring WhatsApp to front: {e}")
        return None


def get_input_coords():
    """
    Get the WhatsApp message input box coordinates automatically.
    The input box is always near the bottom-center of the WhatsApp window.
    No manual measurement needed.
    """
    try:
        _, rect = get_whatsapp_window()
        left, top, right, bottom = rect
        win_width  = right - left
        win_height = bottom - top
        
        # Input box is horizontally centered, ~40px above the window bottom
        x = left + win_width // 2
        y = bottom - 40
        return x, y
    except:
        # Fallback to screen-based coords if window detection fails
        w, h = pyautogui.size()
        return w // 2, h - 60


def focus_input(retries=4, delay=0.4):
    """Click the WhatsApp input bar to ensure it has focus."""
    x, y = get_input_coords()
    for _ in range(retries):
        pyautogui.click(x, y)
        time.sleep(delay)


# ─────────────────────────────────────────────────────────────
#  SEARCH & OPEN CHAT
# ─────────────────────────────────────────────────────────────

def search_contact(phone_or_name):
    """Open a WhatsApp chat by searching for a number using Ctrl+F."""
    print(f"    Searching: {phone_or_name}")

    bring_whatsapp_to_front()
    time.sleep(DELAY_SEARCH_OPEN)

    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.7)

    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyperclip.copy(phone_or_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.7)

    pyautogui.press('down')
    time.sleep(DELAY_GROUP_SELECT)

    pyautogui.press('return')
    time.sleep(DELAY_AFTER_OPEN)

    pyautogui.press('escape')
    time.sleep(0.8)

    return True


# ─────────────────────────────────────────────────────────────
#  CLIPBOARD
# ─────────────────────────────────────────────────────────────

def write_image_to_clipboard(image_path):
    """Write PNG/JPG as CF_DIB bitmap to Windows clipboard."""
    from PIL import Image
    import io

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    buf = io.BytesIO()
    img.save(buf, format='BMP')
    dib = buf.getvalue()[14:]
    buf.close()

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, dib)
    finally:
        win32clipboard.CloseClipboard()


# ─────────────────────────────────────────────────────────────
#  FORMAT CAPTION
# ─────────────────────────────────────────────────────────────

def format_caption(group_data):
    dms = group_data.get('dms', [])
    tag_lines = [f"@{dm['name'].strip()}" for dm in dms if dm.get('name', '').strip()]
    tag_block = "\n".join(tag_lines)
    if tag_block:
        tag_block += "\n"

    return (
        f"{tag_block}"
        "  🚨 URGENT REMINDER 🚨\n\n"
        "Important reminder that the RMA, XBM & TRADE-IN shipments listed are still pending and are approaching the deadline ⏳\n\n"
        "⚠️ Delayed shipment may result in chargebacks, so we kindly request you to prioritize shipping these devices as soon as possible 🚚📦\n\n"
        "If you need any support, clarification, or assistance, please feel free to reach out — we're here to help 🤝\n\n"
        "✨"
    )


# ─────────────────────────────────────────────────────────────
#  SEND IMAGE + CAPTION AS ONE MESSAGE
# ─────────────────────────────────────────────────────────────

def send_image_with_caption(image_path, caption_text):
    """
    Send image + caption as a single WhatsApp message.

    Flow:
      1. Focus input box (coords auto-detected from WhatsApp window)
      2. Write bitmap to clipboard
      3. Ctrl+V → WhatsApp image preview dialog opens
      4. Caption field in the dialog is auto-focused → paste caption
      5. Enter → sends image with caption as one message
    """
    if not os.path.exists(image_path):
        print(f"      ❌ Image not found: {image_path}")
        return False

    print(f"      Image: {os.path.basename(image_path)}")

    # 1. Bring WhatsApp to front and focus input
    bring_whatsapp_to_front()
    focus_input(retries=3, delay=0.4)

    # 2. Write image to clipboard
    try:
        write_image_to_clipboard(image_path)
    except Exception as e:
        print(f"      ❌ Clipboard error: {e}")
        return False

    time.sleep(0.5)

    # 3. Re-focus input (clipboard write can shift focus)
    focus_input(retries=2, delay=0.35)

    # 4. Paste → image preview dialog opens
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3.0)     # wait for preview dialog to render

    # 5. Caption field in preview dialog is now focused — paste caption
    pyperclip.copy(caption_text)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.6)

    # 6. Send
    pyautogui.press('return')
    time.sleep(3.0)

    print(f"      ✅ Sent")
    return True


# ─────────────────────────────────────────────────────────────
#  PROCESS ONE GROUP
# ─────────────────────────────────────────────────────────────

def send_group_test(group_data, group_number):
    whatsapp_group = group_data.get('whatsapp_group')
    image_path     = group_data.get('image')
    record_count   = group_data.get('record_count', 0)
    dms            = group_data.get('dms', [])
    markets        = group_data.get('markets', [])

    print(f"\n{'─'*60}")
    print(f"[{group_number}] {whatsapp_group}")
    print(f"Markets : {', '.join(markets)}")
    print(f"Records : {record_count}  |  DMs: {len(dms)}")
    print(f"{'─'*60}")

    caption = format_caption(group_data)

    print(f"\n  Opening chat...")
    if not search_contact(TEST_PHONE):
        print(f"  ❌ Could not open chat")
        return False

    time.sleep(1.0)

    print(f"  Sending image + caption...")
    if image_path and os.path.exists(image_path):
        result = send_image_with_caption(image_path, caption)
    else:
        # No image — send caption as plain text fallback
        print(f"  ⚠️  No image — sending caption as text only")
        bring_whatsapp_to_front()
        focus_input(retries=3, delay=0.4)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.15)
        pyautogui.press('delete')
        time.sleep(0.15)
        pyperclip.copy(caption)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.6)
        pyautogui.press('return')
        time.sleep(2.0)
        result = True

    print(f"  {'✅ Done' if result else '❌ Failed'}")
    return result


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  STEP 2 (TEST) — Send Reminders to Personal Number  [v5]")
    print("=" * 70)
    print(f"\n📱 Test number : {TEST_PHONE}")

    # Verify WhatsApp is open before doing anything
    try:
        _, rect = get_whatsapp_window()
        left, top, right, bottom = rect
        print(f"✅  WhatsApp window found at ({left}, {top}, {right}, {bottom})")
        print(f"   Input box will click at: {get_input_coords()}")
    except RuntimeError as e:
        print(f"\n❌ {e}")
        input("\nPress Enter to exit...")
        return

    if not os.path.exists(METADATA_FILE):
        print(f"\n❌ Metadata not found:\n   {METADATA_FILE}")
        print("   Run STEP1 first!")
        input("\nPress Enter to exit...")
        return

    with open(METADATA_FILE, 'r') as f:
        group_list = json.load(f)

    print(f"\nLoaded {len(group_list)} groups")

    missing = sum(1 for g in group_list if g.get('image') and not os.path.exists(g['image']))
    if missing:
        print(f"⚠️  {missing} image(s) missing")

    print("""
─────────────────────────────────────────────────────────────
  DO NOT touch mouse or keyboard while the script runs.
  Ctrl+C to abort at any time.
─────────────────────────────────────────────────────────────""")
    input("\nPress Enter to start...")

    ok = fail = 0

    for idx, group_data in enumerate(group_list, 1):
        try:
            if send_group_test(group_data, idx):
                ok += 1
            else:
                fail += 1
            time.sleep(DELAY_BETWEEN_GROUPS)

        except KeyboardInterrupt:
            print("\n\n⚠️  Aborted by user")
            break
        except Exception as e:
            print(f"\n❌ Error on group {idx}: {e}")
            import traceback; traceback.print_exc()
            fail += 1
            time.sleep(3)

    print("\n" + "=" * 70)
    print(f"✅ Sent   : {ok}")
    print(f"❌ Failed : {fail}")
    print(f"Total     : {len(group_list)}")
    print("=" * 70)
    print(f"\n📱 Check WhatsApp on {TEST_PHONE}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal: {e}")
        import traceback; traceback.print_exc()
        input("\nPress Enter to exit...")