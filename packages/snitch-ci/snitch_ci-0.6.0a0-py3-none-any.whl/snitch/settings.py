import os
import json
import logging as log

from PyQt5.QtCore import QObject, pyqtSlot

CONFIG_FILE = os.path.expanduser('~/.snitch.json')
DEFAULT_SETTINGS = {
  'minimize_on_record': False,
  'replay_delay': 0.2,
  'diff_threshold': 98,
  'history': {
    'max_size': 10,
    'last_location': '',
    'last_files': []
  }
}

class Settings(QObject):
    def __init__(self, load_file=True, parent=None):
        super().__init__(parent)

        self.data = DEFAULT_SETTINGS

        if os.path.isfile(CONFIG_FILE) and load_file:
            config_string = open(CONFIG_FILE, 'r').read()
            try:
                self.data = json.loads(config_string)
            except json.JSONDecodeError:
                log.error("Invalid configuration file. Falling back to defaults.")


    @pyqtSlot()
    def save(self):
        with open(CONFIG_FILE, 'w') as cfg:
            json.dump(self.data, cfg, indent=2)

    @pyqtSlot(bool)
    def set_minimize_on_record(self, value):
        self.data['minimize_on_record'] = value

    @pyqtSlot(float)
    def set_replay_delay(self, value):
        self.data['replay_delay'] = value

    @pyqtSlot(str)
    def append_to_history(self, value):
        self.data['history']['last_location'] = os.path.dirname(value)
        last_files = self.data['history']['last_files']

        if value in last_files:
            last_files.remove(value)

        last_files.insert(0, value)

        while len(last_files) > self.data['history']['max_size']:
            del last_files[-1]

    @pyqtSlot(str)
    def sel_last_dir(self, value):
        self.data['history']['last_location'] = value

SETTINGS = Settings()
CFG = SETTINGS.data
