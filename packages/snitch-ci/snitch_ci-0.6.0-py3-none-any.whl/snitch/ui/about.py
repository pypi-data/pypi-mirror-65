from PyQt5.QtWidgets import QDialog

import snitch

from .about_ui import Ui_AboutDialog

class AboutDialog(QDialog):
    """ Information dialog """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ui = Ui_AboutDialog()
        self._ui.setupUi(self)

        about_string = self._ui.text.text()
        self._ui.text.setText(about_string.replace('{VERSION_NUMBER}', snitch.__version__))
