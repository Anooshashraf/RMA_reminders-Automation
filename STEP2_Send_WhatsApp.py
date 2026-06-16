# """
# =====================================================================
#   STEP 2 — SEND WHATSAPP MESSAGES
#   RMA / XBM / Trade-in Pending Shipments

#   Exact same logic as your senior's DSR WHATSAPP.py:
#   Ctrl+F → clear → paste group name → Down → Enter → send image

#   Run STEP 1 first, then this. Keep WhatsApp Desktop open!
# =====================================================================
# """

# import pyautogui
# import pyperclip
# import time
# import os
# import json

# # ─────────────────────────────────────────────────────────────
# #  CONFIGURATION
# # ─────────────────────────────────────────────────────────────

# OUTPUT_FOLDER   = r"C:\Users\User\Desktop\RMA_Screenshots"

# SENDER_NAME     = "HAMMAD ALI"
# SENDER_PHONE_PK = "+92 371 1128675"
# SENDER_PHONE_US = "+1 (213) 214-4337"

# # ── GROUP MAP ────────────────────────────────────────────────
# # Format: ("Market in Excel", "District in Excel"): "WhatsApp Group Name"
# # District can be "" or "-" if not applicable
# # These are built from YOUR screenshots

# GROUP_MAP = {

#     # ── MEMPHIS ──────────────────────────────────────────────
#     ("MEMPHIS", "North"):   "Memphis Team North",
#     ("MEMPHIS", "South"):   "Memphis Team South",
#     ("MEMPHIS", "Central"): "Memphis Team Central",
#     ("MEMPHIS", "-"):       "Memphis Team Central",   # fallback
#     ("MEMPHIS", ""):        "Memphis Team Central",

#     # ── HOUSTON ──────────────────────────────────────────────
#     ("HOUSTON", "South"):    "SOUTH DISTRICT - HOUSTON",
#     ("HOUSTON", "Central"):  "CENTRAL DISTRICT - HOUSTON",
#     ("HOUSTON", "Airline"):  "AIRLINE DISTRICT - HOUSTON",
#     ("HOUSTON", "North"):    "NORTH DISTRICT - HOUSTON",
#     ("HOUSTON", "East"):     "EAST DISTRICT - HOUSTON",
#     ("HOUSTON", "-"):        "CENTRAL DISTRICT - HOUSTON",  # fallback
#     ("HOUSTON", ""):         "CENTRAL DISTRICT - HOUSTON",

#     # ── ARIZONA ──────────────────────────────────────────────
#     ("ARIZONA", "East Valley"):         "ARIZONA SUPPORT",
#     ("ARIZONA", "Central /South Valley"): "ARIZONA SUPPORT",
#     ("ARIZONA", "West Valley"):         "ARIZONA SUPPORT",
#     ("ARIZONA", "-"):                   "ARIZONA SUPPORT",
#     ("ARIZONA", ""):                    "ARIZONA SUPPORT",

#     # ── LOS ANGELES ──────────────────────────────────────────
#     ("LOS ANGELES", "San Bernardino"):  "LOS ANGELES - San Bernardino",
#     ("LOS ANGELES", "North"):           "LOS ANGELES - NORTH",
#     ("LOS ANGELES", "East"):            "LOS ANGELES - EAST",
#     ("LOS ANGELES", "LA - Central"):    "LOS ANGELES - CENTRAL",
#     ("LOS ANGELES", "Central"):         "LOS ANGELES - CENTRAL",
#     ("LOS ANGELES", "-"):               "LOS ANGELES - NORTH",   # fallback
#     ("LOS ANGELES", ""):                "LOS ANGELES - NORTH",

#     # ── NASHVILLE ────────────────────────────────────────────
#     ("NASHVILLE", "-"):  "NASHVILLE - SUPPORT",
#     ("NASHVILLE", ""):   "NASHVILLE - SUPPORT",

