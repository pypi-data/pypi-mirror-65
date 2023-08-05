from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from .settings_ui import Ui_SettingsDialog
from ..settings import SETTINGS, CFG

class SettingsDialog(QDialog):
    """ Information dialog """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)

        self._ui.checkBoxMinimizeOnRecord.setChecked(CFG['minimize_on_record'])
        self._ui.valuePlaybackDelay.setValue(CFG['replay_delay'])
        self._ui.valueMaxRecent.setValue(CFG['history']['max_size'])
        self._ui.valueDiffThreshold.setValue(CFG['diff_threshold'])


    @pyqtSlot()
    def accept(self):
        CFG['minimize_on_record'] = self._ui.checkBoxMinimizeOnRecord.isChecked()
        CFG['replay_delay'] = self._ui.valuePlaybackDelay.value()
        CFG['history']['max_size'] = self._ui.valueMaxRecent.value()
        CFG['diff_threshold'] = self._ui.valueDiffThreshold.value()

        SETTINGS.save()
        super().accept()
