# """
# =====================================================================
#   UNIVERSAL WHATSAPP SENDER
#   Works with screenshots generated from ANY dataset!
  
#   Reads _group_list.json and sends with images + optional DM tags
# =====================================================================
# """

# import tkinter as tk
# from tkinter import ttk, messagebox, scrolledtext, filedialog
# import pyautogui
# import pyperclip
# import time
# import os
# import json
# import threading
# from PIL import Image
# import win32clipboard
# import win32con
# import io

# SETTINGS_FILE = "whatsapp_sender_settings.json"


# def load_settings():
#     defaults = {
#         "your_number": "",
#         "test_mode": True,
#         "start_from": 1,
#         "tag_dms": False,
#         "metadata_folder": "",
#     }
#     if os.path.exists(SETTINGS_FILE):
#         try:
#             with open(SETTINGS_FILE, 'r') as f:
#                 defaults.update(json.load(f))
#         except:
#             pass
#     return defaults


# def save_settings(s):
#     with open(SETTINGS_FILE, 'w') as f:
#         json.dump(s, f, indent=2)


# # ═══════════════════════════════════════════════════════════════
# #  WHATSAPP FUNCTIONS
# # ═══════════════════════════════════════════════════════════════

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


# def tag_mention(dm):
#     """Type @mention tag - returns True if successful, does NOT send"""
#     dm_name = dm.get('dmNameRep', '')
#     if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
#         return False
#     clean = dm_name.strip().lstrip('~').strip()
#     if not clean:
#         return False
    
#     # Type @ to trigger popup
#     pyautogui.write('@', interval=0.05)
#     time.sleep(0.8)
    
#     # Type the name
#     pyautogui.write(clean, interval=0.05)
#     time.sleep(1.5)
    
#     # Press Tab to select the mention (inserts it but doesn't send)
#     pyautogui.press('tab')
#     time.sleep(0.5)
    
#     return True


# # ═══════════════════════════════════════════════════════════════
# #  GUI
# # ═══════════════════════════════════════════════════════════════

# class WhatsAppSenderApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Universal WhatsApp Sender")
#         self.root.geometry("900x700")
        
#         self.settings = load_settings()
#         self.group_list = []
#         self.sending = False
        
#         self.build_ui()
    
#     def build_ui(self):
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         main_frame.columnconfigure(0, weight=1)
        
#         ttk.Label(main_frame, text="📱 Universal WhatsApp Sender", 
#                   font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=(0, 10))
        
#         # Metadata folder
#         meta_frame = ttk.LabelFrame(main_frame, text="Screenshots Folder", padding="10")
#         meta_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         self.meta_var = tk.StringVar(value=self.settings.get('metadata_folder', ''))
#         ttk.Entry(meta_frame, textvariable=self.meta_var, width=60).pack(side=tk.LEFT, padx=5)
#         ttk.Button(meta_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
#         ttk.Button(meta_frame, text="Load Groups", command=self.load_groups).pack(side=tk.LEFT, padx=5)
        
#         # Message
#         msg_frame = ttk.LabelFrame(main_frame, text="Message", padding="10")
#         msg_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
#         main_frame.rowconfigure(2, weight=1)
        
#         self.template_var = tk.StringVar(value="custom")
#         ttk.Radiobutton(msg_frame, text="RMA Reminder", variable=self.template_var, 
#                         value="rma", command=self.load_template).grid(row=0, column=0, padx=5)
#         ttk.Radiobutton(msg_frame, text="HINT Device", variable=self.template_var, 
#                         value="hint", command=self.load_template).grid(row=0, column=1, padx=5)
#         ttk.Radiobutton(msg_frame, text="Custom", variable=self.template_var, 
#                         value="custom").grid(row=0, column=2, padx=5)
        
#         self.msg_text = scrolledtext.ScrolledText(msg_frame, height=8)
#         self.msg_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
#         msg_frame.columnconfigure(0, weight=1)
#         msg_frame.rowconfigure(1, weight=1)
        
#         # Options
#         opt_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
#         opt_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         self.test_var = tk.BooleanVar(value=self.settings.get('test_mode', True))
#         ttk.Checkbutton(opt_frame, text="Test Mode", variable=self.test_var).grid(row=0, column=0, padx=5)
        
#         ttk.Label(opt_frame, text="Your Number:").grid(row=0, column=1, padx=5)
#         self.num_var = tk.StringVar(value=self.settings.get('your_number', ''))
#         ttk.Entry(opt_frame, textvariable=self.num_var, width=15).grid(row=0, column=2, padx=5)
        
#         self.tag_var = tk.BooleanVar(value=self.settings.get('tag_dms', False))
#         ttk.Checkbutton(opt_frame, text="Tag DMs", variable=self.tag_var).grid(row=0, column=3, padx=5)
        
#         ttk.Label(opt_frame, text="Start from #:").grid(row=0, column=4, padx=5)
#         self.start_var = tk.IntVar(value=self.settings.get('start_from', 1))
#         ttk.Spinbox(opt_frame, from_=1, to=100, textvariable=self.start_var, width=5).grid(row=0, column=5, padx=5)
        
