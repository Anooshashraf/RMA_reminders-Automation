"""
=====================================================================
  STEP 1 — GENERATE SCREENSHOTS
  RMA / XBM / Trade-in Pending Shipments
  
  UPDATED: Groups by WhatsApp Group, not individual DM
  
  HOW IT WORKS:
  - Reads WhatsApp group mapping from CONFIG_WhatsApp_Groups.py
  - Groups all rows by their WhatsApp group assignment
  - Special merging: ARIZONA all districts, DALLAS both groups, etc.
  - Saves one .png per WhatsApp group
  - Stores DM tagging info in _group_list.json
  
  Run this FIRST, then run STEP2_Send_WhatsApp.py
=====================================================================
"""

import win32com.client
import os
import time
from PIL import ImageGrab
import json
import re
from CONFIG_WhatsApp_Groups import get_group_for_market, load_dm_contacts, get_dms_for_group

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION — Update these for your machine
# ─────────────────────────────────────────────────────────────

EXCEL_FILE    = r"\\192.168.1.3\Inventory\Anoosha\RMA XBM Tradein-in Consolidated 2026.xlsx"
SHEET_NAME    = "Sheet1"
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")
DM_CONTACTS_FILE = os.path.join(BASE_DIR, "DM contacts.xlsx")

# Column letters matching your Excel
COL_MARKET   = "A"
COL_DISTRICT = "B"
COL_DM       = "C"
COL_STORE_ID = "D"
COL_STORE    = "E"
COL_DESC     = "F"
COL_IMEI     = "G"
COL_EMPLOYEE = "H"
COL_ASSURANT = "I"
COL_PROC_DT  = "J"
COL_LABEL    = "K"
COL_RMA_NUM  = "L"
COL_RMA_DATE = "M"
COL_COUNT    = "N"
COL_TRACKING = "O"
COL_STATUS   = "P"
COL_COST     = "Q"
COL_AGE      = "R"
COL_XBM      = "S"
COL_TYPE     = "T"

HEADER_ROW = 1

# ─────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def col_to_num(col_letter):
    result = 0
    for char in col_letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()

def normalize_name(name):
    """Normalize name for matching - remove special chars, extra spaces"""
    if not name:
        return ""
    # Remove special characters and extra spaces
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    name = ' '.join(name.split())
    return name.lower().strip()

# ─────────────────────────────────────────────────────────────
#  DM NAME MAPPING (for names that don't match exactly)
# ─────────────────────────────────────────────────────────────

DM_NAME_MAPPING = {
    # Main Excel Name → DM Contacts Name
    "Hamed Ali": "HAMED ALI SUFI SYED",
    "Hamza Ali": "Hamza Ali",
    "Akbar Uddin": "Akbar Uddin",
    "Abdullah Butt": "ABDULLAH BUTT",
    "Muhammad Farhan Asghar": "Muhammad Farhan Asghar",
    "Talha Qureshi": "TALHA QURESHI",
    "Hassan Saleem": "HASSAN SALEEM",
    "Kamaran Mohammed": "KAMRAN MOHAMMED",
    "SyedAli AhmedRizvi": "ALI RIZVI",
    "Muhammad Sumairuddin": "MOHAMMED SUMAIR",
    "Imran Ahmed Mohammed": "IMRAN AHMED MOHAMMED",
    "Imran Shaikh": "SHAIK MAZHAR UDDIN",
    "Salim Thanawala": "SALIM THANAWALA",
    "Ayyan Budwani": "AYAN BUDHWANI",
    "Muhammad Shoaib Sheeraz": "SHOAIB SHEERAZ",
    "MD Sunvee Bin Islam": "MD Sunvee Bin Islam",
    "Mohammed Anas": "Mohammed Anas",
    "MUHAMMAD AFZAL": "MUHAMMAD AFZAL",
    "Namir Elmouchantaf": "Namir Elmouchantaf",
    "Mukram Shareef Mohammed": "Mukram Shareef Mohammed",
    "SALMAN RIAZ": "SALMAN RIAZ",
    "Wajahat Ali Sattar Rajper": "Wajahat Ali Sattar Rajper",
    "ZUBAIR HUSSAIN": "ZUBAIR HUSSAIN",
    "ABDUL RAFAY ASHRAF": "ABDUL RAFAY ASHRAF",
    "MAAZ KHAN": "MAAZ KHAN",
    "SHARIK THOBANI": "Sharik Thobani",
    "SUBHAN ANSARI": "Subhan Ansari",
    "SHOAIB SHEERAZ": "Shoaib Sheeraz",
    "ZAID WASEEM": "Zaid Waseem",
    "SYED AMIR": "SYED AMIR",
    "Khaja Ameenuddin Ghori": "Khaja Ameenuddin Ghori",
    "MOHAMMED SUMAIR": "MOHAMMED SUMAIR",
    "SYEDALI AHMEDRIZVI": "SyedAli AhmedRizvi",
    "HASSAN TANVEER": "Hassan Tanveer",
    "UZAIR UDDIN": "Uzair Uddin",
    "Prabhakar Sivan": "Prabhakar Sivan",
    "ASLAM KHAN": "Aslam Khan",
    "Shahrukh Khalid": "SHAHRUKH KHALID",
    "HAFIZ ASAD BURGEES": "Hafiz Asad Burgees",
    "TALHA QURESHI": "Talha Qureshi",
    "HASSAN SALEEM": "Hassan Saleem",
    "KAMRAN MOHAMMED": "Kamran Mohammad",
    "Nur Rahman": "NUR RAHMAN",
    "Shoeb Naqvi": "SHOEB NAQVI",
    "HAMED ALI SUFI SYED": "Hamed Ali Sufi Syed",
    "Muhammad Sumairuddin": "MOHAMMED SUMAIRUDDIN",
    
}

