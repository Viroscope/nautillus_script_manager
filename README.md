A simple yet powerful GUI tool for Linux users to **enable/disable/edit Nautilus context menu scripts** (Nautilus "Scripts" feature). With live updates, easy permission toggling, and direct integration with VSCode or VSCode Insiders for script creation and editing.

## Features

1. **List all Nautilus Scripts** in `~/.local/share/nautilus/scripts`
2. **Enable or disable scripts** by toggling executable permissions (`chmod +x/-x`)
3. **Edit/create scripts easily** — open the scripts folder in VSCode or VSCode Insiders with one click
4. **Auto-refresh script list** when files are added/removed/renamed (using `watchdog`)
5. **Set your preferred code editor:** If VSCode is not found, choose your own!
6. **Lightweight PyQt5 GUI** – intuitive and simple

## Prerequisites

- Python 3.7+
- Nautilus (GNOME Files) on Linux

## Installation

First, install dependencies:

```bash
pip3 install PyQt5 watchdog
```

## Usage

1. **Clone or download this repo:**
    ```bash
    git clone https://github.com/Viroscope/nautilus_script_manager.git
    cd nautilus_script_manager
    ```

2. **Run the manager:**
    ```bash
    python3 main.py
    ```

### What you can do

- See all your Nautilus scripts and check/uncheck to enable/disable.
- Click **"Create/Edit Scripts in VSCode"** to start coding new scripts, or edit existing ones.
- If VSCode isn't installed or found, you'll be prompted to pick any editor executable.

## Configuration

The location of your code editor is stored in:

```
~/.config/nautilus_scripts_manager.conf
```

You can edit or delete this file to reset your choice.

## Why?

The default "Scripts" feature in Nautilus is hidden under a submenu and doesn't let you easily manage which scripts are enabled. With this app, you have one-click control for permission toggling and editing—making your custom Nautilus scripts easier to manage than ever.

## Advanced

- Supports any code editor—just select its executable if VSCode is missing.
- Instantly reflects file changes in the scripts folder: add or remove scripts, and the UI updates.

## Troubleshooting

- If the script list doesn't update instantly, press **"Refresh List"**.
- If you switch code editors, delete `~/.config/nautilus_scripts_manager.conf`.
- You must have write and execute permission to the scripts folder.

## License

MIT License

## Contributing

Pull requests are welcome! If you have suggestions or want more advanced features (icons, drag-drop, scripts from templates), open an issue or PR.

---