#         # Groups list
#         grp_frame = ttk.LabelFrame(main_frame, text="Groups", padding="10")
#         grp_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
#         main_frame.rowconfigure(4, weight=1)
        
#         columns = ('#', 'Group', 'Records', 'Image', 'DMs')
#         self.tree = ttk.Treeview(grp_frame, columns=columns, show='headings', height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#         self.tree.column('#', width=40)
#         self.tree.column('Group', width=200)
#         self.tree.column('Records', width=60)
#         self.tree.column('Image', width=60)
#         self.tree.column('DMs', width=300)
#         self.tree.pack(fill=tk.BOTH, expand=True)
        
#         # Buttons
#         btn_frame = ttk.Frame(main_frame)
#         btn_frame.grid(row=5, column=0, pady=(10, 0))
        
#         self.send_btn = ttk.Button(btn_frame, text="🚀 SEND", command=self.start_sending)
#         self.send_btn.pack(side=tk.LEFT, padx=5)
        
#         self.stop_btn = ttk.Button(btn_frame, text="⏹ STOP", command=self.stop, state=tk.DISABLED)
#         self.stop_btn.pack(side=tk.LEFT, padx=5)
        
#         ttk.Button(btn_frame, text="💾 Save", command=self.save).pack(side=tk.LEFT, padx=5)
        
#         self.progress_var = tk.StringVar(value="Ready")
#         ttk.Label(btn_frame, textvariable=self.progress_var).pack(side=tk.RIGHT, padx=10)
        
#         # Log
#         log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
#         log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         main_frame.rowconfigure(6, weight=1)
        
#         self.log_text = scrolledtext.ScrolledText(log_frame, height=6, state=tk.DISABLED)
#         self.log_text.pack(fill=tk.BOTH, expand=True)
    
#     def log(self, msg):
#         self.log_text.configure(state=tk.NORMAL)
#         self.log_text.insert(tk.END, msg + "\n")
#         self.log_text.see(tk.END)
#         self.log_text.configure(state=tk.DISABLED)
#         self.root.update_idletasks()
    
#     def browse_folder(self):
#         folder = filedialog.askdirectory(title="Select Screenshots Folder")
#         if folder:
#             self.meta_var.set(folder)
    
#     def load_template(self):
#         self.msg_text.delete('1.0', tk.END)
#         t = self.template_var.get()
#         if t == "rma":
#             self.msg_text.insert('1.0', 
#                 "🚨 URGENT REMINDER 🚨\n\n"
#                 "Important reminder that the RMA, XBM & TRADE-IN shipments "
#                 "listed are still pending and are approaching the deadline ⏳\n\n"
#                 "⚠️ Delayed shipment may result in chargebacks, so we kindly "
#                 "request you to prioritize shipping these devices as soon as "
#                 "possible 🚚📦\n\n"
#                 "If you need any support, clarification, or assistance, please "
#                 "feel free to reach out — we're here to help 🤝\n\n"
#                 "✨"

                
#                 )
#             self.tag_var.set(True)
#         elif t == "hint":
#             self.msg_text.insert('1.0', "Greetings Store Team,\n\n"
#                 "If any store is experiencing issues with defective HINT or other devices, "
#                 "please have them reach out to us promptly with:\n\n"
#                 "• Pictures of the device with visible IMEI\n"
#                 "• EDGE history\n\nThank you!")
#             self.tag_var.set(False)
    
#     def load_groups(self):
#         folder = self.meta_var.get()
#         meta_file = os.path.join(folder, "_group_list.json")
        
#         if not os.path.exists(meta_file):
#             messagebox.showerror("Error", "_group_list.json not found in selected folder!")
#             return
        
#         with open(meta_file) as f:
#             self.group_list = json.load(f)
        
#         self.tree.delete(*self.tree.get_children())
#         for i, g in enumerate(self.group_list, 1):
#             img = "✅" if g.get('image') and os.path.exists(g['image']) else "❌"
#             dms = ', '.join([str(d.get('dmNameRep', '?')) for d in g.get('dms', [])[:5]])
#             self.tree.insert('', tk.END, values=(i, g['whatsapp_group'], g.get('record_count', 0), img, dms))
        
#         self.log(f"✅ Loaded {len(self.group_list)} groups")
    
#     def save(self):
#         self.settings.update({
#             'your_number': self.num_var.get(),
#             'test_mode': self.test_var.get(),
#             'start_from': self.start_var.get(),
#             'tag_dms': self.tag_var.get(),
#             'metadata_folder': self.meta_var.get(),
#         })
#         save_settings(self.settings)
#         self.log("💾 Saved!")
    
#     def start_sending(self):
#         if self.sending:
#             return
#         if not self.group_list:
#             messagebox.showerror("Error", "Load groups first!")
#             return
        
