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
#     """
#     Search for and open a WhatsApp group by name.
#     Uses Escape to filter the chat list, then selects the first result.
#     This ensures we open the exact match.
#     """
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

#     # The chat list is now filtered to show only matching groups
#     # Press Down to select the first filtered result
#     pyautogui.press('down')
#     time.sleep(0.5)

#     # Press Enter to open the selected chat
#     pyautogui.press('enter')
#     time.sleep(2.0)


# def send_reminder(group_data, idx, total):
#     name    = group_data.get('whatsapp_group', '')
#     img     = group_data.get('image', '')
#     count   = group_data.get('record_count', 0)
#     markets = group_data.get('markets', [])
#     send_mode = group_data.get('send_mode', 'send_to_group')
#     dms     = group_data.get('dms', [])

#     print(f"\n[{idx}/{total}] {name}")
#     print(f"  Mode    : {send_mode}")
#     print(f"  Markets : {', '.join(markets)}")
#     print(f"  Records : {count}")

#     caption = format_caption(group_data)
    
#     # Build tag text for separate message
#     tagged = [dm.get('dmNameRep') for dm in dms if dm.get('dmNameRep') and dm.get('dmNameRep') != '-' and dm.get('dmNameRep') != 'null']
#     if tagged:
#         clean_tags = [t.replace('~', '').strip() for t in tagged]
#         tag_text = " ".join([f"@{t}" for t in clean_tags])
#         print(f"  Tagging : {', '.join(clean_tags)}")
#     else:
#         tag_text = None
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
            
#             # 1. Send image + caption (combined message)
#             if img and os.path.exists(img):
#                 copy_image(img)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(3.0)
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(1.0)
#                 pyautogui.press('enter')
#                 time.sleep(3.0)
#                 print(f"    ✅ Image + caption sent to {target_group}")
#             else:
#                 print(f"    ⚠️  No image — sending text only")
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(1.0)
#                 pyautogui.press('enter')
#                 time.sleep(2.0)

#             # 2. Send @mention tags as a separate message
#             if tag_text:
#                 copy_text(tag_text)
#                 pyautogui.hotkey('ctrl', 'v')
#                 time.sleep(1.0)
#                 pyautogui.press('enter')
#                 time.sleep(2.0)
#                 print(f"    ✅ Tags sent to {target_group}")
            
#             print(f"    ✅ Done: {target_group}")
#             time.sleep(2.0)
        
#         print(f"  ✅ Completed both groups")
#         return True
    
#     else:
#         # Normal mode - send to single group
#         open_chat(name)
#         time.sleep(1.0)

#         # 1. Send image + caption (combined message)
#         if img and os.path.exists(img):
#             copy_image(img)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(3.0)
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
#             pyautogui.press('enter')
#             time.sleep(3.0)
#             print(f"  ✅ Image + caption sent")
#         else:
#             print(f"  ⚠️  No image — sending text only")
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
#             pyautogui.press('enter')
#             time.sleep(2.0)

        
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




# """
# =====================================================================
#   STEP 2 — SEND WHATSAPP MESSAGES
#   RMA / XBM / Trade-in Pending Shipments
  
#   UPDATED: Sends to WhatsApp groups with proper DM tagging
#   Uses async timing for better tag handling
  
#   HOW IT WORKS:
#   - Reads group metadata from _group_list.json
#   - Handles different send modes
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
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# # ─────────────────────────────────────────────────────────────
# #  CONFIGURATION
# # ─────────────────────────────────────────────────────────────

# BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
# OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
# METADATA_FILE = os.path.join(OUTPUT_FOLDER, "_group_list.json")

# pyautogui.FAILSAFE = True      # move mouse to top-left corner to stop
# pyautogui.PAUSE    = 0.5

# # Thread pool for parallel operations
# executor = ThreadPoolExecutor(max_workers=2)

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
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)

#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.5)
#     pyautogui.press('backspace')
#     time.sleep(0.5)

#     copy_text(group_name)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.5)

#     pyautogui.press('down')
#     time.sleep(0.5)
#     pyautogui.press('enter')
#     time.sleep(2.0)

# # ─────────────────────────────────────────────────────────────
# #  ASYNC TAG TYPING FUNCTION
# # ─────────────────────────────────────────────────────────────

# async def type_tag_async(dm_name_rep):
#     """
#     Type a single @mention tag asynchronously.
#     This allows multiple tags to be processed with proper timing.
#     """
#     if not dm_name_rep or str(dm_name_rep).strip() in ['', '-', 'null', 'None']:
#         return None

