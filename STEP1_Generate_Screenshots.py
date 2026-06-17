"""
=====================================================================
  STEP 1 — GENERATE SCREENSHOTS
  RMA / XBM / Trade-in Pending Shipments

  HOW IT WORKS:
  - Opens your Excel file using win32com (real Excel app)
  - Groups rows by DM NAME (across all their markets)
  - Special case: OXNARD + PALMDALE = same DM, merged into one image
  - Saves one .png per DM to the output folder

  Run this FIRST, then run STEP2_Send_WhatsApp.py
=====================================================================
"""

import win32com.client
import os
import time
from PIL import ImageGrab

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION — Update these for your machine
# ─────────────────────────────────────────────────────────────

EXCEL_FILE    = r"\\192.168.1.3\Inventory\Anoosha\RMA XBM Tradein-in Consolidated 2026.xlsx"
SHEET_NAME    = "Sheet1"
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "RMA_Screenshots")

# Column letters matching your Excel
COL_MARKET   = "A"
COL_DISTRICT = "B"
COL_DM       = "C"
COL_STORE_ID = "D"
COL_STORE    = "E"
COL_DESC     = "H"
COL_IMEI     = "I"
COL_EMPLOYEE = "J"
COL_ASSURANT = "K"
COL_PROC_DT  = "L"
COL_LABEL    = "M"
COL_RMA_NUM  = "N"
COL_RMA_DATE = "O"
COL_COUNT    = "P"
COL_TRACKING = "Q"
COL_STATUS   = "R"
COL_COST     = "S"
COL_AGE      = "T"
COL_XBM      = "U"
COL_TYPE     = "V"

HEADER_ROW = 1

# ── MARKET MERGE RULES ───────────────────────────────────────
# Markets listed here get merged into one DM entry.
# Key = canonical market name shown in the image title
# Value = list of market names in Excel that belong together

MERGE_MARKETS = {
    "OXNARD/PALMDALE": ["OXNARD", "PALMDALE"],
    # Add more merged markets here if needed:
    # "MARKET A / MARKET B": ["MARKET A", "MARKET B"],
}

# Build reverse lookup: Excel market name → canonical name
MARKET_CANONICAL = {}
for canonical, members in MERGE_MARKETS.items():
    for m in members:
        MARKET_CANONICAL[m.upper()] = canonical

# ─────────────────────────────────────────────────────────────

def col_to_num(col_letter):
    result = 0
    for char in col_letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()

def main():
    print("=" * 60)
    print("  STEP 1 — Generating DM Screenshots from Excel")
    print("=" * 60)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Clear previous screenshots and previous DM list to avoid duplicates
    try:
        removed = 0
        for fname in os.listdir(OUTPUT_FOLDER):
            if fname.lower().endswith('.png') or fname == '_dm_list.json':
                try:
                    os.remove(os.path.join(OUTPUT_FOLDER, fname))
                    removed += 1
                except Exception as e:
                    print(f"  ⚠️ Could not remove {fname}: {e}")
        if removed:
            print(f"Cleared {removed} existing files from {OUTPUT_FOLDER}")
    except Exception as e:
        print(f"  ⚠️ Could not clear old screenshots: {e}")

    print("\nLaunching Excel...")
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

    # Group by DM NAME (merge markets where needed)
    # dm_map key: (canonical_market, district, dm_name)
    # dm_map value: list of row numbers
    dm_map = {}

    for row in range(HEADER_ROW + 1, last_row + 1):
        market   = str(ws.Cells(row, col_to_num(COL_MARKET)).Value  or "").strip()
        district = str(ws.Cells(row, col_to_num(COL_DISTRICT)).Value or "").strip()
        dm_name  = str(ws.Cells(row, col_to_num(COL_DM)).Value      or "").strip()

        if not market or not dm_name or market == "None":
            continue

        # Resolve canonical market (merge OXNARD + PALMDALE etc.)
        canonical_market = MARKET_CANONICAL.get(market.upper(), market.upper())

        key = (canonical_market, district, dm_name)
        if key not in dm_map:
            dm_map[key] = []
        dm_map[key].append(row)

    total = len(dm_map)
    print(f"Found {total} unique DM groups\n")

    # Export full reminder columns: A through V and preserve source styling
    START_COL = col_to_num('A')
    END_COL = col_to_num('V')
    SHOW_COLS = list(range(START_COL, END_COL + 1))
    SOURCE_RANGE_LEFT = col_to_num(COL_MARKET)
    SOURCE_RANGE_RIGHT = col_to_num(COL_TYPE)

    dm_info_list = []

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

    for idx, ((canonical_market, district, dm_name), rows) in enumerate(dm_map.items(), 1):
        print(f"[{idx}/{total}] {dm_name} ({canonical_market}) — {len(rows)} devices")

        # Clear temp sheet
        temp_ws.Cells.Clear()

        # Copy source cells and formatting row-by-row so the screenshot matches the original sheet
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

        # Copy header row separately so it keeps the source header colors/weights
        source_header_range = ws.Range(
            ws.Cells(HEADER_ROW, SOURCE_RANGE_LEFT),
            ws.Cells(HEADER_ROW, SOURCE_RANGE_RIGHT)
        )
        target_header_range = temp_ws.Range(
            temp_ws.Cells(1, 1),
            temp_ws.Cells(1, src_cols)
        )
        source_header_range.Copy(target_header_range)

        # Match source column widths and row heights for a closer visual match
        for c in range(SOURCE_RANGE_LEFT, SOURCE_RANGE_RIGHT + 1):
            temp_ws.Columns(c - SOURCE_RANGE_LEFT + 1).ColumnWidth = ws.Columns(c).ColumnWidth
        temp_ws.Rows(1).RowHeight = ws.Rows(HEADER_ROW).RowHeight
        for target_row, src_row in enumerate(rows, 2):
            temp_ws.Rows(target_row).RowHeight = ws.Rows(src_row).RowHeight

        data_range = temp_ws.Range(
            temp_ws.Cells(1, 1),
            temp_ws.Cells(len(rows) + 1, src_cols)
        )

        # Increase screenshot legibility without changing the sheet content
        temp_ws.Application.ActiveWindow.Zoom = 115

        # Copy as picture to clipboard
        data_range.CopyPicture(Appearance=1, Format=2)
        time.sleep(0.8)

        # Save clipboard image
        safe_name = safe_filename(f"{canonical_market}_{dm_name}")
        img_path  = os.path.join(OUTPUT_FOLDER, f"{safe_name}.png")

        try:
            img = ImageGrab.grabclipboard()
            if img:
                img.save(img_path, "PNG")
                print(f"  ✅ Saved: {os.path.basename(img_path)}")
            else:
                print(f"  ⚠️  Clipboard empty for {dm_name} — retrying...")
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

        dm_info_list.append({
            "market":   canonical_market,
            "district": district,
            "dm_name":  dm_name,
            "image":    img_path,
            "count":    len(rows)
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

    # Save DM list for Step 2
    import json
    list_path = os.path.join(OUTPUT_FOLDER, "_dm_list.json")
    with open(list_path, "w") as f:
        json.dump(dm_info_list, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print(f"✅ Done! {total} screenshots saved to:")
    print(f"   {OUTPUT_FOLDER}")
    print(f"\nNow run STEP2_Send_WhatsApp.py")
    print(f"{'='*60}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