#         self.save()
#         self.sending = True
#         self.send_btn.configure(state=tk.DISABLED)
#         self.stop_btn.configure(state=tk.NORMAL)
        
#         thread = threading.Thread(target=self.send_all)
#         thread.daemon = True
#         thread.start()
    
#     def stop(self):
#         self.sending = False
    
#     # def send_all(self):
#     #     message = self.msg_text.get('1.0', tk.END).strip()
#     #     test_mode = self.test_var.get()
#     #     tag_dms = self.tag_var.get()
#     #     start_from = self.start_var.get()
#     #     your_number = self.num_var.get()
        
#     #     groups_to_send = self.group_list[start_from - 1:]
#     #     total = len(self.group_list)
#     #     ok = fail = 0
        
#     #     self.log(f"Starting: {len(groups_to_send)} groups")
        
#     #     for idx, group in enumerate(groups_to_send, start_from):
#     #         if not self.sending:
#     #             break
            
#     #         try:
#     #             name = group['whatsapp_group']
#     #             mode = group.get('send_mode', 'send_to_group')
#     #             dms = group.get('dms', []) if tag_dms else []
#     #             dm_images = group.get('dm_images', [])  # For Per DM mode
#     #             single_image = group.get('image', '')    # For Per Group mode
                
#     #             self.log(f"\n[{idx}/{total}] {name}")
#     #             self.progress_var.set(f"[{idx}/{total}] {name}")
                
#     #             # Determine targets
#     #             if test_mode:
#     #                 targets = [your_number]
#     #             elif mode == "send_to_both_groups":
#     #                 targets = ["Dallas Team South", "Dallas Team North"]
#     #             else:
#     #                 targets = [name]
                
#     #             # Send to each target
#     #             for target in targets:
#     #                 self.log(f"  → {target}")
#     #                 open_chat(target)
#     #                 time.sleep(1.0)
#     #                 focus_whatsapp()
#     #                 time.sleep(0.5)
                    
#     #                 # ═══════════════════════════════════════════
#     #                 #  PER DM MODE (Accessories): Multiple images
#     #                 # ═══════════════════════════════════════════
                    
#     #                 if dm_images:
#     #                     self.log(f"    📎 Sending {len(dm_images)} DM images...")
                        
#     #                     for dm_img in dm_images:
#     #                         dm_img_path = dm_img.get('image', '')
#     #                         dm_name = dm_img.get('name', '')
                            
#     #                         if not dm_img_path or not os.path.exists(dm_img_path):
#     #                             self.log(f"    ⚠️ Image missing for {dm_name}")
#     #                             continue
                            
#     #                         # Find this DM's tag info
#     #                         dm_tag_info = None
#     #                         if tag_dms:
#     #                             for d in dms:
#     #                                 if d.get('name') == dm_name:
#     #                                     dm_tag_info = d
#     #                                     break
                            
#     #                         # Tag the DM first
#     #                         if dm_tag_info:
#     #                             tag_mention(dm_tag_info)
#     #                             pyautogui.write(' ', interval=0.05)
#     #                             time.sleep(0.3)
                            
#     #                         # Send their image
#     #                         copy_image(dm_img_path)
#     #                         pyautogui.hotkey('ctrl', 'v')
#     #                         time.sleep(3.0)
#     #                         pyautogui.press('enter')
#     #                         time.sleep(2.0)
#     #                         self.log(f"      ✅ {dm_name}")
                        
#     #                     # Send the common message after all images
#     #                     if message:
#     #                         copy_text(message)
#     #                         pyautogui.hotkey('ctrl', 'v')
#     #                         time.sleep(1.0)
#     #                         pyautogui.press('enter')
#     #                         time.sleep(2.0)
                        
#     #                     self.log(f"    ✅ All {len(dm_images)} DMs sent")
                    
#     #                 # ═══════════════════════════════════════════
#     #                 #  PER GROUP MODE (RMA): Single image
#     #                 # ═══════════════════════════════════════════
                    
#     #                 else:
#     #                     tagged = 0
                        
#     #                     # Send single image
#     #                     if single_image and os.path.exists(single_image):
#     #                         copy_image(single_image)
#     #                         pyautogui.hotkey('ctrl', 'v')
#     #                         time.sleep(3.0)
#     #                         self.log(f"    📎 Image sent")
                        
#     #                     # Tag all DMs
#     #                     if dms and tag_dms:
#     #                         self.log(f"    👥 Tagging {len(dms)} DMs...")
#     #                         valid = [d for d in dms if d.get('dmNameRep') and str(d['dmNameRep']).strip() not in ['', '-', 'null', 'None']]
#     #                         for i, dm in enumerate(valid):
#     #                             if tag_mention(dm):
#     #                                 tagged += 1
#     #                                 if i < len(valid) - 1:
#     #                                     pyautogui.write('  ', interval=0.05)
#     #                                     time.sleep(0.2)
#     #                         if tagged > 0:
#     #                             pyautogui.press('enter')
#     #                             time.sleep(0.2)
#     #                             pyautogui.press('enter')
#     #                             time.sleep(0.3)
                        