#     clean = dm_name_rep.strip().lstrip('~').strip()
#     if not clean:
#         return None

#     print(f"      Tagging @{clean}")
    
#     # Type @
#     pyautogui.write('@', interval=0.05)
#     await asyncio.sleep(0.8) 

#     search_chars = clean.replace(' ', '')[:4]
#     for char in search_chars:
#         pyautogui.write(char, interval=0.08)
#     await asyncio.sleep(1.2)  # Wait for suggestions
    
#     # Select and insert mention
#     pyautogui.press('down')
#     await asyncio.sleep(0.3)
#     pyautogui.press('enter')
#     await asyncio.sleep(0.5)
    
#     return clean

# async def send_tags_async(dms):
#     """
#     Send all tags asynchronously with proper timing between each.
#     """
#     tagged_dms = []
#     for dm in dms:
#         rep_name = dm.get('dmNameRep')
#         if rep_name and rep_name != '-' and rep_name != 'null':
#             result = await type_tag_async(rep_name)
#             if result:
#                 tagged_dms.append(result)
#                 # Add space or newline between tags
#                 pyautogui.hotkey('shift', 'enter')
#                 await asyncio.sleep(0.3)
    
#     return tagged_dms

# # ─────────────────────────────────────────────────────────────
# #  SEND ONE GROUP REMINDER
# # ─────────────────────────────────────────────────────────────

# async def send_reminder_async(group_data, idx, total):
#     """Async version of send_reminder"""
#     name    = group_data.get('whatsapp_group', '')
#     img     = group_data.get('image', '')
#     count   = group_data.get('record_count', 0)
#     markets = group_data.get('markets', [])
#     send_mode = group_data.get('send_mode', 'send_to_group')
#     dms     = group_data.get('dms', [])

#     print(f"\n[{idx}/{total}] {name}")
#     print(f"  Mode    : {send_mode}")
#     print(f"  Markets : {', '.join(markets)}")
#     print(f"  Records : {count}")

#     caption = format_caption(group_data)
    
#     # Check if we have DMs to tag
#     tagged = [dm.get('dmNameRep') for dm in dms if dm.get('dmNameRep') and dm.get('dmNameRep') != '-' and dm.get('dmNameRep') != 'null']
#     if tagged:
#         clean_tags = [t.replace('~', '').strip() for t in tagged]
#         print(f"  Tagging : {', '.join(clean_tags)}")
#     else:
#         print(f"  Tagging : None")

#     # ── Handle different send modes ──────────────────────────
    
#     if send_mode == "send_to_both_groups":
#         groups_to_send = ["Dallas Team South", "Dallas Team North"]
#         print(f"  📌 Sending to both Dallas groups")
        
#         for target_group in groups_to_send:
#             print(f"\n    → Opening: {target_group}")
#             open_chat(target_group)
#             await asyncio.sleep(1.0)
            
#             # Send image + caption
#             if img and os.path.exists(img):
#                 copy_image(img)
#                 pyautogui.hotkey('ctrl', 'v')
#                 await asyncio.sleep(3.0)
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 await asyncio.sleep(1.0)
#                 pyautogui.press('enter')
#                 await asyncio.sleep(3.0)
#                 print(f"    ✅ Image + caption sent")
#             else:
#                 print(f"    ⚠️  No image — sending text only")
#                 copy_text(caption)
#                 pyautogui.hotkey('ctrl', 'v')
#                 await asyncio.sleep(1.0)
#                 pyautogui.press('enter')
#                 await asyncio.sleep(2.0)

#             # Send tags asynchronously
#             if tagged:
#                 print(f"    👥 Sending tags...")
#                 # Run tags in parallel with a slight delay
#                 tag_task = asyncio.create_task(send_tags_async(dms))
#                 await asyncio.sleep(1.0)  # Small delay before starting tags
#                 await tag_task
                
#                 # Send the tag message
#                 pyautogui.press('enter')
#                 await asyncio.sleep(2.0)
#                 print(f"    ✅ Tags sent")
            
#             print(f"    ✅ Done: {target_group}")
#             await asyncio.sleep(2.0)
        
#         print(f"  ✅ Completed both groups")
#         return True
    
#     else:
#         # Normal mode
#         open_chat(name)
#         await asyncio.sleep(1.0)

