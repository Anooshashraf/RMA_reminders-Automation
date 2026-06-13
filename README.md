# RMA Reminders Automation

Python automation for generating reminder screenshots from Excel and sending them through WhatsApp Desktop.

## Files

- `STEP1_Generate_Screenshots.py` - builds per-DM screenshots from the source Excel file and saves them to `RMA_Screenshots/`
- `STEP2_Send_WhatsApp.py` - sends the generated screenshots from `RMA_Screenshots/`
- `INSTALL_PACKAGES.bat` - installs the Python dependencies used by the scripts

## Requirements

- Windows
- Microsoft Excel installed
- WhatsApp Desktop installed and logged in
- Access to the Excel source file referenced in `STEP1_Generate_Screenshots.py`

## Setup

Run:

```bat
INSTALL_PACKAGES.bat
```

## Usage

1. Update the Excel path in `STEP1_Generate_Screenshots.py` if needed.
2. Run Step 1 to generate screenshots.
3. Run Step 2 to send them.

## Output

Generated screenshots are saved in `RMA_Screenshots/` next to the scripts.