#     # ── DALLAS ───────────────────────────────────────────────
#     ("DALLAS", "South"):  "Dallas Team South",
#     ("DALLAS", "North"):  "Dallas Team North",
#     ("DALLAS", "-"):      "Dallas Team South",   # fallback
#     ("DALLAS", ""):       "Dallas Team South",

#     # ── GEORGIA / ATLANTA ────────────────────────────────────
#     ("GEORGIA", "-"):  "Atlanta Team",
#     ("GEORGIA", ""):   "Atlanta Team",

#     # ── COLORADO / DENVER ────────────────────────────────────
#     ("COLORADO", "South"):   "Southside Denver",
#     ("COLORADO", "North"):   "Northside Denver",
#     ("COLORADO", "-"):       "Southside Denver",  # fallback
#     ("COLORADO", ""):        "Southside Denver",

#     # ── NORTH CAROLINA ───────────────────────────────────────
#     ("NORTH CAROL", "Raleigh East"):  "NC-Raleigh East",
#     ("NORTH CAROL", "Raleigh West"):  "NC- Raleigh West",
#     ("NORTH CAROL", "Durham"):        "NC- Durham",
#     ("NORTH CAROL", "-"):             "NC-Raleigh East",  # fallback
#     ("NORTH CAROL", ""):              "NC-Raleigh East",

#     # ── PHILADELPHIA ─────────────────────────────────────────
#     ("PHILLY", "-"):  "Philadelphia Support",
#     ("PHILLY", ""):   "Philadelphia Support",

#     # ── UTAH ─────────────────────────────────────────────────
#     ("UTAH", "-"):  "Utah Support",
#     ("UTAH", ""):   "Utah Support",

#     # ── SACRAMENTO ───────────────────────────────────────────
#     ("SACRAMENTO", "-"):  "Sacramento Main",
#     ("SACRAMENTO", ""):   "Sacramento Main",

#     # ── SAN DIEGO ────────────────────────────────────────────
#     ("SAN DIEGO", "-"):   "SAN DIEGO CORE",
#     ("SAN DIEGO", ""):    "SAN DIEGO CORE",

#     # ── SAN FRANCISCO / BAY AREA ─────────────────────────────
#     ("SAN FRANCISCO", "-"):  "San Francisco Core",
#     ("SAN FRANCISCO", ""):   "San Francisco Core",
#     ("BAY AREA", "Core"):    "Bay Area Core",
#     ("BAY AREA", "East"):    "East Bay Area",
#     ("BAY AREA", "-"):       "Bay Area Core",
#     ("BAY AREA", ""):        "Bay Area Core",

#     # ── PORTLAND / OREGON ────────────────────────────────────
#     ("PORTLAND", "-"):  "Portland Oregon Main",
#     ("PORTLAND", ""):   "Portland Oregon Main",

#     # ── OXNARD + PALMDALE (merged by STEP 1 into one DM entry) ─
#     # STEP 1 combines both under canonical name "OXNARD/PALMDALE"
#     ("OXNARD/PALMDALE", "Oxnard/Palmdale"): "Team Oxnard - Palmdale Core",
#     ("OXNARD/PALMDALE", "-"):               "Team Oxnard - Palmdale Core",
#     ("OXNARD/PALMDALE", ""):                "Team Oxnard - Palmdale Core",
#     # Fallback if encountered individually
#     ("OXNARD",   "Oxnard/Palmdale"): "Team Oxnard - Palmdale Core",
#     ("OXNARD",   "-"):               "Team Oxnard - Palmdale Core",
#     ("OXNARD",   ""):                "Team Oxnard - Palmdale Core",
#     ("PALMDALE", "Oxnard/Palmdale"): "Team Oxnard - Palmdale Core",
#     ("PALMDALE", "-"):               "Team Oxnard - Palmdale Core",
#     ("PALMDALE", ""):                "Team Oxnard - Palmdale Core",