#     #                     # Send message
#     #                     if message:
#     #                         copy_text(message)
#     #                         pyautogui.hotkey('ctrl', 'v')
#     #                         time.sleep(1.0)
#     #                         pyautogui.press('enter')
#     #                         time.sleep(2.0)
                        
#     #                     self.log(f"    ✅ Sent ({tagged} tags)")
                
#     #             ok += 1
#     #             self.settings['start_from'] = idx + 1
#     #             save_settings(self.settings)
#     #             time.sleep(2.0)
                
#     #         except pyautogui.FailSafeException:
#     #             self.log(f"\n🛑 ABORTED at group #{idx}")
#     #             self.log(f"   To resume, set Start from # = {idx}")
#     #             self.settings['start_from'] = idx
#     #             save_settings(self.settings)
#     #             break
#     #         except KeyboardInterrupt:
#     #             self.log(f"\n🛑 ABORTED at group #{idx}")
#     #             self.log(f"   To resume, set Start from # = {idx}")
#     #             self.settings['start_from'] = idx
#     #             save_settings(self.settings)
#     #             break
#     #         except Exception as e:
#     #             self.log(f"  ❌ Error: {e}")
#     #             import traceback
#     #             traceback.print_exc()
#     #             fail += 1
#     #             time.sleep(2)
        
#     #     self.root.after(0, self.done, ok, fail)
#     def send_all(self):
#         message = self.msg_text.get('1.0', tk.END).strip()
#         test_mode = self.test_var.get()
#         tag_dms = self.tag_var.get()
#         start_from = self.start_var.get()
#         your_number = self.num_var.get()
        
#         groups_to_send = self.group_list[start_from - 1:]
#         total = len(self.group_list)
#         ok = fail = 0
        
#         self.log(f"Starting: {len(groups_to_send)} groups")
        
#         for idx, group in enumerate(groups_to_send, start_from):
#             if not self.sending:
#                 break
            
#             try:
#                 name = group['whatsapp_group']
#                 mode = group.get('send_mode', 'send_to_group')
#                 dms = group.get('dms', []) if tag_dms else []
#                 dm_images = group.get('dm_images', [])
#                 single_image = group.get('image', '')
                
#                 self.log(f"\n[{idx}/{total}] {name}")
#                 self.progress_var.set(f"[{idx}/{total}] {name}")
                
#                 # Determine targets
#                 if test_mode:
#                     targets = [your_number]
#                 elif mode == "send_to_both_groups":
#                     targets = ["Dallas Team South", "Dallas Team North"]
#                 else:
#                     targets = [name]
                
#                 # Send to each target
#                 for target in targets:
#                     self.log(f"  → {target}")
#                     open_chat(target)
#                     time.sleep(1.0)
#                     focus_whatsapp()
#                     time.sleep(0.5)
                    
#                     # ═══════════════════════════════════════════
#                     #  PER DM MODE: Image + Caption (ONE message)
#                     #  Caption = @Tag + Text
#                     # ═══════════════════════════════════════════
                    
#                     if dm_images:
#                         total_sent = 0
                        
#                         for dm_img in dm_images:
#                             dm_img_path = dm_img.get('image', '')
#                             dm_name = dm_img.get('name', '')
                            
#                             if not dm_img_path or not os.path.exists(dm_img_path):
#                                 self.log(f"    ⚠️ Skipping {dm_name} - no image")
#                                 continue
                            
#                             # Find this DM's tag info
#                             dm_tag_info = None
#                             if tag_dms:
#                                 for d in dms:
#                                     if d.get('name') == dm_name:
#                                         dm_tag_info = d
#                                         break
                            
#                             # Build caption: @Tag + Message
#                             tag_part = ""
#                             if dm_tag_info:
#                                 clean_tag = dm_tag_info.get('dmNameRep', '').strip().lstrip('~').strip()
#                                 if clean_tag:
#                                     tag_part = f"@{clean_tag}"
                            
#                             if tag_part and message:
#                                 full_caption = f"{tag_part}\n\n{message}"
#                             elif tag_part:
#                                 full_caption = tag_part
#                             else:
#                                 full_caption = message if message else ""
                            
#                             # Step 1: Paste the image
#                             copy_image(dm_img_path)
#                             pyautogui.hotkey('ctrl', 'v')
#                             time.sleep(3.0)
                            
#                             # Step 2: Add caption text (image + caption = ONE message)
#                             if full_caption:
#                                 copy_text(full_caption)
#                                 pyautogui.hotkey('ctrl', 'v')
#                                 time.sleep(1.0)
                            
#                             # Step 3: Send as ONE message
#                             pyautogui.press('enter')
#                             time.sleep(2.0)
                            
#                             total_sent += 1
#                             self.log(f"      ✅ {dm_name}")
                        
#                         self.log(f"    ✅ {total_sent} messages sent")
                    
