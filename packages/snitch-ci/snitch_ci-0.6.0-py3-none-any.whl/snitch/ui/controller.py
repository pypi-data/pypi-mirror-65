""" Application entry point """
import logging as log
import json
import pickle
import os

from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QLabel, QFrame, QMenu, QAction,
    QFileDialog, QMessageBox, QHeaderView)
import pyautogui
from pynput.keyboard import Key

from ..model.data.testcase import TestCase
from ..model.data.events import Event
from ..model.data.screenshot import Screenshot
from ..model.eventproperties import EventPropertiesModel, EventPropertiesItemDelegate
from ..model.eventlist import EventListModel
from ..model.properties import PropertiesTableModel
from ..model.snaplist import SnapListModel
from .controller_ui import Ui_Controller
from .about import AboutDialog
from .settings import SettingsDialog
from ..recorder import EventRecorder, KeyEventCatcher
from ..player import EventPlayer, SnapshotPlayer
from ..settings import SETTINGS, CFG
from ..snapper import Snapper

class Data:
    #pylint: disable=too-few-public-methods
    TYPES = [pickle, json]
    NAMES = ["Pickle (*.p)", "Json (*.json *.js)"]
    DEFAULT_TYPE = json
    PANES_SIZES = [692, 308]

class Controller(QMainWindow):
    STATUS_TEXT = QApplication.translate('Controller', '{0} events recorded.')
    """ Main window for the app """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ui = Ui_Controller()
        self._ui.setupUi(self)

        self.new_testcase()

        self.update_open_recent_menu()

        self._ui.tableEvents.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._ui.eventSplitter.setSizes(Data.PANES_SIZES)
        self._ui.snapshotSplitter.setSizes(Data.PANES_SIZES)

        self._selected_event = None
        self._selected_snap = None
        self._saved_geometry = None
        self._catch_interrupt = None

        self.snap = None

        self._ui.menuAdd = QMenu(self._ui.eventMgmtButtons.ui.buttonAdd)
        for event_type in Event.get_subclasses():
            self._ui.menuAdd.addAction(event_type.__name__)
        self._ui.menuAdd.triggered.connect(self.add_event)
        self._ui.eventMgmtButtons.ui.buttonAdd.setMenu(self._ui.menuAdd)

        self._ui.tableEvents.selectionModel().selectionChanged.connect(self.update_selected_event)
        self._ui.tableProperties.setModel(EventPropertiesModel(None, self))
        self._ui.tableProperties.setItemDelegate(EventPropertiesItemDelegate(self))

        self._ui.listSnap.selectionModel().selectionChanged.connect(self.update_selected_snap)
        self._ui.tableSnapProps.setModel(PropertiesTableModel(None, self))

        self._ui.eventMgmtButtons.ui.buttonUp.clicked.connect(self.move_up)
        self._ui.eventMgmtButtons.ui.buttonDown.clicked.connect(self.move_down)

        self._ui.capsEventMgmtButtons.ui.buttonUp.clicked.connect(self.move_snap_up)
        self._ui.capsEventMgmtButtons.ui.buttonDown.clicked.connect(self.move_snap_down)

        self._ui.buttonPlay.clicked.connect(self.playback)
        self._ui.capsEventMgmtButtons.ui.buttonAdd.clicked.connect(self.capture)
        self._ui.buttonCapture.clicked.connect(self.capture)
        self._ui.buttonDiff.clicked.connect(self.diff)
        self._ui.buttonOCR.clicked.connect(self.ocr)

        self._ui.statuspos = QLabel(self)
        self._ui.statuspos.setMinimumWidth(120)
        self._ui.statuspos.setFrameShape(QFrame.Panel)
        self._ui.statuspos.setFrameShadow(QFrame.Sunken)
        self._ui.statuspos.setAlignment(Qt.AlignCenter)
        self._ui.statusbar.addPermanentWidget(self._ui.statuspos)

        self._mousepos_timer = QTimer(self)
        self._mousepos_timer.timeout.connect(self.update_mouse_pos)
        self._mousepos_timer.start(50)