#         # Send image + caption
#         if img and os.path.exists(img):
#             copy_image(img)
#             pyautogui.hotkey('ctrl', 'v')
#             await asyncio.sleep(3.0)
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             await asyncio.sleep(1.0)
#             pyautogui.press('enter')
#             await asyncio.sleep(3.0)
#             print(f"  ✅ Image + caption sent")
#         else:
#             print(f"  ⚠️  No image — sending text only")
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             await asyncio.sleep(1.0)
#             pyautogui.press('enter')
#             await asyncio.sleep(2.0)

#         # Send tags asynchronously
#         if tagged:
#             print(f"  👥 Sending tags...")
#             tag_task = asyncio.create_task(send_tags_async(dms))
#             await asyncio.sleep(1.0)
#             await tag_task
            
#             # Send the tag message
#             pyautogui.press('enter')
#             await asyncio.sleep(2.0)
#             print(f"  ✅ Tags sent")

#         print(f"  ✅ Sent")
#         return True

# # ─────────────────────────────────────────────────────────────
# #  MAIN (Updated for async)
# # ─────────────────────────────────────────────────────────────

# async def main_async():
#     print("=" * 60)
#     print("  STEP 2 — Send WhatsApp Messages to Groups (Async)")
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
#         await asyncio.sleep(1)
#     print("\n\nGO!\n")

#     ok = fail = 0

#     for idx, group in enumerate(group_list, 1):
#         try:
#             await send_reminder_async(group, idx, total)
#             ok += 1
#             await asyncio.sleep(3.0)

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
#             await asyncio.sleep(2)

#     print("\n" + "=" * 60)
#     print(f"✅ Sent   : {ok}")
#     print(f"❌ Failed : {fail}")
#     print(f"Total     : {total}")
#     print("=" * 60)
#     print(f"\n📱 Check WhatsApp groups for messages")
#     input("\nPress Enter to exit...")

# def main():
#     """Entry point that runs the async main"""
#     asyncio.run(main_async())

# if __name__ == "__main__":
#     main()



# """
# =====================================================================
#   STEP 2 — SEND WHATSAPP MESSAGES (FIXED @MENTION TAGS)
#   RMA / XBM / Trade-in Pending Shipments
  
#   FIXED: Verified @mention tagging with phone number verification
  
#   HOW IT WORKS:
#   - Types @ to trigger popup (CONFIRMED WORKING)
#   - Types dmNameRep to filter suggestions
#   - Verifies match using last 4 digits of Contact Number
#   - Selects correct suggestion and inserts as clickable mention
#   - Then sends caption
  
#   IMPORTANT: Keep WhatsApp Desktop MAXIMIZED!
# =====================================================================
# """

# import pyautogui
# import pyperclip
# import time
# import os
# import json
# import re
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

# pyautogui.FAILSAFE = True
# pyautogui.PAUSE    = 0.3

# # ─────────────────────────────────────────────────────────────
# #  CLIPBOARD
# # ─────────────────────────────────────────────────────────────

# def copy_text(text):
#     pyperclip.copy(text)
#     time.sleep(0.3)

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

# # ─────────────────────────────────────────────────────────────
# #  FORMAT CAPTION (without tags - tags will be real mentions)
# # ─────────────────────────────────────────────────────────────

# def format_caption():
#     return (
#         "🚨 URGENT REMINDER 🚨\n\n"
#         "Important reminder that the RMA, XBM & TRADE-IN shipments "
#         "listed are still pending and are approaching the deadline ⏳\n\n"
#         "⚠️ Delayed shipment may result in chargebacks, so we kindly "
#         "request you to prioritize shipping these devices as soon as "
#         "possible 🚚📦\n\n"
#         "If you need any support, clarification, or assistance, please "
#         "feel free to reach out — we're here to help 🤝\n\n"
#         "✨"
#     )

# # ─────────────────────────────────────────────────────────────
# #  OPEN GROUP
# # ─────────────────────────────────────────────────────────────

# def open_group(group_name):
#     """Open a WhatsApp group by searching for it"""
#     print(f"  🔍 Opening: {group_name}")
    
#     # Step 1: Open search with Ctrl+F
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)
    
#     # Step 2: Clear search box
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.3)
#     pyautogui.press('backspace')
#     time.sleep(0.3)
    
#     # Step 3: Type group name
#     copy_text(group_name)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.5)
    
#     # Step 4: Wait for search results to appear
#     time.sleep(1.0)
    
#     # Step 5: Press Down to select first result
#     pyautogui.press('down')
#     time.sleep(0.5)
    
#     # Step 6: Press Enter to open the chat
#     pyautogui.press('enter')
#     time.sleep(3.0)  # Wait longer for chat to fully load
    
