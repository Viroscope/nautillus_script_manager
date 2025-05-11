import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPTS_DIR = os.path.expanduser('~/.local/share/nautilus/scripts')
CONFIG_PATH = os.path.expanduser('~/.config/nautilus_scripts_manager.conf')

def read_vscode_path():
    # Try reading user-set path from config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            path = f.read().strip()
            if path and os.path.isfile(path) and os.access(path, os.X_OK):
                return path
    # Try defaults
    for default in ('/usr/bin/code-insiders', '/usr/bin/code'):
        if os.path.isfile(default) and os.access(default, os.X_OK):
            return default
    return None

def save_vscode_path(path):
    # Save the chosen path to the config file
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        f.write(path)

class ScriptEventHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_any_event(self, event):
        self.app.update_script_list()

class NautilusScriptsManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nautilus Scripts Manager')
        self.setGeometry(200, 200, 500, 400)

        self.vscode_path = read_vscode_path()

        central = QWidget()
        self.setCentralWidget(central)
        self.vbox = QVBoxLayout()
        central.setLayout(self.vbox)

        self.script_list = QListWidget()
        self.vbox.addWidget(QLabel("Scripts in Nautilus Scripts Folder:"))
        self.vbox.addWidget(self.script_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.open_vscode_btn = QPushButton("Create / Edit Scripts in VSCode")
        self.open_vscode_btn.clicked.connect(self.open_vscode_in_scripts_dir)
        btn_layout.addWidget(self.open_vscode_btn)

        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.update_script_list)
        btn_layout.addWidget(self.refresh_btn)

        self.vbox.addLayout(btn_layout)

        # File Watcher
        self.init_watcher()

        # Load List
        self.update_script_list()

        self.script_list.itemChanged.connect(self.toggle_script)

    def init_watcher(self):
        self.observer = Observer()
        self.event_handler = ScriptEventHandler(self)
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
        self.observer.schedule(self.event_handler, SCRIPTS_DIR, recursive=False)
        self.observer.start()

    def closeEvent(self, event):
        self.observer.stop()
        self.observer.join()
        event.accept()

    def prompt_vscode_path(self):
        dlg = QFileDialog(self, "Select VSCode Executable")
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("VSCode executables (code* *)")
        if dlg.exec_():
            chosen = dlg.selectedFiles()[0]
            if chosen and os.path.isfile(chosen) and os.access(chosen, os.X_OK):
                save_vscode_path(chosen)
                self.vscode_path = chosen
                return True
        return False

    def open_vscode_in_scripts_dir(self):
        if not self.vscode_path or not os.path.isfile(self.vscode_path):
            QMessageBox.information(self, "VSCode Not Found",
                                    "VSCode or VSCode Insiders was not found.\nPlease select the executable.")
            if not self.prompt_vscode_path():
                return
        try:
            subprocess.Popen([self.vscode_path, SCRIPTS_DIR])
        except Exception as e:
            QMessageBox.warning(self, "Error launching VSCode", str(e))

    def update_script_list(self):
        self.script_list.blockSignals(True)
        self.script_list.clear()
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
        for script in sorted(os.listdir(SCRIPTS_DIR)):
            fullpath = os.path.join(SCRIPTS_DIR, script)
            item = QListWidgetItem(script)
            is_exec = os.access(fullpath, os.X_OK)
            item.setCheckState(Qt.Checked if is_exec else Qt.Unchecked)
            self.script_list.addItem(item)
        self.script_list.blockSignals(False)

    def toggle_script(self, item):
        script_name = item.text()
        fullpath = os.path.join(SCRIPTS_DIR, script_name)
        enable = item.checkState() == Qt.Checked
        mode = os.stat(fullpath).st_mode
        if enable:
            os.chmod(fullpath, mode | 0o100)
        else:
            os.chmod(fullpath, mode & ~0o111)

def main():
    app = QApplication(sys.argv)
    win = NautilusScriptsManager()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()