######## ##     ## ######## ##    ## ########  ######
##       ##     ## ##       ###   ##    ##    ##    ##
##       ##     ## ##       ####  ##    ##    ##
######   ##     ## ######   ## ## ##    ##     ######
##        ##   ##  ##       ##  ####    ##          ##
##         ## ##   ##       ##   ###    ##    ##    ##
########    ###    ######## ##    ##    ##     ######


    def select_event(self, event):
        """ Selects the row in the table for the event passed as parameter """
        self._ui.tableEvents.selectRow(self._testcase.event_list.events.index(event))
        self._ui.tableEvents.scrollTo(self._ui.tableEvents.selectedIndexes()[0])
        # Allows UI update, but may be time consuming, remove if necessary:
        QApplication.processEvents()

    def get_selected_index(self):
        """
        :return: The index of the selected row of the event list,
                 or -1 if the selection is empty
        """
        selected_rows = self._ui.tableEvents.selectionModel().selectedRows()
        if selected_rows:
            # this is ok since the selection mode/behavior is single/rows
            return selected_rows[0].row()
        return -1

    @pyqtSlot()
    def playback(self, include_snapshots=False):
        """ Plays the recorded events """
        keys = [{Key.esc}]
        with KeyEventCatcher(keys, self._player.stop) as catcher:
            self._player.play(
                start_at=self.get_selected_index(),
                event_played_callback=self.select_event,
                key_event_catcher=catcher
            )
        if include_snapshots:
            return self._snap_player.play()

        QMessageBox.information(
            self,
            self.tr("Information"),
            self.tr("Sequence playback over.")
        )
        self._ui.tableEvents.clearSelection()

    @pyqtSlot()
    def stop_playback(self):
        """ Interrupts the playback """
        self._player.stop()


    @pyqtSlot(QAction)
    def add_event(self, event_type):
        """
        :type event_type: QAction
        """
        self._testcase.event_list.insert(self.get_selected_index(), event_type.text())

    @pyqtSlot()
    def move_up(self):
        """ Move selected event up one row """
        self._move(-1)

    @pyqtSlot()
    def move_down(self):
        """ Move selected event down one row """
        self._move(+1)

    def _move(self, direction):
        self._testcase.event_list.move(self._selected_event, direction)
        self._ui.tableEvents.selectRow(self.get_selected_index()+direction)

    @pyqtSlot()
    def update_selected_event(self):
        """ Sets the properties table to the selected event """
        item_index = self.get_selected_index()
        if not self._recorder.is_recording:
            if item_index < 0:
                self._testcase.event_list.offset = self._testcase.event_list.size()
            else:
                self._testcase.event_list.offset = item_index+1

        if 0 <= item_index < self._testcase.event_list.size():
            self._selected_event = self._testcase.event_list.events[item_index]
        else:
            self._selected_event = None

        self._update_control_buttons(item_index)
        self._update_properties()

    def _update_control_buttons(self, index):
        """ Updates enableness of the buttons of the selected event """
        is_event_selected = self._selected_event is not None
        self._ui.eventMgmtButtons.ui.buttonDel.setEnabled(is_event_selected)
        self._ui.eventMgmtButtons.ui.buttonUp.setEnabled(is_event_selected and index > 0)
        self._ui.eventMgmtButtons.ui.buttonDown.setEnabled(is_event_selected and index < self._testcase.event_list.size()-1)

    def _update_properties(self):
        """ Updates the property view of the selected event """
        if self._selected_event is not None:
            self._ui.tableProperties.setEnabled(True)
            model = EventPropertiesModel(self._selected_event, self)
            self._ui.tableProperties.setModel(model)
        else:
            self._selected_event = None
            self._ui.tableProperties.setEnabled(False)
            self._ui.tableProperties.setModel(EventPropertiesModel(None, self))

    @pyqtSlot(str)
    def change_event_type(self, new_class):
        """ Change the type of the selected event (may be unsafe) """
        if self._selected_event is not None:
            event = Event.create(new_class, self._selected_event)
            self._testcase.event_list.replace(self._selected_event, event)
            self._selected_event = event
            self._update_properties()

    @pyqtSlot(tuple)
    def set_shortcut_modifiers(self, modifiers):
        if self._selected_event is not None:
            self._selected_event.modifiers = modifiers
            self._update_properties()


 ######  ##    ##    ###    ########   ######  ##     ##  #######  ########  ######
##    ## ###   ##   ## ##   ##     ## ##    ## ##     ## ##     ##    ##    ##    ##
##       ####  ##  ##   ##  ##     ## ##       ##     ## ##     ##    ##    ##
 ######  ## ## ## ##     ## ########   ######  ######### ##     ##    ##     ######
      ## ##  #### ######### ##              ## ##     ## ##     ##    ##          ##