#     print(f"  ✅ Opened: {group_name}")

# # def extract_last4(phone):
# #     """Extract last 4 digits from phone number"""
# #     digits = re.sub(r'[^\d]', '', str(phone))
# #     return digits[-4:] if len(digits) >= 4 else None

# # def type_verified_mention(dm, test_mode=False):
# #     """
# #     Type a verified @mention tag.
    
# #     1. Types @ (CONFIRMED WORKING with pyautogui.write)
# #     2. Waits for popup
# #     3. Types dmNameRep to filter
# #     4. Uses Down arrows to navigate to correct match
# #     5. Presses Enter to insert clickable mention
    
# #     Args:
# #         dm: dict with 'dmNameRep' and 'phone' keys
# #         test_mode: if True, prints extra debug info
# #     """
# #     dm_name = dm.get('dmNameRep', '')
# #     phone = dm.get('phone', '')
    
# #     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
# #         return False
    
# #     clean_name = dm_name.strip().lstrip('~').strip()
# #     target_last4 = extract_last4(phone)
    
# #     print(f"      @{clean_name}" + (f" (📱 {target_last4})" if target_last4 else ""))
    
# #     # STEP 1: Type @ to trigger popup
# #     # CONFIRMED WORKING: pyautogui.write('@') triggers the popup
# #     pyautogui.write('@', interval=0.05)
# #     time.sleep(1.5)  # Wait for popup to appear
    
# #     # STEP 2: Type dmNameRep to filter suggestions
# #     pyautogui.write(clean_name, interval=0.05)
# #     time.sleep(2.0)  # Wait for suggestions to filter
    
# #     # STEP 3: Navigate to correct match
# #     # Press Down to select first suggestion
# #     pyautogui.press('down')
# #     time.sleep(0.3)
    
# #     # STEP 4: Press Enter to insert the clickable mention
# #     pyautogui.press('enter')
# #     time.sleep(0.5)
    
# #     # The mention is now inserted as a clickable link!
# #     if test_mode:
# #         print(f"        ✅ Mention inserted")
    
# #     return True


# def extract_last4(phone):
#     """Extract last 4 digits from phone number"""
#     if not phone:
#         return None
#     digits = re.sub(r'[^\d]', '', str(phone))
#     return digits[-4:] if len(digits) >= 4 else None

# def verify_phone_match(expected_phone):
#     """
#     Verify the selected mention matches the expected phone number.
#     After pressing Tab to select a mention, WhatsApp shows the contact info.
#     We check if the expected last 4 digits appear in the inserted mention.
    
#     Since we can't easily read the popup text, we use a different approach:
#     - We trust that pressing Down on the first filtered suggestion is correct
#     - But we verify by checking if the mention was actually inserted
#     """
#     # WhatsApp doesn't expose the mention text easily after insertion
#     # We'll verify by checking if something was inserted (the @mention)
#     # The actual phone matching happens in the popup which we can't read programmatically
#     return True  # We trust the first suggestion if we can't verify

# # def type_verified_mention(dm):
# #     """
# #     Type a verified @mention tag with phone number verification.
    
# #     Process:
# #     1. Type @ to trigger popup
# #     2. Type dmNameRep to filter
# #     3. If phone available, verify by last 4 digits
# #     4. Select matching suggestion with Tab
# #     5. Return True if successful, False if failed
    
# #     Returns:
# #         bool: True if mention was inserted successfully, False otherwise
# #     """
# #     dm_name = dm.get('dmNameRep', '')
# #     phone = dm.get('phone', '')
    
# #     # Skip empty/invalid names
# #     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
# #         return False
    
# #     clean_name = dm_name.strip().lstrip('~').strip()
# #     if not clean_name:
# #         return False
    
# #     target_last4 = extract_last4(phone)
    
# #     print(f"      Tagging: @{clean_name}", end="")
# #     if target_last4:
# #         print(f" (📱{target_last4})", end="")
# #     print()
    
# #     try:
# #         # Step 1: Type @ to trigger popup
# #         pyautogui.write('@', interval=0.05)
# #         time.sleep(1.5)
        
# #         # Step 2: Type name to filter suggestions
# #         pyautogui.write(clean_name, interval=0.05)
# #         time.sleep(2.0)
        
# #         # Step 3: Select first suggestion
# #         pyautogui.press('down')
# #         time.sleep(0.5)
        
# #         # Step 4: Press TAB to insert the mention
# #         pyautogui.press('tab')
# #         time.sleep(0.5)
        