#                     # ═══════════════════════════════════════════
#                     #  PER GROUP MODE (RMA): Tags + Text + Image
#                     #  ALL IN ONE MESSAGE
#                     # ═══════════════════════════════════════════
                    
#                     else:
#                         tagged = 0
                        
#                         # Step 1: Tag all DMs (clickable mentions)
#                         if dms and tag_dms:
#                             valid = [d for d in dms if d.get('dmNameRep') and str(d['dmNameRep']).strip() not in ['', '-', 'null', 'None']]
#                             for i, dm in enumerate(valid):
#                                 if tag_mention(dm):
#                                     tagged += 1
#                                     if i < len(valid) - 1:
#                                         pyautogui.write(' ', interval=0.05)
#                                         time.sleep(0.2)
                            
#                             # Use Shift+Enter for newline (does NOT send the message)
#                             if tagged > 0:
#                                 pyautogui.hotkey('shift', 'enter')
#                                 time.sleep(0.2)
#                                 pyautogui.hotkey('shift', 'enter')
#                                 time.sleep(0.3)
                        
#                         # Step 2: Paste message text (adds to same input box)
#                         if message:
#                             copy_text(message)
#                             pyautogui.hotkey('ctrl', 'v')
#                             time.sleep(0.5)
                        
#                         # Step 3: Paste image (adds to same message)
#                         if single_image and os.path.exists(single_image):
#                             copy_image(single_image)
#                             pyautogui.hotkey('ctrl', 'v')
#                             time.sleep(3.0)
                        
#                         # Step 4: NOW send everything as ONE message
#                         pyautogui.press('enter')
#                         time.sleep(2.0)
                        
#                         self.log(f"    ✅ Sent ({tagged} tags + text + image in ONE message)")
                
#                 ok += 1
#                 self.settings['start_from'] = idx + 1
#                 save_settings(self.settings)
#                 time.sleep(2.0)
                
#             except pyautogui.FailSafeException:
#                 self.log(f"\n🛑 ABORTED at group #{idx}")
#                 self.log(f"   To resume, set Start from # = {idx}")
#                 self.settings['start_from'] = idx
#                 save_settings(self.settings)
#                 break
#             except KeyboardInterrupt:
#                 self.log(f"\n🛑 ABORTED at group #{idx}")
#                 self.log(f"   To resume, set Start from # = {idx}")
#                 self.settings['start_from'] = idx
#                 save_settings(self.settings)
#                 break
#             except Exception as e:
#                 self.log(f"  ❌ Error: {e}")
#                 import traceback
#                 traceback.print_exc()
#                 fail += 1
#                 time.sleep(2)
        
#         self.root.after(0, self.done, ok, fail)
     

#     def done(self, ok, fail):
#         self.sending = False
#         self.send_btn.configure(state=tk.NORMAL)
#         self.stop_btn.configure(state=tk.DISABLED)
#         self.progress_var.set(f"Done! {ok} sent, {fail} failed")


# def main():
#     root = tk.Tk()
#     app = WhatsAppSenderApp(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()







