# MH3U Save File Editor

A desktop save file editor for **Monster Hunter 3 Ultimate (MH3U)**, built with Python and Tkinter. Allows you to view and modify player data, item boxes, and equipment boxes directly in your save file.

## Features

- **Player Info** — Change your hunter's name and Zenny (in-game currency) amount
- **Item Box** — Browse and modify items across 10 pages (1,000 item slots), including item type and quantity
- **Equipment Box** — Browse and swap equipment pieces across 10 pages (1,000 equipment slots)
- Open and save files with standard file dialogs, including Save As support

## Requirements

- Python 3.x
- Tkinter (included with most Python distributions)

## Installation

```bash
git clone https://github.com/your-username/mh3u-save-editor.git
cd mh3u-save-editor
```

No additional dependencies are required.

## Usage

```bash
python MH3U_Save_Editor.py
```

1. Launch the application
2. Go to **File → Open File** and select your MH3U save file
3. Edit player info, items, or equipment using the tabs
4. Go to **File → Save File** to overwrite the original, or **File → Save As...** to write a new file

> **Tip:** It's recommended to back up your save file before making any edits.

## Project Structure

```
mh3u-save-editor/
├── MH3U_Save_Editor.py       # Main application entry point (UI)
├── fileEditAPI/
│   ├── __init__.py
│   └── saveEditorAPI.py      # Core read/write logic for the save file
└── data/
    ├── __init__.py
    ├── globalData.py         # Shared state and byte offsets
    ├── offsets.py            # Save file byte offset constants
    ├── itemCodes.py          # Item name ↔ hex code mappings
    └── equipmentCodes.py     # Equipment name ↔ hex code mappings
```

## Save File Format (Known Offsets)

| Field          | Offset | Size    |
|----------------|--------|---------|
| Player Name    | 43     | 10 bytes |
| Zenny Amount   | 73     | 3 bytes  |
| Item Box       | 432    | 4 bytes/slot |
| Equipment Box  | 4432   | 16 bytes/slot |