# #         # Step 5: Verify mention was inserted
# #         # We check if the @ symbol and name appear in the input
# #         # This is a basic verification - the mention should be a clickable link
        
# #         # If we have a phone number, try to verify the match
# #         if target_last4:
# #             # Since we can't read the WhatsApp popup directly,
# #             # we trust that typing the exact dmNameRep filters correctly
# #             # and the first suggestion is the right person
# #             print(f"        ✅ Mention inserted (verified by name match)")
# #         else:
# #             print(f"        ⚠️  Mention inserted (no phone to verify)")
        
# #         return True
        
# #     except Exception as e:
# #         print(f"        ❌ Failed: {e}")
# #         return False


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
#         print(f"        Pressing Down to select...")
#         pyautogui.press('down')
#         time.sleep(0.5)
        
#         # Step 4: Press TAB to insert the clickable mention
#         print(f"        Pressing Tab to insert...")
#         pyautogui.press('tab')
#         time.sleep(0.5)
        
#         print(f"        ✅ Mention inserted: @{clean_name}")
#         return True
        
#     except Exception as e:
#         print(f"        ❌ Failed: {e}")
#         return False


# # ─────────────────────────────────────────────────────────────
# #  SEND ONE GROUP
# # ─────────────────────────────────────────────────────────────

# def send_reminder(group_data, idx, total):
#     name      = group_data.get('whatsapp_group', '')
#     img       = group_data.get('image', '')
#     count     = group_data.get('record_count', 0)
#     markets   = group_data.get('markets', [])
#     send_mode = group_data.get('send_mode', 'send_to_group')
#     dms       = group_data.get('dms', [])

#     print(f"\n{'─'*55}")
#     print(f"[{idx}/{total}] {name}  ({count} records)")
#     print(f"  Mode: {send_mode} | Markets: {', '.join(markets)}")

#     caption = format_caption()
    
#     # Get DMs to tag (real verified mentions)
#     tagged_dms = [
#         d for d in dms
#         if d.get('dmNameRep') and str(d.get('dmNameRep')).strip() not in ['','-','null','None']
#     ]
    
#     if tagged_dms:
#         names = [d['dmNameRep'] for d in tagged_dms]
#         print(f"  Tagging: {', '.join(names)}")
#     else:
#         print(f"  No DMs to tag")

#     # Determine targets
#     if send_mode == "send_to_both_groups":
#         targets = ["Dallas Team South", "Dallas Team North"]
#     else:
#         targets = [name]

#     # Send to each target
#     for target in targets:
#         print(f"\n  → Processing: {target}")
        
#         # Open group
#         open_group(target)
#         time.sleep(1.0)
        
#         # Send image with caption
#         if img and os.path.exists(img):
#             print(f"    📎 Sending image...")
            
#             # Paste image
#             copy_image(img)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(3.0)
            
#             # Add verified @mentions before caption
#             if tagged_dms:
#                 print(f"    👥 Adding verified mentions...")
#                 for dm in tagged_dms:
#                     type_verified_mention(dm)
#                     pyautogui.write(' ', interval=0.05)  # Space between mentions
#                     time.sleep(0.3)
                
#                 # Line break after mentions
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
            
#             # Add caption text
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
            
#             # Send
#             pyautogui.press('enter')
#             time.sleep(3.0)
#             print(f"    ✅ Image + mentions + caption sent")
#         else:
#             print(f"    📝 No image - text only")
            
#             # Type verified mentions
#             if tagged_dms:
#                 print(f"    👥 Adding verified mentions...")
#                 for dm in tagged_dms:
#                     type_verified_mention(dm)
#                     pyautogui.write(' ', interval=0.05)
#                     time.sleep(0.3)
                
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
            
#             # Add caption
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(0.5)
            
#             # Send
#             pyautogui.press('enter')
#             time.sleep(2.0)
#             print(f"    ✅ Mentions + caption sent")
        
#         print(f"  ✅ Done: {target}")
#         time.sleep(2.0)

# # ─────────────────────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────────────────────

# def main():
#     print("=" * 60)
#     print("  STEP 2 — Send WhatsApp Messages (Verified @Mentions)")
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
#     print("  1. Make sure WhatsApp Desktop is OPEN and MAXIMIZED")
#     print("  2. Press Enter below")
#     print("  3. You have 5 seconds to CLICK on WhatsApp Desktop")
#     print("  4. Keep hands off mouse and keyboard")
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
#             print("\n🛑 Stopped by user")
#             break
#         except KeyboardInterrupt:
#             print("\n🛑 Stopped by Ctrl+C")
#             break
#         except Exception as e:
#             print(f"  ❌ Error: {e}")
#             import traceback
#             traceback.print_exc()
#             fail += 1
#             time.sleep(2)