#     # ── BOSTON / MAINE ───────────────────────────────────────
#     ("BOSTON", "-"):  "Boston-Maine",
#     ("BOSTON", ""):   "Boston-Maine",

#     # ── CHARLOTTE ────────────────────────────────────────────
#     ("CHARLOTTE", "-"):  "Charlotte-Support",
#     ("CHARLOTTE", ""):   "Charlotte-Support",
# }

# # ─────────────────────────────────────────────────────────────
# #  HELPER: Resolve group name from Excel Market + District
# # ─────────────────────────────────────────────────────────────

# def resolve_group(market, district):
#     market   = str(market).strip().upper()
#     district = str(district).strip()

#     # Try exact match first
#     key = (market, district)
#     if key in GROUP_MAP:
#         return GROUP_MAP[key]

#     # Try uppercase district
#     key = (market, district.upper())
#     if key in GROUP_MAP:
#         return GROUP_MAP[key]

#     # Try fallback with "-"
#     key = (market, "-")
#     if key in GROUP_MAP:
#         return GROUP_MAP[key]

#     # Try fallback with ""
#     key = (market, "")
#     if key in GROUP_MAP:
#         return GROUP_MAP[key]

#     # Last resort: use market name as-is
#     print(f"  ⚠️  No group found for Market='{market}' District='{district}' — using market name")
#     return market


# # ─────────────────────────────────────────────────────────────
# #  BUILD MESSAGE
# # ─────────────────────────────────────────────────────────────

# def build_message(market, district, dm_name, device_count):
#     first_name = dm_name.strip().split()[0]

#     if district and district not in ["-", "nan", "", "None"]:
#         header = f"{market} - {district} - {dm_name}"
#     else:
#         header = f"{market} - {dm_name}"

#     msg = (
#         f"{header}\n\n"
#         f"@~{first_name}\n"
#         f"\U0001f6a8 URGENT REMINDER\n\n"
#         f"Important reminder that the RMA, XBM & TRADE-IN shipments listed "
#         f"are still pending and are approaching the deadline \u23f3\n\n"
#         f"\u26a0\ufe0f Delayed shipment may result in chargebacks, so we kindly "
#         f"request you to prioritize shipping these devices as soon as possible "
#         f"\U0001f69a\U0001f4e6\n\n"
#         f"If you need any support, clarification, or assistance, please feel "
#         f"free to reach out \u2013 we\u2019re here to help \U0001f91d\n\n"
#         f"~ {SENDER_NAME} {SENDER_PHONE_PK}\n"
#         f"~.\n"
#         f"{SENDER_PHONE_US}"
#     )
#     return msg


# # ─────────────────────────────────────────────────────────────
# #  COPY IMAGE TO CLIPBOARD
# # ─────────────────────────────────────────────────────────────

# def copy_image_to_clipboard(image_path):
#     from PIL import Image
#     import win32clipboard
#     import win32con
#     import io

#     img = Image.open(image_path).convert("RGB")
#     output = io.BytesIO()
#     img.save(output, "BMP")
#     bmp_data = output.getvalue()[14:]
#     output.close()

#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardData(win32con.CF_DIB, bmp_data)
#     win32clipboard.CloseClipboard()


# # ─────────────────────────────────────────────────────────────
# #  SEND TO ONE GROUP  (exact same steps as your senior)
# # ─────────────────────────────────────────────────────────────

# def send_to_group(group_name, image_path, message):
#     # Step 1: Open search
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(2)

#     # Step 1.5: Clear previous search
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(2)
#     pyautogui.press('backspace')
#     time.sleep(2)

#     # Step 2: Type group name via clipboard (handles special chars)
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(2)
#     pyperclip.copy(group_name)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2)

#     # Step 3: Open first result
#     pyautogui.press('down')
#     time.sleep(2)
#     pyautogui.press('enter')
#     time.sleep(2)

#     # Step 4: Send text message
#     pyperclip.copy(message)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(1)
#     pyautogui.press('enter')
#     time.sleep(2)

