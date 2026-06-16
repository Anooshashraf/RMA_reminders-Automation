"""
Quick reference: WhatsApp Group Mappings

This script generates a human-readable mapping of which markets/districts
go to which WhatsApp groups. Use this to verify your setup.
"""

from CONFIG_WhatsApp_Groups import WHATSAPP_GROUP_MAP, SPECIAL_GROUP_CONFIGS

def generate_group_reference():
    """Generate a readable reference of all mappings."""
    
    # Group by WhatsApp group name
    groups_by_name = {}
    
    for (market, district), config in WHATSAPP_GROUP_MAP.items():
        group_name = config.get('group')
        send_mode = config.get('mode')
        merge_key = config.get('merge_key')
        
        if group_name not in groups_by_name:
            groups_by_name[group_name] = {
                'markets': [],
                'mode': send_mode,
                'merge_key': merge_key
            }
        
        groups_by_name[group_name]['markets'].append((market, district, send_mode))
    
    return groups_by_name

def print_reference():
    """Print formatted reference."""
    
    print("\n" + "="*80)
    print("WHATSAPP GROUP - MARKET MAPPING REFERENCE")
    print("="*80 + "\n")
    
    groups = generate_group_reference()
    
    # Sort by group name
    for group_name in sorted(groups.keys()):
        group_data = groups[group_name]
        markets = group_data['markets']
        mode = group_data['mode']
        merge_key = group_data['merge_key']
        
        print(f"📱 GROUP: {group_name}")
        print(f"   Mode: {mode}")
        if merge_key:
            print(f"   Merge Key: {merge_key}")
        print(f"   Records:")
        
        # Group markets by base name
        unique_markets = set((m, d if d else "") for m, d, _ in markets)
        for market, district in sorted(unique_markets):
            if district:
                print(f"     • {market} - {district}")
            else:
                print(f"     • {market}")
        
        print()
    
    print("="*80)
    print("\nLEGEND:")
    print("  tag_all_dms      → Group receives all data, each DM tagged individually")
    print("  send_to_group    → Group receives district/market specific data")
    print("  send_to_both_groups → Special case (Dallas) sends to multiple groups")
    print("="*80 + "\n")

def count_statistics():
    """Print statistics."""
    
    groups = generate_group_reference()
    
    print("\nSTATISTICS:")
    print(f"  Total WhatsApp Groups: {len(groups)}")
    
    tag_all = len([g for g, d in groups.items() if d['mode'] == 'tag_all_dms'])
    send_group = len([g for g, d in groups.items() if d['mode'] == 'send_to_group'])
    send_both = len([g for g, d in groups.items() if d['mode'] == 'send_to_both_groups'])
    
    print(f"  Groups with DM tagging: {tag_all}")
    print(f"  Groups send-to-group: {send_group}")
    print(f"  Groups send-to-both: {send_both}")
    print()

if __name__ == "__main__":
    print_reference()
    count_statistics()