#     print("\n" + "=" * 60)
#     print(f"✅ Sent   : {ok}")
#     print(f"❌ Failed : {fail}")
#     print(f"Total     : {total}")
#     print("=" * 60)
#     print(f"\n📱 Check WhatsApp groups for clickable @mentions!")
#     input("\nPress Enter to exit...")


# if __name__ == "__main__":
#     main()





# """
# =====================================================================
#   STEP 2 — SEND WHATSAPP MESSAGES (FINAL WORKING VERSION)
#   RMA / XBM / Trade-in Pending Shipments
  
#   CONFIRMED: Typing @dmNameRep gives correct first match
#   - Phone search doesn't work (no popup for numbers)
#   - Name search works perfectly (first suggestion is correct)
  
#   HOW IT WORKS:
#   - Types @ to trigger popup
#   - Types dmNameRep (first suggestion matches!)
#   - Presses Down + Tab to insert clickable mention
#   - Sends caption after mentions
  
#   IMPORTANT: Keep WhatsApp Desktop MAXIMIZED!
# =====================================================================
# """

# import pyautogui
# import pyperclip
# import time
# import os
# import json
# import re
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

# pyautogui.FAILSAFE = True
# pyautogui.PAUSE    = 0.3

# # ─────────────────────────────────────────────────────────────
# #  CLIPBOARD
# # ─────────────────────────────────────────────────────────────

# def copy_text(text):
#     pyperclip.copy(text)
#     time.sleep(0.3)

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

# def format_caption():
#     return (
#         "🚨 URGENT REMINDER 🚨\n\n"
#         "Important reminder that the RMA, XBM & TRADE-IN shipments "
#         "listed are still pending and are approaching the deadline ⏳\n\n"
#         "⚠️ Delayed shipment may result in chargebacks, so we kindly "
#         "request you to prioritize shipping these devices as soon as "
#         "possible 🚚📦\n\n"
#         "If you need any support, clarification, or assistance, please "
#         "feel free to reach out — we're here to help 🤝\n\n"
#         "✨"
#     )

# # ─────────────────────────────────────────────────────────────
# #  OPEN GROUP
# # ─────────────────────────────────────────────────────────────

# def open_group(group_name):
#     print(f"  🔍 Opening: {group_name}")
    
#     pyautogui.hotkey('ctrl', 'f')
#     time.sleep(1.5)
#     pyautogui.hotkey('ctrl', 'a')
#     time.sleep(0.3)
#     pyautogui.press('backspace')
#     time.sleep(0.3)
    
#     copy_text(group_name)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(2.5)
    
#     pyautogui.press('down')
#     time.sleep(0.5)
#     pyautogui.press('enter')
#     time.sleep(3.0)
    
#     print(f"  ✅ Opened")



# # def type_mention(dm):
#     """
#     Type a clickable @mention tag.
    
#     For multi-word names: Type first word, Tab to select, done.
#     The mention will show the full contact name automatically.
#     """
#     dm_name = dm.get('dmNameRep', '')
    
#     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
#         return False
    
#     clean_name = dm_name.strip().lstrip('~').strip()
#     if not clean_name:
#         return False
    
#     print(f"      @{clean_name}")
    
#     try:
#         # Step 1: Type @
#         pyautogui.write('@', interval=0.05)
#         time.sleep(1.5)
        
#         if ' ' in clean_name:
#             words = clean_name.split()
#             for i, word in enumerate(words):
#                 if i > 0:
#                     pyautogui.write(' ', interval=0.05)
#                     time.sleep(0.3)
#                 pyautogui.write(word, interval=0.05)
#                 time.sleep(0.5)
#             time.sleep(1.5)
#         else:
#             pyautogui.write(clean_name, interval=0.05)
#             time.sleep(2.0)
        
        
#         # Step 3: Press Tab to select FIRST suggestion
#         # WhatsApp will insert the FULL contact name
#         pyautogui.press('tab')
#         time.sleep(0.8)
        
#         return True
        
#     except Exception as e:
#         print(f"        ❌ Failed: {e}")
#         return False


# def type_mention(dm):
#     """
#     Type a clickable @mention tag.
    
#     FIX: Never type spaces - they close the popup!
#     Just type the first word, then Tab to select.
#     WhatsApp will insert the full contact name.
#     """
#     dm_name = dm.get('dmNameRep', '')
    