"""
=====================================================================
  UNIVERSAL WHATSAPP SENDER — COMPLETE & WORKING
  Handles ALL scenarios with proven tagging from STEP2.
  
  1. RMA mode: Image + clickable @tags + text (ONE message)
  2. Accessories: Per DM image + caption (ONE message each)
  3. Config mode: Clickable @tags + text only (ONE message)
  4. Text only: Just message, no tags, no images
=====================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import pyautogui
import pyperclip
import time
import os
import json
import threading
from PIL import Image
import win32clipboard
import win32con
import io

SETTINGS_FILE = "whatsapp_sender_settings.json"


def load_settings():
    defaults = {
        "your_number": "",
        "test_mode": True,
        "start_from": 1,
        "tag_dms": False,
        "metadata_folder": "",
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                defaults.update(json.load(f))
        except:
            pass
    return defaults


def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)


# ═══════════════════════════════════════════════════════════════
#  WHATSAPP HELPERS (same as working STEP2)
# ═══════════════════════════════════════════════════════════════

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


def open_chat(target):
    """Open a WhatsApp group by searching for it (working version)"""
    # Focus WhatsApp
    w, h = pyautogui.size()
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)
    copy_text(target)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)

    # Wait for results
    time.sleep(1.0)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3.0)  # Wait for chat to fully load


def type_verified_mention(dm):
    """
    Type a clickable @mention tag.
    EXACTLY the same as the working STEP2 version.
    Types @ + name, waits for popup, presses Tab to insert.
    Tab inserts the mention WITHOUT sending.
    """
    dm_name = dm.get('dmNameRep', '')
    if not dm_name or str(dm_name).strip() in ['', '-', 'null', 'None']:
        return False

    clean_name = dm_name.strip().lstrip('~').strip()
    if not clean_name:
        return False

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

        # Press Tab to insert the clickable mention (DOES NOT SEND)
        pyautogui.press('tab')
        time.sleep(0.5)

        w, h = pyautogui.size()
        pyautogui.click(w // 2, h - 100)
        time.sleep(0.3)

        return True

    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════
#  GUI APPLICATION
# ═══════════════════════════════════════════════════════════════

class WhatsAppSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal WhatsApp Sender")
        self.root.geometry("900x700")

        self.settings = load_settings()
        self.group_list = []
        self.sending = False

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="📱 Universal WhatsApp Sender",
                  font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=(0, 10))

        # Source frame
        source_frame = ttk.LabelFrame(main_frame, text="Load Groups From", padding="10")
        source_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Row 1: Screenshots folder
        folder_row = ttk.Frame(source_frame)
        folder_row.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(folder_row, text="Screenshots:").pack(side=tk.LEFT)
        self.meta_var = tk.StringVar(value=self.settings.get('metadata_folder', ''))
        ttk.Entry(folder_row, textvariable=self.meta_var, width=45).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_row, text="Browse", command=self.browse_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(folder_row, text="Load Groups", command=self.load_groups).pack(side=tk.LEFT, padx=2)

        # Row 2: From Config
        config_row = ttk.Frame(source_frame)
        config_row.pack(fill=tk.X)
        ttk.Label(config_row, text="OR").pack(side=tk.LEFT, padx=20)
        ttk.Button(config_row, text="📋 Load from CONFIG (Text + Tags only)",
                   command=self.load_from_config).pack(side=tk.LEFT, padx=5)
        ttk.Label(config_row, text="← No screenshots needed",
                  font=('Arial', 8)).pack(side=tk.LEFT, padx=5)

        # Message
        msg_frame = ttk.LabelFrame(main_frame, text="Message", padding="10")
        msg_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)

        self.template_var = tk.StringVar(value="custom")
        ttk.Radiobutton(msg_frame, text="RMA Reminder", variable=self.template_var,
                        value="rma", command=self.load_template).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(msg_frame, text="HINT Device", variable=self.template_var,
                        value="hint", command=self.load_template).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(msg_frame, text="Custom", variable=self.template_var,
                        value="custom").grid(row=0, column=2, padx=5)

        self.msg_text = scrolledtext.ScrolledText(msg_frame, height=8)
        self.msg_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        msg_frame.columnconfigure(0, weight=1)
        msg_frame.rowconfigure(1, weight=1)

        # Options
        opt_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        opt_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.test_var = tk.BooleanVar(value=self.settings.get('test_mode', True))
        ttk.Checkbutton(opt_frame, text="Test Mode", variable=self.test_var).grid(row=0, column=0, padx=5)

        ttk.Label(opt_frame, text="Your Number:").grid(row=0, column=1, padx=5)
        self.num_var = tk.StringVar(value=self.settings.get('your_number', ''))
        ttk.Entry(opt_frame, textvariable=self.num_var, width=15).grid(row=0, column=2, padx=5)

        self.tag_var = tk.BooleanVar(value=self.settings.get('tag_dms', False))
        ttk.Checkbutton(opt_frame, text="Tag DMs", variable=self.tag_var).grid(row=0, column=3, padx=5)

        ttk.Label(opt_frame, text="Start from #:").grid(row=0, column=4, padx=5)
        self.start_var = tk.IntVar(value=self.settings.get('start_from', 1))
        ttk.Spinbox(opt_frame, from_=1, to=100, textvariable=self.start_var, width=5).grid(row=0, column=5, padx=5)

        # Groups list
        grp_frame = ttk.LabelFrame(main_frame, text="Groups", padding="10")
        grp_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(4, weight=1)

        columns = ('#', 'Group', 'Records', 'Image', 'DMs')
        self.tree = ttk.Treeview(grp_frame, columns=columns, show='headings', height=8)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column('#', width=40)
        self.tree.column('Group', width=200)
        self.tree.column('Records', width=60)
        self.tree.column('Image', width=60)
        self.tree.column('DMs', width=300)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, pady=(10, 0))

        self.send_btn = ttk.Button(btn_frame, text="🚀 SEND", command=self.start_sending)
        self.send_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="⏹ STOP", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="💾 Save", command=self.save).pack(side=tk.LEFT, padx=5)

        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(btn_frame, textvariable=self.progress_var).pack(side=tk.RIGHT, padx=10)

        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(6, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.root.update_idletasks()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Screenshots Folder")
        if folder:
            self.meta_var.set(folder)

    def load_template(self):
        self.msg_text.delete('1.0', tk.END)
        t = self.template_var.get()
        if t == "rma":
            self.msg_text.insert('1.0',
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
            self.tag_var.set(True)
        elif t == "hint":
            self.msg_text.insert('1.0',
                "Greetings Store Team,\n\n"
                "If any store is experiencing issues with defective HINT or other devices, "
                "please have them reach out to us promptly with:\n\n"
                "• Pictures of the device with visible IMEI\n"
                "• EDGE history\n\nThank you!"
            )
            self.tag_var.set(False)

    def load_from_config(self):
        """Load groups directly from CONFIG_WhatsApp_Groups.py (no screenshots needed)"""
        try:
            from CONFIG_WhatsApp_Groups import WHATSAPP_GROUP_MAP, load_dm_contacts, get_dms_for_group

            dm_contacts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DM contacts.xlsx")
            dm_contacts = {}
            if os.path.exists(dm_contacts_file):
                dm_contacts = load_dm_contacts(dm_contacts_file)
                self.log(f"✅ Loaded DM contacts from file")

            # Build unique groups from config
            groups = {}
            for (market, district), info in WHATSAPP_GROUP_MAP.items():
                merge_key = info.get('merge_key')
                key = merge_key if merge_key else info.get('group')
                if key not in groups:
                    groups[key] = {
                        'whatsapp_group': info.get('group'),
                        'send_mode': info.get('mode', 'send_to_group'),
                        'markets': set(),
                    }
                groups[key]['markets'].add(market)

            self.group_list = []
            for key, data in sorted(groups.items()):
                all_dms = []
                seen_dms = set()
                for market in data['markets']:
                    for dm in get_dms_for_group(market, None, dm_contacts):
                        if dm['name'] not in seen_dms:
                            seen_dms.add(dm['name'])
                            all_dms.append({
                                'name': dm['name'],
                                'phone': dm.get('phone'),
                                'dmNameRep': dm.get('dmNameRep', dm['name']),
                            })

                self.group_list.append({
                    'whatsapp_group': data['whatsapp_group'],
                    'send_mode': data['send_mode'],
                    'dms': all_dms,
                    'dm_images': [],
                    'image': '',
                    'record_count': len(all_dms),
                })

            self.tree.delete(*self.tree.get_children())
            for i, g in enumerate(self.group_list, 1):
                dms = ', '.join([str(d.get('dmNameRep', '?')) for d in g.get('dms', [])[:5]])
                self.tree.insert('', tk.END, values=(i, g['whatsapp_group'], g.get('record_count', 0), 'N/A', dms))

            self.log(f"✅ Loaded {len(self.group_list)} groups from CONFIG (text + tags only)")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load from CONFIG:\n{e}")
            self.log(f"❌ {e}")

    def load_groups(self):
        """Load groups from _group_list.json (with screenshots)"""
        folder = self.meta_var.get()
        meta_file = os.path.join(folder, "_group_list.json")

        if not os.path.exists(meta_file):
            messagebox.showerror("Error", "_group_list.json not found in selected folder!")
            return

        with open(meta_file) as f:
            self.group_list = json.load(f)

        self.tree.delete(*self.tree.get_children())
        for i, g in enumerate(self.group_list, 1):
            dm_images = g.get('dm_images', [])
            if dm_images:
                has_images = all(os.path.exists(d.get('image', '')) for d in dm_images if d.get('image'))
                img_status = "✅" if has_images else "❌"
            else:
                single = g.get('image', '')
                img_status = "✅" if single and os.path.exists(single) else "❌"

            dms = ', '.join([str(d.get('dmNameRep', '?')) for d in g.get('dms', [])[:5]])
            self.tree.insert('', tk.END, values=(i, g['whatsapp_group'], g.get('record_count', 0), img_status, dms))

        self.log(f"✅ Loaded {len(self.group_list)} groups from screenshots folder")

    def save(self):
        self.settings.update({
            'your_number': self.num_var.get(),
            'test_mode': self.test_var.get(),
            'start_from': self.start_var.get(),
            'tag_dms': self.tag_var.get(),
            'metadata_folder': self.meta_var.get(),
        })
        save_settings(self.settings)
        self.log("💾 Saved!")

    def start_sending(self):
        if self.sending:
            return
        if not self.group_list:
            messagebox.showerror("Error", "Load groups first!")
            return

        self.save()
        self.sending = True
        self.send_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)

        thread = threading.Thread(target=self.send_all)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.sending = False

    # ═══════════════════════════════════════════════════════════
    #  MAIN SEND LOGIC – EXACT WORKING FLOW FROM STEP2
    # ═══════════════════════════════════════════════════════════

    def send_all(self):
        message = self.msg_text.get('1.0', tk.END).strip()
        test_mode = self.test_var.get()
        tag_dms = self.tag_var.get()
        start_from = self.start_var.get()
        your_number = self.num_var.get()

        groups_to_send = self.group_list[start_from - 1:]
        total = len(self.group_list)
        ok = fail = 0

        self.log(f"Starting: {len(groups_to_send)} groups")

        # 5‑second countdown
        self.log("⚠️ Switch to WhatsApp Desktop NOW!")
        for i in range(5, 0, -1):
            self.progress_var.set(f"Starting in {i}...")
            self.log(f"  {i}...")
            time.sleep(1)
        self.progress_var.set("GO!")
        self.log("GO!")

        for idx, group in enumerate(groups_to_send, start_from):
            if not self.sending:
                break

            try:
                name = group['whatsapp_group']
                mode = group.get('send_mode', 'send_to_group')
                dms = group.get('dms', []) if tag_dms else []
                dm_images = group.get('dm_images', [])
                single_image = group.get('image', '')

                # Valid DMs with dmNameRep
                valid_dms = []
                if dms:
                    valid_dms = [d for d in dms if d.get('dmNameRep') and str(d['dmNameRep']).strip() not in ['', '-', 'null', 'None']]

                self.log(f"\n[{idx}/{total}] {name}")
                self.progress_var.set(f"[{idx}/{total}] {name}")

                if test_mode:
                    targets = [your_number]
                elif mode == "send_to_both_groups":
                    targets = ["Dallas Team South", "Dallas Team North"]
                else:
                    targets = [name]

                for target in targets:
                    self.log(f"  → {target}")
                    open_chat(target)
                    time.sleep(1.0)

                    # Click input box once before starting
                    w, h = pyautogui.size()
                    pyautogui.click(w // 2, h - 100)
                    time.sleep(0.5)

                    # ----- PER DM MODE (Accessories) -----
                    if dm_images:
                        for dm_img in dm_images:
                            dm_img_path = dm_img.get('image', '')
                            dm_name = dm_img.get('name', '')
                            if not dm_img_path or not os.path.exists(dm_img_path):
                                continue

                            dm_tag = ""
                            if valid_dms:
                                for d in valid_dms:
                                    if d.get('name') == dm_name:
                                        rep = d.get('dmNameRep', '').strip().lstrip('~').strip()
                                        if rep:
                                            dm_tag = f"@{rep}"
                                        break

                            caption = ""
                            if dm_tag and message:
                                caption = f"{dm_tag}\n\n{message}"
                            elif dm_tag:
                                caption = dm_tag
                            elif message:
                                caption = message

                            pyautogui.click(w // 2, h - 100)
                            time.sleep(0.3)
                            copy_image(dm_img_path)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(3.0)

                            if caption:
                                copy_text(caption)
                                pyautogui.hotkey('ctrl', 'v')
                                time.sleep(1.0)

                            pyautogui.press('enter')
                            time.sleep(2.0)
                            self.log(f"      ✅ {dm_name}")

                        self.log(f"    ✅ {len(dm_images)} messages")

                    # ----- PER GROUP (RMA / text only) -----
                    else:
                        if single_image and os.path.exists(single_image):
                            # With image (RMA mode)
                            copy_image(single_image)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(3.0)

                            if valid_dms:
                                for dm in valid_dms:
                                    type_verified_mention(dm)
                                    # CRITICAL: manually add a space after each mention
                                    pyautogui.write(' ', interval=0.05)
                                    time.sleep(0.3)

                                # Click back to input box, then add newlines
                                pyautogui.click(w // 2, h - 100)
                                time.sleep(0.2)
                                pyautogui.hotkey('shift', 'enter')
                                time.sleep(0.2)
                                pyautogui.hotkey('shift', 'enter')
                                time.sleep(0.3)

                            if message:
                                copy_text(message)
                                pyautogui.hotkey('ctrl', 'v')
                                time.sleep(0.5)

                            pyautogui.press('enter')
                            time.sleep(3.0)
                            self.log(f"    ✅ Image + {len(valid_dms)} tags + text")

                        else:
                            # Text only
                            if valid_dms:
                                for dm in valid_dms:
                                    type_verified_mention(dm)
                                    pyautogui.write(' ', interval=0.05)
                                    time.sleep(0.3)

                                pyautogui.click(w // 2, h - 100)
                                time.sleep(0.2)
                                pyautogui.hotkey('shift', 'enter')
                                time.sleep(0.2)
                                pyautogui.hotkey('shift', 'enter')
                                time.sleep(0.3)

                            if message:
                                copy_text(message)
                                pyautogui.hotkey('ctrl', 'v')
                                time.sleep(0.5)

                            pyautogui.press('enter')
                            time.sleep(2.0)
                            self.log(f"    ✅ {len(valid_dms)} tags + text")

                ok += 1
                self.settings['start_from'] = idx + 1
                save_settings(self.settings)
                time.sleep(2.0)

            except pyautogui.FailSafeException:
                self.log(f"\n🛑 ABORTED at group #{idx}")
                self.settings['start_from'] = idx
                save_settings(self.settings)
                break
            except KeyboardInterrupt:
                self.log(f"\n🛑 ABORTED at group #{idx}")
                self.settings['start_from'] = idx
                save_settings(self.settings)
                break
            except Exception as e:
                self.log(f"  ❌ Error: {e}")
                import traceback
                traceback.print_exc()
                fail += 1
                time.sleep(2)

        self.root.after(0, self.done, ok, fail)
        def done(self, ok, fail):
            self.sending = False
            self.send_btn.configure(state=tk.NORMAL)
            self.stop_btn.configure(state=tk.DISABLED)
            self.progress_var.set(f"Done! {ok} sent, {fail} failed")


def main():
    root = tk.Tk()
    app = WhatsAppSenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()