##    ## ##   ### ##     ## ##        ##    ## ##     ## ##     ##    ##    ##    ##
 ######  ##    ## ##     ## ##         ######  ##     ##  #######     ##     ######


    def get_selected_snap_index(self):
        """
        :return: The index of the selected row of the snapshot list,
                 or -1 if the selection is empty
        """
        selected_rows = self._ui.listSnap.selectionModel().selectedRows()
        if selected_rows:
            return selected_rows[0].row()
        return -1


    @pyqtSlot()
    def move_snap_up(self):
        """ Move selected event up one row """
        self._move_snap(-1)

    @pyqtSlot()
    def move_snap_down(self):
        """ Move selected event down one row """
        self._move_snap(+1)

    def _move_snap(self, direction):
        self._testcase.snap_list.move(self._selected_snap, direction)
        self._ui.listSnap.setCurrentIndex(
            self._ui.listSnap.model().index(self.get_selected_snap_index()+direction, 0)
            )

    @pyqtSlot()
    def update_selected_snap(self):
        """
        Sets the properties table to the selected snapshot and updates the
        snap preview
        """
        item_index = self.get_selected_snap_index()
        if 0 <= item_index < self._testcase.snap_list.size():
            self._selected_snap = self._testcase.snap_list.get(item_index)
            img = self._selected_snap.as_image()
            if img is not None:
                self._ui.labelPreview.setPixmap(img)
        else:
            self._selected_snap = None
            # reset to default image
            self._ui.labelPreview.setPixmap(QPixmap(":/eyecandy/ui/icons/snitch_a30.png"))

        self._update_snap_properties()
        self._update_snap_control_buttons(item_index)

    def _update_snap_control_buttons(self, index):
        """ Updates enableness of the buttons of the selected snapshot """
        is_snap_selected = self._selected_snap is not None
        self._ui.capsEventMgmtButtons.ui.buttonDel.setEnabled(is_snap_selected)
        self._ui.capsEventMgmtButtons.ui.buttonUp.setEnabled(is_snap_selected and index > 0)
        self._ui.capsEventMgmtButtons.ui.buttonDown.setEnabled(is_snap_selected and index < self._testcase.snap_list.size()-1)

    def _update_snap_properties(self):
        """ Updates the property view of the selected snapshots """
        if self._selected_snap is not None:
            self._ui.tableSnapProps.setEnabled(True)
            model = PropertiesTableModel(self._selected_snap, self)
            self._ui.tableSnapProps.setModel(model)
        else:
            self._ui.tableSnapProps.setEnabled(False)
            self._ui.tableSnapProps.setModel(EventPropertiesModel(None, self))

    @pyqtSlot()
    def capture(self):
        """ Starts the screen capture sequence """
        QApplication.setOverrideCursor(Qt.CrossCursor)
        self.snap = Snapper()
        self.snap.area_captured.connect(self.save_capture)

    @pyqtSlot(int, int, int, int)
    def save_capture(self, x, y, w, h):
        """ Slot called when the capture is performed """
        self.snap = None

        capture = Screenshot(region=(x, y, w, h))
        capture.do_capture()
        self._testcase.snap_list.push(capture)
        self._ui.listSnap.setCurrentIndex(self._ui.listSnap.model().index(self._testcase.snap_list.size()-1, 0, QModelIndex()))
        QApplication.restoreOverrideCursor()

    @pyqtSlot()
    def diff(self):
        """ Shows the image diff window for the selected capture """
        selection = self._ui.listSnap.selectedIndexes()
        if selection:
            snap_id = selection[0].row()
            self._snap_player.show_diff(snap_id)
        else:
            QMessageBox.warning(
                self,
                self.tr("Error"),
                self.tr("Please select a snapshot.")
            )

    @pyqtSlot()
    def ocr(self):
        """ Computes the ocr of the selected capture """
        selection = self._ui.listSnap.selectedIndexes()
        if selection:
            snap_id = selection[0].row()
            self._snap_player.compute_ocr(snap_id)
            self._update_snap_properties()
        else:
            QMessageBox.warning(
                self,
                self.tr("Error"),
                self.tr("Please select a snapshot.")
            )