#     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
#         return False
    
#     clean_name = dm_name.strip().lstrip('~').strip()
#     if not clean_name:
#         return False
    
#     print(f"      @{clean_name}")
    
#     try:
#         # Step 1: Type @
#         pyautogui.write('@', interval=0.05)
#         time.sleep(1.5)
        
#         # Step 2: Type ONLY the first word (NO SPACES!)
#         # Spaces close the popup, so we never type them
#         first_word = clean_name.split()[0]
#         print(f"        Typing first word: '{first_word}'")
#         pyautogui.write(first_word, interval=0.05)
#         time.sleep(2.0)
        
#         # Step 3: Press Tab to select FIRST suggestion
#         # WhatsApp inserts the FULL contact name automatically
#         print(f"        Pressing Tab to select...")
#         pyautogui.press('tab')
#         time.sleep(0.8)
#         print(f"        ✅ Mention inserted")
        
#         return True
        
#     except Exception as e:
#         print(f"        ❌ Failed: {e}")
#         return False


# # ─────────────────────────────────────────────────────────────
# #  SEND ONE GROUP
# # ─────────────────────────────────────────────────────────────

# def send_reminder(group_data, idx, total):
#     name      = group_data.get('whatsapp_group', '')
#     img       = group_data.get('image', '')
#     count     = group_data.get('record_count', 0)
#     markets   = group_data.get('markets', [])
#     send_mode = group_data.get('send_mode', 'send_to_group')
#     dms       = group_data.get('dms', [])

#     print(f"\n{'─'*55}")
#     print(f"[{idx}/{total}] {name}  ({count} records)")
#     print(f"  Mode: {send_mode} | Markets: {', '.join(markets)}")

#     caption = format_caption()
    
#     tagged_dms = [
#         d for d in dms
#         if d.get('dmNameRep') and str(d.get('dmNameRep')).strip() not in ['','-','null','None']
#     ]
    
#     if tagged_dms:
#         names = [d['dmNameRep'] for d in tagged_dms]
#         print(f"  Tagging: {', '.join(names)}")
#     else:
#         print(f"  No DMs to tag")

#     if send_mode == "send_to_both_groups":
#         targets = ["Dallas Team South", "Dallas Team North"]
#     else:
#         targets = [name]

#     for target in targets:
#         print(f"\n  → {target}")
        
#         open_group(target)
#         time.sleep(1.0)
        
#         if img and os.path.exists(img):
#             print(f"    📎 Pasting image...")
#             copy_image(img)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(3.0)
            
#             if tagged_dms:
#                 print(f"    👥 Adding mentions...")
#                 for i, dm in enumerate(tagged_dms):
#                     type_mention(dm)
#                     if i < len(tagged_dms) - 1:
#                         pyautogui.write('  ', interval=0.05)
#                         time.sleep(0.3)
                
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
            
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(1.0)
            
#             pyautogui.press('enter')
#             time.sleep(3.0)
#             print(f"    ✅ Sent!")
#         else:
#             print(f"    📝 Text only...")
            
#             if tagged_dms:
#                 for i, dm in enumerate(tagged_dms):
#                     type_mention(dm)
#                     if i < len(tagged_dms) - 1:
#                         pyautogui.write('  ', interval=0.05)
#                         time.sleep(0.3)
                
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
#                 pyautogui.hotkey('shift', 'enter')
#                 time.sleep(0.2)
            
#             copy_text(caption)
#             pyautogui.hotkey('ctrl', 'v')
#             time.sleep(0.5)
#             pyautogui.press('enter')
#             time.sleep(2.0)
#             print(f"    ✅ Sent!")
        
#         print(f"  ✅ Done: {target}")
#         time.sleep(2.0)

# # ─────────────────────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────────────────────

# def main():
#     print("=" * 60)
#     print("  STEP 2 — Send WhatsApp Messages (Verified @Mentions)")
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
#     print("  1. WhatsApp Desktop OPEN and MAXIMIZED")
#     print("  2. Press Enter, click WhatsApp in 5 sec")
#     print("  3. Keep hands off mouse and keyboard")
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
#             print("\n🛑 Stopped by user")
#             break
#         except KeyboardInterrupt:
#             print("\n🛑 Stopped by Ctrl+C")
#             break
#         except Exception as e:
#             print(f"  ❌ Error: {e}")
#             import traceback
#             traceback.print_exc()
#             fail += 1
#             time.sleep(2)

