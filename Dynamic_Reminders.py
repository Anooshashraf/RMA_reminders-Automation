# """
# =====================================================================
#   STANDALONE TEXT-ONLY WHATSAPP SENDER
#   ONE message per group - NO DM tags - Plain text only!
  
#   Uses CONFIG_WhatsApp_Groups.py for group list
# =====================================================================
# """

# import pyautogui
# import pyperclip
# import time
# import os
# import sys

# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from CONFIG_WhatsApp_Groups import WHATSAPP_GROUP_MAP

# # ═══════════════════════════════════════════════════════════════
# #  CONFIGURATION
# # ═══════════════════════════════════════════════════════════════

# TEST_MODE = False  # True = send to YOUR_NUMBER only, False = send to group
# YOUR_NUMBER = "923108486366"

# # ═══════════════════════════════════════════════════════════════
# #  YOUR MESSAGE HERE
# # ═══════════════════════════════════════════════════════════════

# MESSAGE = """Greetings Store Team,

# If any store is experiencing issues with defective HINT or other devices, 
# please have them reach out to us promptly with:

# • Pictures of the device with visible IMEI
# • EDGE history so that label can be processed

# Thank you for your cooperation and support."""

# pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 0.3


# # ═══════════════════════════════════════════════════════════════
# #  BUILD UNIQUE GROUP LIST
# # ═══════════════════════════════════════════════════════════════

# def build_group_list():
#     """Build unique group list - ONE per WhatsApp group."""
#     groups = {}

#     for (market, district), info in WHATSAPP_GROUP_MAP.items():
#         merge_key = info.get('merge_key')
#         key = merge_key if merge_key else info.get('group')

#         if key not in groups:
#             groups[key] = {
#                 'whatsapp_group': info.get('group'),
#                 'send_mode': info.get('mode', 'send_to_group'),
#             }

#     # ONE per unique group name
#     group_list = []
#     sent_groups = set()

#     for key, data in groups.items():
#         name = data['whatsapp_group']
#         if name in sent_groups:
#             continue
#         sent_groups.add(name)

#         group_list.append({
#             'whatsapp_group': name,
#             'send_mode': data['send_mode'],
#         })

#     return group_list


# # ═══════════════════════════════════════════════════════════════
# #  WHATSAPP HELPERS
# # ═══════════════════════════════════════════════════════════════

# def copy_text(text):
#     pyperclip.copy(text)
#     time.sleep(0.3)


# def focus_whatsapp():
#     w, h = pyautogui.size()
#     pyautogui.click(w // 2, h // 2)
#     time.sleep(0.5)
#     pyautogui.click(w // 2, h // 2)
#     time.sleep(0.5)


# def open_chat(target):
#     focus_whatsapp()
#     time.sleep(0.5)
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.3)
#     pyautogui.press('backspace')
#     time.sleep(0.3)
#     copy_text(target)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.0)
#     pyautogui.press('down')
#     time.sleep(0.5)
#     pyautogui.press('enter')
#     time.sleep(2.0)
#     print(f"  ✅ Opened: {target}")


# def send_text(target):
#     """Send plain text message - no tags"""
#     open_chat(target)
#     time.sleep(1.0)
#     focus_whatsapp()
#     time.sleep(0.5)

#     copy_text(MESSAGE)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(1.0)
#     pyautogui.press('enter')
#     time.sleep(2.0)
#     print(f"  ✅ Sent")


# # ═══════════════════════════════════════════════════════════════
# #  MAIN
# # ═══════════════════════════════════════════════════════════════

# def main():
#     print("=" * 60)
#     print("  STANDALONE TEXT SENDER (NO TAGS)")
#     print("=" * 60)

#     group_list = build_group_list()
#     total = len(group_list)
#     print(f"📊 {total} unique groups\n")

#     print("📋 Message:")
#     print("-" * 40)
#     print(MESSAGE)
#     print("-" * 40)

#     print(f"\n📋 Groups:")
#     for i, g in enumerate(group_list, 1):
#         print(f"  {i:2}. {g['whatsapp_group']}")

#     print(f"\n⚠️  {'TEST MODE → +' + YOUR_NUMBER if TEST_MODE else 'LIVE MODE'}")
#     print(f"   ONE plain text message per group (no @tags)")

#     print("\n" + "-" * 60)
#     print("1. WhatsApp Desktop OPEN & MAXIMIZED")
#     print("2. Press Enter, click WhatsApp in 5 sec")
#     print("3. Mouse to TOP-LEFT corner to abort")
#     print("-" * 60)

#     if input("\nPress Enter (q to quit): ").lower() == 'q':
#         return

#     print("\n⚠️  Click WhatsApp NOW!")
#     for i in range(5, 0, -1):
#         print(f"  {i}...", end="\r")
#         time.sleep(1)
#     print("\nGO!\n")

#     ok = fail = 0

#     for idx, g in enumerate(group_list, 1):
#         try:
#             name = g['whatsapp_group']
#             mode = g.get('send_mode', 'send_to_group')

#             print(f"\n{'─'*55}")
#             print(f"[{idx}/{total}] {name}")

#             if TEST_MODE:
#                 targets = [YOUR_NUMBER]
#             elif mode == "send_to_both_groups":
#                 targets = ["Dallas Team South", "Dallas Team North"]
#             else:
#                 targets = [name]

#             for t in targets:
#                 print(f"  → {t}")
#                 send_text(t)
#                 time.sleep(2.0)

#             ok += 1
#             time.sleep(2.0)

#         except pyautogui.FailSafeException:
#             print("\n🛑 Aborted")
#             break
#         except KeyboardInterrupt:
#             print("\n🛑 Aborted")
#             break
#         except Exception as e:
#             print(f"  ❌ {e}")
#             fail += 1
#             time.sleep(2)