# ─────────────────────────────────────────────────────────────
#  MAIN FUNCTION
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  STEP 1 — Generating WhatsApp Group Screenshots from Excel")
    print("=" * 70)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Load DM contacts for tagging info
    print("Loading DM contacts...")
    try:
        dm_contacts = load_dm_contacts(DM_CONTACTS_FILE)
        print(f"✅ Loaded {sum(len(v) for v in dm_contacts.values())} DMs")
    except Exception as e:
        print(f"⚠️  Could not load DM contacts: {e}")
        dm_contacts = {}

    # Clear previous screenshots and metadata to avoid duplicates
    try:
        removed = 0
        for fname in os.listdir(OUTPUT_FOLDER):
            if fname.lower().endswith('.png') or fname == '_group_list.json':
                try:
                    os.remove(os.path.join(OUTPUT_FOLDER, fname))
                    removed += 1
                except Exception as e:
                    print(f"  ⚠️ Could not remove {fname}: {e}")
        if removed:
            print(f"Cleared {removed} existing files from {OUTPUT_FOLDER}\n")
    except Exception as e:
        print(f"  ⚠️ Could not clear old screenshots: {e}\n")

    print("Launching Excel...")
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = True

    print(f"Opening: {EXCEL_FILE}")
    try:
        wb = excel.Workbooks.Open(EXCEL_FILE)
    except Exception as e:
        print(f"\n❌ Could not open file: {e}")
        print("   Check EXCEL_FILE path at top of script.")
        excel.Quit()
        input("\nPress Enter to exit...")
        return

    ws = wb.Sheets(SHEET_NAME)

    # ── Read all rows ─────────────────────────────────────────
    print("Reading data...")
    last_row = ws.Cells(ws.Rows.Count, col_to_num(COL_MARKET)).End(-4162).Row

    # Group by WhatsApp Group
    group_map = {}
    row_errors = []

    for row in range(HEADER_ROW + 1, last_row + 1):
        market   = str(ws.Cells(row, col_to_num(COL_MARKET)).Value  or "").strip()
        district = str(ws.Cells(row, col_to_num(COL_DISTRICT)).Value or "").strip()
        dm_name  = str(ws.Cells(row, col_to_num(COL_DM)).Value      or "").strip()

        if not market or not dm_name or market == "None":
            continue

        # Get WhatsApp group for this market/district
        group_info = get_group_for_market(market, district)
        if not group_info:
            row_errors.append(f"Row {row}: No WhatsApp group found for {market}/{district}")
            continue

        whatsapp_group = group_info.get('group')
        merge_key = group_info.get('merge_key')
        send_mode = group_info.get('mode')

        # Use merge_key if present, otherwise use group name
        group_key = merge_key if merge_key else whatsapp_group

        if group_key not in group_map:
            group_map[group_key] = {
                'whatsapp_group': whatsapp_group,
                'send_mode': send_mode,
                'rows': [],
                'markets': set(),
                'districts': set(),
                'dms': set(),
            }

        group_map[group_key]['rows'].append(row)
        group_map[group_key]['markets'].add(market)
        group_map[group_key]['districts'].add(district)
        group_map[group_key]['dms'].add(dm_name)

    if row_errors:
        print(f"\n⚠️  Found {len(row_errors)} rows with no group mapping:")
        for err in row_errors[:5]:
            print(f"   {err}")
        if len(row_errors) > 5:
            print(f"   ... and {len(row_errors) - 5} more")

    total = len(group_map)
    print(f"Found {total} unique WhatsApp groups\n")

    # Export full reminder columns: A through T
    START_COL = col_to_num('A')
    END_COL = col_to_num('T')
    SOURCE_RANGE_LEFT = col_to_num(COL_MARKET)
    SOURCE_RANGE_RIGHT = col_to_num(COL_TYPE)

    group_info_list = []

    # Add temp sheet for building table images
    try:
        excel.DisplayAlerts = False
        wb.Sheets("_TEMP_SS").Delete()
        excel.DisplayAlerts = True
    except:
        excel.DisplayAlerts = True

    excel.DisplayAlerts = False
    temp_ws = wb.Sheets.Add()
    temp_ws.Name = "_TEMP_SS"
    excel.DisplayAlerts = True

    for idx, (group_key, group_data) in enumerate(sorted(group_map.items()), 1):
        whatsapp_group = group_data['whatsapp_group']
        send_mode = group_data['send_mode']
        rows = group_data['rows']
        dms_in_group = group_data['dms']
        markets_in_group = group_data['markets']

        print(f"[{idx}/{total}] {whatsapp_group}")
        print(f"      Mode: {send_mode}")
        print(f"      Markets: {', '.join(sorted(markets_in_group))}")
        print(f"      DMs: {', '.join(sorted(dms_in_group))}")
        print(f"      Records: {len(rows)}\n")

        # Clear temp sheet
        temp_ws.Cells.Clear()

        # Copy source cells and formatting row-by-row
        src_cols = ws.Range(ws.Cells(HEADER_ROW, SOURCE_RANGE_LEFT), ws.Cells(HEADER_ROW, SOURCE_RANGE_RIGHT)).Columns.Count
        for target_row, src_row in enumerate(rows, 2):
            source_row_range = ws.Range(
                ws.Cells(src_row, SOURCE_RANGE_LEFT),
                ws.Cells(src_row, SOURCE_RANGE_RIGHT)
            )
            target_row_range = temp_ws.Range(
                temp_ws.Cells(target_row, 1),
                temp_ws.Cells(target_row, src_cols)
            )
            source_row_range.Copy(target_row_range)

            # Preserve long numeric identifiers as visible text in the screenshot
            for text_col in [COL_IMEI, COL_ASSURANT]:
                text_index = col_to_num(text_col) - SOURCE_RANGE_LEFT + 1
                try:
                    cell = temp_ws.Cells(target_row, text_index)
                    cell.NumberFormat = "@"
                    value = ws.Cells(src_row, col_to_num(text_col)).Text
                    cell.Value = value
                except Exception:
                    pass

        # Copy header row separately
        source_header_range = ws.Range(
            ws.Cells(HEADER_ROW, SOURCE_RANGE_LEFT),
            ws.Cells(HEADER_ROW, SOURCE_RANGE_RIGHT)
        )
        target_header_range = temp_ws.Range(
            temp_ws.Cells(1, 1),
            temp_ws.Cells(1, src_cols)
        )
        source_header_range.Copy(target_header_range)

        # Match source column widths and row heights
        for c in range(SOURCE_RANGE_LEFT, SOURCE_RANGE_RIGHT + 1):
            temp_ws.Columns(c - SOURCE_RANGE_LEFT + 1).ColumnWidth = ws.Columns(c).ColumnWidth
        temp_ws.Rows(1).RowHeight = ws.Rows(HEADER_ROW).RowHeight
        for target_row, src_row in enumerate(rows, 2):
            temp_ws.Rows(target_row).RowHeight = ws.Rows(src_row).RowHeight

        data_range = temp_ws.Range(
            temp_ws.Cells(1, 1),
            temp_ws.Cells(len(rows) + 1, src_cols)
        )

        # Increase screenshot legibility
        temp_ws.Application.ActiveWindow.Zoom = 115

        # Copy as picture to clipboard
        data_range.CopyPicture(Appearance=1, Format=2)
        time.sleep(0.8)

        # Save clipboard image
        safe_name = safe_filename(f"{whatsapp_group}")
        img_path  = os.path.join(OUTPUT_FOLDER, f"{safe_name}.png")

        try:
            img = ImageGrab.grabclipboard()
            if img:
                img.save(img_path, "PNG")
                print(f"  ✅ Saved: {os.path.basename(img_path)}")
            else:
                print(f"  ⚠️  Clipboard empty — retrying...")
                time.sleep(1)
                data_range.CopyPicture(Appearance=1, Format=2)
                time.sleep(1)
                img = ImageGrab.grabclipboard()
                if img:
                    img.save(img_path, "PNG")
                    print(f"  ✅ Saved on retry")
                else:
                    print(f"  ❌ Failed to capture image")
                    img_path = ""
        except Exception as e:
            print(f"  ❌ Image error: {e}")
            img_path = ""

        # ─────────────────────────────────────────────────────────────
        #  COLLECT DM INFO FOR TAGGING - WITH DISTRICT MATCHING
        # ─────────────────────────────────────────────────────────────

        dms_for_tagging = []
        for dm_name in sorted(dms_in_group):
            phone = None
            dm_name_rep = None
            normalized_dm_name = normalize_name(dm_name)
            
            print(f"    Looking for DM: '{dm_name}'")
            
            # Try to find DM in contacts - look across all markets and districts in this group
            for market in markets_in_group:
                if market not in dm_contacts:
                    continue
                
                # Check each district in this market
                for district, dms_in_district in dm_contacts[market].items():
                    # Try exact match first
                    if dm_name in dms_in_district:
                        contact_info = dms_in_district[dm_name]
                        phone = contact_info.get('phone', None)
                        dm_name_rep = contact_info.get('dmNameRep', None)
                        print(f"      ✅ Found in market: {market}, district: {district} → {dm_name_rep}")
                        break
                    
                    # Try case-insensitive match
                    found = False
                    for contact_name, contact_info in dms_in_district.items():
                        if dm_name.lower() == contact_name.lower():
                            phone = contact_info.get('phone', None)
                            dm_name_rep = contact_info.get('dmNameRep', None)
                            found = True
                            print(f"      ✅ Case-insensitive match in {market}/{district}: {dm_name} → {contact_name} → {dm_name_rep}")
                            break
                    
                    if found:
                        break
                    
                    # Try normalized match
                    found = False
                    for contact_name, contact_info in dms_in_district.items():
                        if normalize_name(contact_name) == normalized_dm_name:
                            phone = contact_info.get('phone', None)
                            dm_name_rep = contact_info.get('dmNameRep', None)
                            found = True
                            print(f"      ✅ Normalized match in {market}/{district}: {dm_name} → {contact_name} → {dm_name_rep}")
                            break
                    
                    if found:
                        break
                    
                    # Try partial match
                    found = False
                    for contact_name, contact_info in dms_in_district.items():
                        norm_contact = normalize_name(contact_name)
                        if (normalized_dm_name in norm_contact or 
                            norm_contact in normalized_dm_name):
                            phone = contact_info.get('phone', None)
                            dm_name_rep = contact_info.get('dmNameRep', None)
                            found = True
                            print(f"      ✅ Partial match in {market}/{district}: {dm_name} → {contact_name} → {dm_name_rep}")
                            break
                    
                    if found:
                        break
                
                if phone or dm_name_rep:
                    break
            
            if not dm_name_rep:
                print(f"      ❌ No match found for: {dm_name}")
            
            dms_for_tagging.append({
                "name": dm_name,
                "phone": phone,
                "dmNameRep": dm_name_rep
            })

        group_info_list.append({
            "whatsapp_group": whatsapp_group,
            "send_mode": send_mode,
            "image": img_path,
            "record_count": len(rows),
            "markets": list(markets_in_group),
            "dms": dms_for_tagging,
        })

        time.sleep(0.3)

    # Cleanup
    excel.DisplayAlerts = False
    try:
        temp_ws.Delete()
    except:
        pass
    excel.DisplayAlerts = True
    wb.Close(SaveChanges=False)
    excel.Quit()

    # Save group metadata for Step 2
    list_path = os.path.join(OUTPUT_FOLDER, "_group_list.json")
    with open(list_path, "w") as f:
        json.dump(group_info_list, f, indent=2, default=str)

    print(f"\n{'='*70}")
    print(f"✅ Done! {total} screenshots saved to:")
    print(f"   {OUTPUT_FOLDER}")
    print(f"\nMetadata saved to: _group_list.json")
    print(f"\nNow run STEP2_Send_WhatsApp.py")
    print(f"{'='*70}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()