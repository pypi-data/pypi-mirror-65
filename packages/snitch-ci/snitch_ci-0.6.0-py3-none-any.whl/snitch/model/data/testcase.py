""" File format """
import logging as log
import json
import pickle
import os

import pyautogui
from PyQt5.QtCore import QObject

from ... import FILE_VERSION
from .events import Event
from ..eventlist import EventList
from .screenshot import Screenshot
from ..snaplist import SnapList

class TestCase(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._file_version = FILE_VERSION
        self.name = 'test_case'
        self._screen = pyautogui.size()

        self.event_list = EventList(self)
        self.snap_list = SnapList(self)

    def save(self, filename, export_module=json):
        """
        Saves the event recording into a file
        :param filename: The name of the file
        :param export_module: Either pickle or json
        """
        log.info('Saving %d events into "%s"', self.event_list.size(), filename)
        self.name = os.path.splitext(os.path.basename(filename))[0]
        try:
            file_content = {
                'version': self._file_version,
                'screen': pyautogui.size(),
                **self.event_list.get_serializable(),
                **self.snap_list.get_serializable()
            }
            if export_module == json:
                with open(filename, 'w') as record:
                    log.debug(file_content)
                    json.dump(file_content, record, indent=4, ensure_ascii=False)
            else:
                with open(filename, 'bw') as record:
                    pickle.dump(file_content, record)
        except OSError as ex:
            log.error(str(ex))

    def load(self, filename, import_module=json):
        """
        Loads the event recording from a file
        :param filename: The name of the file
        :param import_module: Either pickle or json
        """
        try:
            if import_module == json:
                with open(filename, 'r') as record:
                    data = json.load(record)
                    self._build_list_from_dict(data)
            elif import_module == pickle:
                with open(filename, 'r') as record:
                    file_content = pickle.load(record)
                    self._file_version = file_content['version']
                    self.event_list = file_content['events']
                    self.snap_list = file_content['screenshots']
            else:
                log.error('Unsuported file format: %s', import_module)

            self.name = os.path.splitext(os.path.basename(filename))[0]
            log.info('Loaded %d events from "%s"', self.event_list.size(), filename)
        except OSError as ex:
            log.error(str(ex))

    def _build_list_from_dict(self, event_list_dict):
        """
        :param event_list_dict: dictionnary of the JSON decoded object
        """
        try:
            self._file_version = event_list_dict['version']
            for event_item in event_list_dict['events']:
                event = Event.create(event_item['type'])
                for key, val in event_item.items():
                    event.__dict__[key] = val
                self.event_list.push(event)
            self.event_list.list_changed.emit()
            for snap_item in event_list_dict['screenshots']:
                snap = Screenshot()
                for key, val in snap_item.items():
                    snap.__dict__[key] = val
                self.snap_list.push(snap)
            self.snap_list.list_changed.emit()

        except (KeyError, IndexError) as err:
            log.error("Can't decode file: %s", err)
