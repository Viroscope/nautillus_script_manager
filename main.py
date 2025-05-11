import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QCheckBox, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPTS_DIR = os.path.expanduser('~/.local/share/nautilus/scripts')

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

    def open_vscode_in_scripts_dir(self):
        try:
            subprocess.Popen(['/usr/bin/code-insiders', SCRIPTS_DIR])
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "VSCode Insiders not found at /usr/bin/code-insiders")

    def update_script_list(self):
        self.script_list.clear()
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
        for script in sorted(os.listdir(SCRIPTS_DIR)):
            fullpath = os.path.join(SCRIPTS_DIR, script)
            item = QListWidgetItem(script)
            is_exec = os.access(fullpath, os.X_OK)
            item.setCheckState(Qt.Checked if is_exec else Qt.Unchecked)
            self.script_list.addItem(item)
        self.script_list.itemChanged.connect(self.toggle_script)

    def toggle_script(self, item):
        script_name = item.text()
        fullpath = os.path.join(SCRIPTS_DIR, script_name)
        enable = item.checkState() == Qt.Checked
        mode = os.stat(fullpath).st_mode
        if enable:
            # Add user-executable permission
            os.chmod(fullpath, mode | 0o100)
        else:
            # Remove all executable permissions
            os.chmod(fullpath, mode & ~0o111)

def main():
    app = QApplication(sys.argv)
    win = NautilusScriptsManager()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()