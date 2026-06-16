"""
=====================================================================
  WHATSAPP GROUP & DM MAPPING CONFIGURATION
  
  Maps Market/District combinations to:
  - WhatsApp group names
  - Send modes (tag all DMs vs send to group)
  - DM names to tag/mention
=====================================================================
"""

import openpyxl
import json

# ─────────────────────────────────────────────────────────────
#  WHATSAPP GROUP MAPPING
# ─────────────────────────────────────────────────────────────

WHATSAPP_GROUP_MAP = {
    # Format: (Market, District) → {whatsapp_group, send_mode, special_handling}
    
    # ARIZONA - All districts in one group, tag all DMs
    ("ARIZONA", "West"):                {"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    ("ARIZONA", "Central"):             {"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    ("ARIZONA", "Central /South Valley"):{"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    ("ARIZONA", "East"):                {"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    ("ARIZONA", ""):                    {"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    ("ARIZONA", None):                  {"group": "ARIZONA SUPPORT", "mode": "tag_all_dms", "merge_key": "ARIZONA_ALL"},
    
    # HOUSTON - Different groups per district
    ("HOUSTON", "South"):               {"group": "SOUTH DISTRICT - HOUSTON", "mode": "send_to_group"},
    ("HOUSTON", "Central"):             {"group": "CENTRAL DISTRICT - HOUSTON", "mode": "send_to_group"},
    ("HOUSTON", "North"):               {"group": "NORTH DISTRICT - HOUSTON", "mode": "send_to_group"},
    ("HOUSTON", "Airline"):             {"group": "AIRLINE DISTRICT - HOUSTON", "mode": "send_to_group"},
    ("HOUSTON", "East"):                {"group": "EAST DISTRICT - HOUSTON", "mode": "send_to_group"},
    
    # LOS ANGELES - Different groups per district
    ("LOS ANGELES", "EAST"):            {"group": "LOS ANGELES - EAST", "mode": "send_to_group"},
    ("LOS ANGELES", "North"):           {"group": "LOS ANGELES - NORTH", "mode": "send_to_group"},
    ("LOS ANGELES", "san Bernardino"):  {"group": "LOS ANGELES - san Bernardino", "mode": "send_to_group"},
    ("LOS ANGELES", "CENTRAL"):         {"group": "LOS ANGELES - CENTRAL", "mode": "send_to_group"},
    
    # MEMPHIS & ARKANSAS - Multiple groups
    ("MEMPHIS", "Central"):             {"group": "Memphis Team Central", "mode": "send_to_group"},
    ("MEMPHIS", "South"):               {"group": "Memphis Team South", "mode": "send_to_group"},
    ("MEMPHIS", "North"):               {"group": "Memphis Team North", "mode": "send_to_group"},
    ("ARKANSAS", "Central"):            {"group": "Memphis Team Central", "mode": "send_to_group"},
    
    # BAY AREA - Multiple groups
    ("BAY AREA", ""):                   {"group": "Bay Area Core", "mode": "send_to_group"},
    ("BAY AREA", None):                 {"group": "Bay Area Core", "mode": "send_to_group"},
    ("EAST BAY AREA", ""):              {"group": "East Bay Area", "mode": "send_to_group"},
    ("EAST BAY AREA", None):            {"group": "East Bay Area", "mode": "send_to_group"},
    ("NORTH BAY AREA", ""):             {"group": "North Bay Area- Main", "mode": "send_to_group"},
    ("NORTH BAY AREA", None):           {"group": "North Bay Area- Main", "mode": "send_to_group"},
    
    # BOSTON
    ("BOSTON", ""):                     {"group": "Boston-Maine", "mode": "send_to_group"},
    ("BOSTON", None):                   {"group": "Boston-Maine", "mode": "send_to_group"},
    
    # CHARLOTTE
    ("CHARLOTTE", ""):                  {"group": "Charlotte-Support", "mode": "send_to_group"},
    ("CHARLOTTE", None):                {"group": "Charlotte-Support", "mode": "send_to_group"},
    
    # COLORADO - Multiple groups
    ("COLORADO", "Southside Denver"):   {"group": "Southside Denver", "mode": "send_to_group"},
    ("COLORADO", "Northside Denver"):   {"group": "Northside Denver", "mode": "send_to_group"},
    
    # DALLAS - Both groups get complete data
    ("DALLAS", ""):                     {"group": "DALLAS_BOTH", "mode": "send_to_both_groups", "merge_key": "DALLAS_ALL"},
    ("DALLAS", None):                   {"group": "DALLAS_BOTH", "mode": "send_to_both_groups", "merge_key": "DALLAS_ALL"},
    
    # EL PASO
    ("EL PASO", ""):                    {"group": "EL PASO-LAS CRUCES MAIN", "mode": "send_to_group"},
    ("EL PASO", None):                  {"group": "EL PASO-LAS CRUCES MAIN", "mode": "send_to_group"},
    
    # FLORIDA, KENTUCKY, NASHVILLE - Shared group
    ("FLORIDA", ""):                    {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    ("FLORIDA", None):                  {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    ("KENTUCKY", ""):                   {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    ("KENTUCKY", None):                 {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    ("NASHVILLE", ""):                  {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    ("NASHVILLE", None):                {"group": "NASHVILLE - SUPPORT", "mode": "send_to_group", "merge_key": "NASHVILLE_REGION"},
    
    # GEORGIA
    ("GEORGIA", ""):                    {"group": "ATLANTA TEAM", "mode": "send_to_group"},
    ("GEORGIA", None):                  {"group": "ATLANTA TEAM", "mode": "send_to_group"},
    
    # NORTH CAROLINA - Multiple groups
    ("NORTH CAROLINA", "Durham"):       {"group": "NC- Durham", "mode": "send_to_group"},
    ("NORTH CAROLINA", "Raleigh West"): {"group": "NC-Raleigh West", "mode": "send_to_group"},
    ("NORTH CAROLINA", "Raleigh East"): {"group": "NC-Raleigh East", "mode": "send_to_group"},
    ("NORTH CAROL", "Durham"):          {"group": "NC- Durham", "mode": "send_to_group"},
    ("NORTH CAROL", "Raleigh West"):    {"group": "NC-Raleigh West", "mode": "send_to_group"},
    ("NORTH CAROL", "Raleigh East"):    {"group": "NC-Raleigh East", "mode": "send_to_group"},
    
    # OKLAHOMA
    ("OKLAHOMA", ""):                   {"group": "Oklahoma Core", "mode": "send_to_group"},
    ("OKLAHOMA", None):                 {"group": "Oklahoma Core", "mode": "send_to_group"},
    
    # OREGON
    ("OREGON", ""):                     {"group": "Portland Oregon Main", "mode": "send_to_group"},
    ("OREGON", None):                   {"group": "Portland Oregon Main", "mode": "send_to_group"},
    
    # PALMDALE/OXNARD - IMPORTANT: Your existing logic merges these
    ("PALMDALE", ""):                   {"group": "Portland Oregon Main", "mode": "send_to_group"},
    ("PALMDALE", None):                 {"group": "Portland Oregon Main", "mode": "send_to_group"},
    ("OXNARD", ""):                     {"group": "Portland Oregon Main", "mode": "send_to_group"},
    ("OXNARD", None):                   {"group": "Portland Oregon Main", "mode": "send_to_group"},
    
    # PALM BEACH
    ("PALM BEACH", ""):                 {"group": "MIAMI - Support", "mode": "send_to_group"},
    ("PALM BEACH", None):               {"group": "MIAMI - Support", "mode": "send_to_group"},
    
    # PHILADELPHIA
    ("PHILADELPHIA", ""):               {"group": "Philadelphia Support", "mode": "send_to_group"},
    ("PHILADELPHIA", None):             {"group": "Philadelphia Support", "mode": "send_to_group"},
    
    # SACRAMENTO - All DMs in single group
    ("SACRAMENTO", ""):                 {"group": "Sacramento Main", "mode": "send_to_group", "merge_key": "SACRAMENTO_ALL"},
    ("SACRAMENTO", None):               {"group": "Sacramento Main", "mode": "send_to_group", "merge_key": "SACRAMENTO_ALL"},
    
    # SAN DIEGO & SAN FRANCISCO - Shared group
    ("SAN DIEGO", ""):                  {"group": "SAN DIEGO CORE", "mode": "send_to_group", "merge_key": "SAN_DIEGO_REGION"},
    ("SAN DIEGO", None):                {"group": "SAN DIEGO CORE", "mode": "send_to_group", "merge_key": "SAN_DIEGO_REGION"},
    ("SAN FRANCISCO", ""):              {"group": "SAN DIEGO CORE", "mode": "send_to_group", "merge_key": "SAN_DIEGO_REGION"},
    ("SAN FRANCISCO", None):            {"group": "SAN DIEGO CORE", "mode": "send_to_group", "merge_key": "SAN_DIEGO_REGION"},
    
    # UTAH
    ("UTAH", ""):                       {"group": "Utah Support", "mode": "send_to_group"},
    ("UTAH", None):                     {"group": "Utah Support", "mode": "send_to_group"},
}

# Special group handling
SPECIAL_GROUP_CONFIGS = {
    "ARIZONA_ALL": {
        "groups": ["ARIZONA SUPPORT"],
        "mode": "tag_all_dms",
        "description": "All Arizona DMs tagged in single reminder"
    },
    "DALLAS_ALL": {
        "groups": ["Dallas Team South", "Dallas Team North"],
        "mode": "send_to_both_groups",
        "description": "Complete data sent to both Dallas groups"
    },
    "NASHVILLE_REGION": {
        "groups": ["NASHVILLE - SUPPORT"],
        "mode": "send_to_group",
        "description": "Shared group for Nashville region"
    },
    "SAN_DIEGO_REGION": {
        "groups": ["SAN DIEGO CORE"],
        "mode": "send_to_group",
        "description": "Shared group for San Diego region"
    },
    "SACRAMENTO_ALL": {
        "groups": ["Sacramento Main"],
        "mode": "send_to_group",
        "description": "All Sacramento DMs in single reminder"
    }
}


# ─────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def get_group_for_market(market, district):
    """
    Get WhatsApp group info for a given market/district.
    Handles various district formats (None, "", normalized names).
    """
    # Normalize district
    if not district:
        district = ""
    district = str(district).strip()
    
    # Try exact match
    key = (market.upper(), district)
    if key in WHATSAPP_GROUP_MAP:
        return WHATSAPP_GROUP_MAP[key]
    
    # Try with empty district
    key = (market.upper(), "")
    if key in WHATSAPP_GROUP_MAP:
        return WHATSAPP_GROUP_MAP[key]
    
    # Not found
    return None


def load_dm_contacts(dm_contacts_file):
    """
    Load DM contact information from Excel file.
    Returns dict: {market: {dm_name: phone_number}}
    """
    wb = openpyxl.load_workbook(dm_contacts_file)
    ws = wb.active
    
    dm_contacts = {}
    
    for row in range(2, ws.max_row + 1):
        market = str(ws.cell(row, 1).value or "").strip()
        name = str(ws.cell(row, 2).value or "").strip()
        phone = str(ws.cell(row, 6).value or "").strip()
        
        if not market or not name:
            continue
        
        if market not in dm_contacts:
            dm_contacts[market] = {}
        
        dm_contacts[market][name] = phone
    
    return dm_contacts


def get_dms_for_group(market, whatsapp_group, dm_contacts):
    """
    Get list of DMs that belong to a specific WhatsApp group.
    Returns list of (dm_name, phone_number) tuples.
    """
    dms_in_market = dm_contacts.get(market, {})
    
    result = []
    for dm_name, phone in dms_in_market.items():
        if phone:  # Only include if phone number exists
            result.append((dm_name, phone))
    
    return result


if __name__ == "__main__":
    # Test the config
    print("Testing WhatsApp group mapping...\n")
    
    test_cases = [
        ("ARIZONA", "West"),
        ("ARIZONA", "Central"),
        ("HOUSTON", "South"),
        ("DALLAS", ""),
        ("MEMPHIS", "North"),
    ]
    
    for market, district in test_cases:
        result = get_group_for_market(market, district)
        print(f"{market:15} | {district:20} → {result}")