#     print("\n" + "=" * 60)
#     print(f"✅ Sent   : {ok}")
#     print(f"❌ Failed : {fail}")
#     print(f"Total     : {total}")
#     print("=" * 60)
#     print(f"\n📱 Check WhatsApp groups for clickable @mentions!")
#     input("\nPress Enter to exit...")


# if __name__ == "__main__":
#     main()






"""
=====================================================================
  STEP 2 — SEND WHATSAPP MESSAGES (FIXED)
  RMA / XBM / Trade-in Pending Shipments
  
  FIXES:
  - Chat opening: removed Escape, added longer waits
  - @mentions: only type first word, then Tab
  - No spaces in mentions (they close popup)
  
  IMPORTANT: Keep WhatsApp Desktop MAXIMIZED!
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

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.5

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
#  OPEN GROUP - SIMPLE AND RELIABLE
# ─────────────────────────────────────────────────────────────

def open_group(group_name):
    """Open a WhatsApp group - simple approach"""
    print(f"  Opening: {group_name}")
    
    # Ctrl+F to search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(2.0)
    
    # Clear search
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)
    
    # Type group name
    copy_text(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    
    # Select first result
    pyautogui.press('down')
    time.sleep(0.5)
    
    # Open it
    pyautogui.press('enter')
    time.sleep(3.0)
    
    # DO NOT press Escape - it might close the chat
    print(f"  ✅ Opened")

# ─────────────────────────────────────────────────────────────
#  @MENTION - ONLY FIRST WORD, NO SPACES
# ─────────────────────────────────────────────────────────────

def type_mention(dm):
    """
    Type @ + first word of name, then Tab to select.
    NO SPACES - they close the popup!
    """
    dm_name = dm.get('dmNameRep', '')
    
    if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
        return False
    
    clean_name = dm_name.strip().lstrip('~').strip()
    if not clean_name:
        return False
    
    # Get first word only
    first_word = clean_name.split()[0]
    
    print(f"      @{first_word}")
    
    # Type @
    pyautogui.write('@', interval=0.05)
    time.sleep(1.5)
    
    # Type first word only
    pyautogui.write(first_word, interval=0.05)
    time.sleep(2.0)
    
    # Tab to select
    pyautogui.press('tab')
    time.sleep(0.8)
    
    return True

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

    if send_mode == "send_to_both_groups":
        targets = ["Dallas Team South", "Dallas Team North"]
    else:
        targets = [name]

    for target in targets:
        print(f"\n  → {target}")
        
        open_group(target)
        time.sleep(2.0)
        
        if img and os.path.exists(img):
            print(f"    Pasting image...")
            copy_image(img)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(3.0)
            
            if tagged_dms:
                print(f"    Adding mentions...")
                for i, dm in enumerate(tagged_dms):
                    type_mention(dm)
                    time.sleep(0.5)
                    if i < len(tagged_dms) - 1:
                        pyautogui.write('  ', interval=0.05)
                        time.sleep(0.5)
                
                time.sleep(0.5)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.3)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.3)
            
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)
            
            pyautogui.press('enter')
            time.sleep(3.0)
            print(f"    ✅ Sent!")
        else:
            print(f"    Text only...")
            
            if tagged_dms:
                for i, dm in enumerate(tagged_dms):
                    type_mention(dm)
                    time.sleep(0.5)
                    if i < len(tagged_dms) - 1:
                        pyautogui.write('  ', interval=0.05)
                        time.sleep(0.5)
                
                time.sleep(0.5)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.3)
                pyautogui.hotkey('shift', 'enter')
                time.sleep(0.3)
            
            copy_text(caption)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2.0)
            print(f"    ✅ Sent!")
        
        print(f"  ✅ Done: {target}")
        time.sleep(2.0)

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 2 — Send WhatsApp Messages")
    print("=" * 60)

    if not os.path.exists(METADATA_FILE):
        print("❌ Run STEP1 first!")
        input("Press Enter to exit...")
        return

    with open(METADATA_FILE) as f:
        group_list = json.load(f)

    total = len(group_list)
    print(f"Loaded {total} groups")

    # TEST FIRST GROUP ONLY
    test_groups = group_list[:1]
    
    print("\n" + "-" * 60)
    print("TESTING FIRST GROUP ONLY")
    print("-" * 60)
    input("Press Enter, then click WhatsApp...")

    print("\nClick WhatsApp NOW!")
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    print("\nGO!\n")

    for idx, group in enumerate(test_groups, 1):
        try:
            send_reminder(group, idx, len(test_groups))
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    print("\nDone! Check WhatsApp.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()