#     # Step 5: Send image
#     copy_image_to_clipboard(image_path)
#     time.sleep(1)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2)
#     pyautogui.press('enter')
#     time.sleep(2)


# # ─────────────────────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────────────────────

# def main():
#     pyautogui.FAILSAFE = True  # Move mouse to top-left corner to stop!

#     print("=" * 60)
#     print("  STEP 2 — Sending WhatsApp Reminders")
#     print("=" * 60)

#     list_path = os.path.join(OUTPUT_FOLDER, "_dm_list.json")
#     if not os.path.exists(list_path):
#         print(f"\n❌ Run STEP1_Generate_Screenshots.py first!")
#         input("\nPress Enter to exit...")
#         return

#     with open(list_path) as f:
#         dm_list = json.load(f)

#     total = len(dm_list)
#     print(f"\nLoaded {total} DMs to send")

#     # Show preview of group mapping
#     print(f"\n{'─'*60}")
#     print("GROUP MAPPING PREVIEW (first 10):")
#     for dm in dm_list[:10]:
#         grp = resolve_group(dm['market'], dm.get('district', '-'))
#         print(f"  {dm['dm_name'][:25]:<25} → \"{grp}\"")
#     print(f"{'─'*60}")

#     print(f"\nMake sure WhatsApp Desktop is OPEN and VISIBLE!")
#     print(f"EMERGENCY STOP: Move mouse to TOP-LEFT corner of screen\n")
#     input("Press Enter when ready...")

#     print("\nYou have 5 seconds to click on WhatsApp Desktop...")
#     for i in range(5, 0, -1):
#         print(f"  {i}...", end="\r")
#         time.sleep(1)
#     print("\nStarting!\n")

#     success = 0
#     failed  = []

#     for idx, dm in enumerate(dm_list, 1):
#         market   = dm["market"]
#         district = dm.get("district", "-")
#         dm_name  = dm["dm_name"]
#         img_path = dm["image"]
#         count    = dm["count"]

#         group_name = resolve_group(market, district)
#         message    = build_message(market, district, dm_name, count)

#         print(f"[{idx}/{total}] {dm_name}")
#         print(f"         → Group: \"{group_name}\"  |  {count} device(s)")

#         if not os.path.exists(img_path):
#             print(f"  ⚠️  Image not found, skipping\n")
#             failed.append(f"{dm_name} (image missing)")
#             continue

#         try:
#             send_to_group(group_name, img_path, message)
#             print(f"  ✅ Sent!\n")
#             success += 1
#             time.sleep(3)

#         except Exception as e:
#             print(f"  ❌ Error: {e}\n")
#             failed.append(dm_name)
#             time.sleep(2)

#     print("=" * 60)
#     print(f"  COMPLETE — {success}/{total} messages sent successfully")
#     if failed:
#         print(f"\n  Failed ({len(failed)}):")
#         for name in failed:
#             print(f"    • {name}")
#     print("=" * 60)
#     input("\nPress Enter to exit...")


# if __name__ == "__main__":
#     main()





















"""
=====================================================================
  STEP 2 — TEST MODE
  Sends to YOUR WhatsApp number only, not to actual groups
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

# ============================================
# TEST MODE CONFIGURATION
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
YOUR_PHONE_NUMBER = "923108486366"  # Your WhatsApp number
SENDER_NAME = "HAMMAD ALI"
SENDER_PHONE_PK = "+92 371 1128675"
SENDER_PHONE_US = "+1 (213) 214-4337"

# ============================================
# COPY IMAGE TO CLIPBOARD
# ============================================

def copy_image_to_clipboard(image_path):
    """Copy image to clipboard for pasting in WhatsApp"""
    img = Image.open(image_path).convert("RGB")
    output = io.BytesIO()
    img.save(output, "BMP")
    bmp_data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, bmp_data)
    win32clipboard.CloseClipboard()

# ============================================
# BUILD MESSAGE
# ============================================

def build_message(market, district, dm_name, device_count, total_value):
    first_name = dm_name.strip().split()[0] if ' ' in dm_name else dm_name
    
    if district and district not in ["-", "nan", "", "None"]:
        header = f"{market} - {district} - {dm_name}"
    else:
        header = f"{market} - {dm_name}"
    
    msg = f"""{header}