######## #### ##       ########    ##     ##  ######   ##     ## ########
##        ##  ##       ##          ###   ### ##    ##  ###   ###    ##
##        ##  ##       ##          #### #### ##        #### ####    ##
######    ##  ##       ######      ## ### ## ##   #### ## ### ##    ##
##        ##  ##       ##          ##     ## ##    ##  ##     ##    ##
##        ##  ##       ##          ##     ## ##    ##  ##     ##    ##    ###
##       #### ######## ########    ##     ##  ######   ##     ##    ##    ###


    def new_testcase(self):
        self._testcase = TestCase(self)

        self._recorder = EventRecorder(self._testcase.event_list, parent=self)
        self._player = EventPlayer(self._testcase.event_list, parent=self)
        self._ui.tableEvents.setModel(EventListModel(self._testcase.event_list, self))

        self._snap_player = SnapshotPlayer(self._testcase.snap_list, parent=self)
        self._ui.listSnap.setModel(SnapListModel(self._testcase.snap_list, self))

        self._ui.eventMgmtButtons.ui.buttonDel.clicked.connect(lambda: self._testcase.event_list.remove(self._selected_event))
        self._ui.capsEventMgmtButtons.ui.buttonDel.clicked.connect(lambda: self._testcase.snap_list.remove(self._selected_snap))

        self._ui.buttonRecord.clicked.connect(self._recorder.start)
        self._ui.buttonStop.clicked.connect(self._recorder.stop)
        self._ui.buttonClear.clicked.connect(self._clear)
        self._ui.buttonPlaySnaps.clicked.connect(self._snap_player.play)

        self._testcase.event_list.list_changed.connect(self.update_status)
        self._testcase.event_list.list_changed.connect(self.update_selected_event)
        self._testcase.snap_list.list_changed.connect(self.update_selected_snap)


    @pyqtSlot()
    def show_save_dialog(self):
        """ Opens the file save dialog """
        filename, filetype = QFileDialog.getSaveFileName(
            self,
            self.tr("Save as"),
            CFG['history']['last_location']+"/record.json",
            ';;'.join(Data.NAMES),
            dict(zip(Data.TYPES, Data.NAMES))[Data.DEFAULT_TYPE]
        )
        if filename:
            self._testcase.save(filename, dict(zip(Data.NAMES, Data.TYPES))[filetype])
            SETTINGS.append_to_history(filename)
            self.update_open_recent_menu()


    @pyqtSlot()
    def show_open_dialog(self):
        """ Opens the file open dialog """
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            self.tr("Open"),
            CFG['history']['last_location'],
            ';;'.join(Data.NAMES),
            dict(zip(Data.TYPES, Data.NAMES))[Data.DEFAULT_TYPE]
        )
        if filename:
            self._testcase.event_list.clear()
            self._testcase.snap_list.clear()
            self._testcase.load(filename, dict(zip(Data.NAMES, Data.TYPES))[filetype])
            SETTINGS.append_to_history(filename)
            self.update_open_recent_menu()

    def load(self, filename):
        if os.path.isfile(filename):
            self._testcase.load(filename)
            return True
        return False

    def save_result(self, filename):
        self._testcase.save(filename.replace('.json', '.result.json'))

    def update_open_recent_menu(self):
        self._ui.menuOpenRecent.clear()
        for recent in CFG['history']['last_files']:
            self._ui.menuOpenRecent.addAction(recent)

    @pyqtSlot(QAction)
    def open_recent(self, action):
        filename = action.text()
        if os.path.isfile(filename):
            self._testcase.load(filename)
            SETTINGS.append_to_history(action.text())
        else:
            QMessageBox.information(
                self,
                self.tr("Information"),
                self.tr("File doesn’t exist anymore.")
            )
            CFG['history']['last_files'].remove(filename)

        self.update_open_recent_menu()


##     ## ####  ######   ######         ##     ## ####
###   ###  ##  ##    ## ##    ##        ##     ##  ##
#### ####  ##  ##       ##              ##     ##  ##
## ### ##  ##   ######  ##              ##     ##  ##
##     ##  ##        ## ##              ##     ##  ##
##     ##  ##  ##    ## ##    ## ###    ##     ##  ##
##     ## ####  ######   ######  ###     #######  ####


    @pyqtSlot()
    def update_status(self):
        """ Updates the statusbar text on event list change """
        message = self.tr('Event list cleared.')
        if self._testcase.event_list.size() > 0:
            message = self.tr('Event added: {0}'.format(self._testcase.event_list.events[-1]))
        self._ui.statusbar.showMessage(message, 1000)
        self.update_status_label()

    @pyqtSlot()
    def update_status_label(self):
        """ Updates the default string of the statusbar """
        action = ''
        if self._recorder.is_recording:
            action = self.tr('RECORDING... ')
        self._status_label = action + Controller.STATUS_TEXT.format(self._testcase.event_list.size())
        self._ui.statusbar.showMessage(self._status_label)

    @pyqtSlot()
    def update_mouse_pos(self):
        self._ui.statuspos.setText('x={} ; y={}'.format(*pyautogui.position()))

    @pyqtSlot()
    def show_settings_dialog(self):
        """ Opens the settings and configuration dialog """
        SettingsDialog(self).show()

    @pyqtSlot()
    def show_about_dialog(self):
        """ Opens the information dialog """
        AboutDialog(self).show()

    @pyqtSlot()
    def _clear(self):
        if QMessageBox.question(
                self,
                self.tr("Confirmation"),
                self.tr("Are you sure you want to delete all events and screenshots?")
                ) == QMessageBox.Yes:

            self._testcase.event_list.clear()
            self._testcase.snap_list.clear()

    def closeEvent(self, event):
        # pylint: disable=no-self-use
        SETTINGS.save()
        event.accept()