#     print("\n" + "=" * 60)
#     print(f"✅ Sent: {ok} | ❌ Failed: {fail}")
#     print(f"📱 {'TEST' if TEST_MODE else 'LIVE'} — Plain text, no tags")
#     print("=" * 60)

#     if TEST_MODE:
#         print(f"\nCheck +{YOUR_NUMBER}, then set TEST_MODE = False")

#     input("\nPress Enter...")


# if __name__ == "__main__":
#     main()




"""
=====================================================================
  STANDALONE TEXT-ONLY WHATSAPP SENDER (RESUMABLE)
  ONE message per group - NO DM tags - Plain text only!
  
  SET START_FROM to resume from a specific group number
=====================================================================
"""

import pyautogui
import pyperclip
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from CONFIG_WhatsApp_Groups import WHATSAPP_GROUP_MAP

# ═══════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════

TEST_MODE = False
YOUR_NUMBER = "923108486366"


START_FROM = 7  

# ═══════════════════════════════════════════════════════════════
#  YOUR MESSAGE HERE
# ═══════════════════════════════════════════════════════════════

MESSAGE = """Greetings Store Team,

If any store is experiencing issues with defective HINT or other devices, 
please have them reach out to us promptly with:

• Pictures of the device with visible IMEI
• EDGE history so that label can be processed

Thank you for your cooperation and support."""

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


# ═══════════════════════════════════════════════════════════════
#  BUILD UNIQUE GROUP LIST
# ═══════════════════════════════════════════════════════════════

def build_group_list():
    """Build unique group list - ONE per WhatsApp group."""
    groups = {}

    for (market, district), info in WHATSAPP_GROUP_MAP.items():
        merge_key = info.get('merge_key')
        key = merge_key if merge_key else info.get('group')

        if key not in groups:
            groups[key] = {
                'whatsapp_group': info.get('group'),
                'send_mode': info.get('mode', 'send_to_group'),
            }

    group_list = []
    sent_groups = set()

    for key, data in groups.items():
        name = data['whatsapp_group']
        if name in sent_groups:
            continue
        sent_groups.add(name)

        group_list.append({
            'whatsapp_group': name,
            'send_mode': data['send_mode'],
        })

    return group_list


# ═══════════════════════════════════════════════════════════════
#  WHATSAPP HELPERS
# ═══════════════════════════════════════════════════════════════

def copy_text(text):
    pyperclip.copy(text)
    time.sleep(0.3)


def focus_whatsapp():
    w, h = pyautogui.size()
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)


def open_chat(target):
    focus_whatsapp()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)
    copy_text(target)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.0)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2.0)
    print(f"  ✅ Opened: {target}")


def send_text(target):
    """Send plain text message - no tags"""
    open_chat(target)
    time.sleep(1.0)
    focus_whatsapp()
    time.sleep(0.5)

    copy_text(MESSAGE)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    pyautogui.press('enter')
    time.sleep(2.0)
    print(f"  ✅ Sent")


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  STANDALONE TEXT SENDER (RESUMABLE)")
    print("=" * 60)

    group_list = build_group_list()
    total = len(group_list)
    
    # Slice list to start from a specific group
    if START_FROM > 1:
        group_list = group_list[START_FROM - 1:]
        print(f"📊 {total} total groups — RESUMING from #{START_FROM}\n")
    else:
        print(f"📊 {total} unique groups\n")

    print("📋 Message:")
    print("-" * 40)
    print(MESSAGE)
    print("-" * 40)

    print(f"\n📋 Groups to send:")
    for i, g in enumerate(group_list, START_FROM if START_FROM > 1 else 1):
        print(f"  {i:2}. {g['whatsapp_group']}")

    print(f"\n⚠️  {'TEST MODE → +' + YOUR_NUMBER if TEST_MODE else 'LIVE MODE'}")
    print(f"   Resuming from group #{START_FROM}" if START_FROM > 1 else "   Starting from beginning")

    print("\n" + "-" * 60)
    print("1. WhatsApp Desktop OPEN & MAXIMIZED")
    print("2. Press Enter, click WhatsApp in 5 sec")
    print("3. Mouse to TOP-LEFT corner to abort")
    print("-" * 60)

    if input("\nPress Enter (q to quit): ").lower() == 'q':
        return

    print("\n⚠️  Click WhatsApp NOW!")
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    print("\nGO!\n")

    ok = fail = 0
    current_num = START_FROM if START_FROM > 1 else 1

    for idx, g in enumerate(group_list, current_num):
        try:
            name = g['whatsapp_group']
            mode = g.get('send_mode', 'send_to_group')

            print(f"\n{'─'*55}")
            print(f"[{idx}/{total}] {name}")

            if TEST_MODE:
                targets = [YOUR_NUMBER]
            elif mode == "send_to_both_groups":
                targets = ["Dallas Team South", "Dallas Team North"]
            else:
                targets = [name]

            for t in targets:
                print(f"  → {t}")
                send_text(t)
                time.sleep(2.0)

            ok += 1
            time.sleep(2.0)

        except pyautogui.FailSafeException:
            print(f"\n🛑 Aborted at group #{idx}")
            print(f"   To resume, set START_FROM = {idx}")
            break
        except KeyboardInterrupt:
            print(f"\n🛑 Aborted at group #{idx}")
            print(f"   To resume, set START_FROM = {idx}")
            break
        except Exception as e:
            print(f"  ❌ {e}")
            fail += 1
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"✅ Sent: {ok} | ❌ Failed: {fail}")
    print(f"📱 {'TEST' if TEST_MODE else 'LIVE'} — Plain text, no tags")
    print("=" * 60)


if __name__ == "__main__":
    main()