@{first_name}
URGENT REMINDER

Important reminder that the RMA, XBM & TRADE-IN shipments listed are still pending and are approaching the deadline 🚨

⚠️ Delayed shipment may result in chargebacks, so we kindly request you to prioritize shipping these devices as soon as possible 🚨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
├ 📦 Total Devices: {device_count}
├ 💰 Total Value: ${total_value:,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you need any support, please reach out 🚨

~ {SENDER_NAME} {SENDER_PHONE_PK}
~.
{SENDER_PHONE_US}"""
    
    return msg

# ============================================
# SEND TO YOUR NUMBER (TEST MODE)
# ============================================

def send_to_test_number(image_path, message):
    """Send message and image to your personal WhatsApp number"""
    
    # Open search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    
    # Clear previous search
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('backspace')
    time.sleep(1)
    
    # Type your number
    pyperclip.copy(YOUR_PHONE_NUMBER)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    
    # Press Enter to open chat
    pyautogui.press('enter')
    time.sleep(2)
    
    # Send text message
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Send image
    copy_image_to_clipboard(image_path)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    
    return True

# ============================================
# MAIN
# ============================================

def main():
    pyautogui.FAILSAFE = True
    
    print("=" * 60)
    print("  STEP 2 — TEST MODE (Sending to YOUR number only)")
    print("=" * 60)
    
    list_path = os.path.join(OUTPUT_FOLDER, "_dm_list.json")
    if not os.path.exists(list_path):
        print(f"\n❌ Run STEP1_Generate_Screenshots.py first!")
        input("\nPress Enter to exit...")
        return
    
    with open(list_path, 'r') as f:
        dm_list = json.load(f)
    
    # Add total_value from screenshots (you may need to calculate)
    # For now, we'll use placeholder values
    for dm in dm_list:
        dm['total_value'] = 0  # You can calculate this from your Excel
    
    total = len(dm_list)
    print(f"\n📊 Loaded {total} DMs for testing")
    print(f"📱 Will send to: +{YOUR_PHONE_NUMBER}")
    
    print(f"\n⚠️ IMPORTANT:")
    print(f"   • Make sure WhatsApp Desktop is OPEN")
    print(f"   • You are LOGGED IN")
    print(f"   • Move mouse to TOP-LEFT corner to stop")
    
    input("\nPress Enter when ready...")
    
    print("\nYou have 5 seconds to click on WhatsApp Desktop...")
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    print("\nStarting!\n")
    
    success = 0
    
    for idx, dm in enumerate(dm_list, 1):
        market = dm.get("market", "Unknown")
        district = dm.get("district", "-")
        dm_name = dm.get("dm_name", "Unknown")
        img_path = dm.get("image", "")
        device_count = dm.get("count", 0)
        total_value = dm.get("total_value", 0)
        
        print(f"[{idx}/{total}] TESTING: {market} - {dm_name}")
        print(f"   Devices: {device_count}")
        
        if not os.path.exists(img_path):
            print(f"   ⚠️ Image not found: {img_path}")
            continue
        
        message = build_message(market, district, dm_name, device_count, total_value)
        
        try:
            send_to_test_number(img_path, message)
            print(f"   ✅ Sent to YOUR WhatsApp!\n")
            success += 1
            time.sleep(2)
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    
    print("=" * 60)
    print(f"  ✅ TEST COMPLETE!")
    print(f"  Sent {success}/{total} test messages to YOUR WhatsApp")
    print("=" * 60)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()