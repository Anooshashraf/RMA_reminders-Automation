"""
=====================================================================
  TAB TIMING TEST - Find the right delay for Tab
=====================================================================
"""

import pyautogui
import pyperclip
import time

TEST_GROUP = "Boston-Maine"
TEST_NAME = "MA"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def copy_text(text):
    pyperclip.copy(text)
    time.sleep(0.3)

def open_group(group_name):
    print(f"Opening: {group_name}")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)
    copy_text(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3.0)
    print("✅ Opened")

def clear_input():
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('backspace')
    time.sleep(0.3)

def test_with_timing(down_delay, tab_delay):
    """Test Tab with specific delays"""
    clear_input()
    
    # Type @MA
    pyautogui.write('@', interval=0.05)
    time.sleep(1.5)
    pyautogui.write(TEST_NAME, interval=0.05)
    time.sleep(2.0)
    
    # Press Down
    pyautogui.press('down')
    print(f"  Down pressed, waiting {down_delay}s...")
    time.sleep(down_delay)
    
    # Press Tab
    print(f"  Tab pressed, waiting {tab_delay}s...")
    pyautogui.press('tab')
    time.sleep(tab_delay)
    
    # Check result
    print(f"  👀 Did it select @MA? (y/n): ", end="")
    result = input().lower()
    
    clear_input()
    return result == 'y'

def main():
    print("=" * 60)
    print("  TAB TIMING TEST")
    print("=" * 60)
    
    print(f"\nTesting in: {TEST_GROUP}")
    print(f"Name: @{TEST_NAME}")
    print("\nWe'll test different delays to find what works")
    
    input("\nPress Enter, click WhatsApp...")
    
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    print("\nGO!\n")
    
    open_group(TEST_GROUP)
    time.sleep(1.0)
    
    # Test different timing combinations
    tests = [
        (0.3, 0.3, "Fast Down, Fast Tab"),
        (0.5, 0.5, "Medium Down, Medium Tab"),
        (1.0, 0.5, "Slow Down, Medium Tab"),
        (0.5, 1.0, "Medium Down, Slow Tab"),
        (1.0, 1.0, "Slow Down, Slow Tab"),
        (0.3, 0.8, "Fast Down, Slow Tab"),
        (0.8, 0.3, "Slow Down, Fast Tab"),
    ]
    
    print("\n" + "=" * 60)
    print("Testing different timings...")
    print("=" * 60)
    
    working = []
    
    for down_delay, tab_delay, desc in tests:
        print(f"\n--- {desc} (Down:{down_delay}s, Tab:{tab_delay}s) ---")
        if test_with_timing(down_delay, tab_delay):
            print(f"  ✅ WORKS!")
            working.append((down_delay, tab_delay, desc))
        else:
            print(f"  ❌ Failed")
    
    print("\n" + "=" * 60)
    print("WORKING COMBINATIONS:")
    if working:
        for down, tab, desc in working:
            print(f"  ✅ {desc} (Down:{down}s, Tab:{tab}s)")
        print(f"\nUse these timings in the main script!")
    else:
        print("  None worked 😢")
        print("  Let's try WITHOUT pressing Down at all...")
        
        # Test without Down arrow
        print(f"\n--- TEST: No Down, just @MA then Tab ---")
        clear_input()
        pyautogui.write('@', interval=0.05)
        time.sleep(1.5)
        pyautogui.write(TEST_NAME, interval=0.05)
        time.sleep(2.0)
        # NO Down - just Tab
        pyautogui.press('tab')
        time.sleep(1.0)
        print("Did Tab without Down work? (y/n): ", end="")
        if input().lower() == 'y':
            print("✅ Works without Down!")
        else:
            print("Still doesn't work")
    
    print("=" * 60)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()