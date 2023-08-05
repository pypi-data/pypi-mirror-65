from os.path import splitext

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog

from .diff_ui import Ui_Diff

from ..settings import CFG


class Diff(QWidget):
    """ Main window for the app """
    def __init__(self, reference_image, result_image, diff_image, reference_ocr=None, result_ocr=None, parent=None):
        """
        :type reference_image: QPixmap
        :type result_image: QPixmap
        :type diff_image: QPixmap
        """
        super().__init__(parent)

        self._ui = Ui_Diff()
        self._ui.setupUi(self)

        self._ui.referenceImageLabel.setPixmap(reference_image)
        self._ui.resultImageLabel.setPixmap(result_image)

        self._original_image = reference_image
        self._result_image = result_image
        self._diff_image = diff_image

        if diff_image is None:
            self._ui.highlightButton.setEnabled(False)
            self._ui.highlightButton.setText(
                self.tr("Captures are identical ({}% threshold)".format(CFG['diff_threshold']))
                )

        if reference_ocr is not None:
            self._ui.referenceTextEdit.setPlainText(reference_ocr)
        if result_ocr is not None:
            self._ui.resultTextEdit.setPlainText(result_ocr)

        self._ui.referenceScrollArea.verticalScrollBar().valueChanged.connect(
            self._ui.resultScrollArea.verticalScrollBar().setValue
        )
        self._ui.referenceScrollArea.horizontalScrollBar().valueChanged.connect(
            self._ui.resultScrollArea.horizontalScrollBar().setValue
        )
        self._ui.resultScrollArea.verticalScrollBar().valueChanged.connect(
            self._ui.referenceScrollArea.verticalScrollBar().setValue
        )
        self._ui.resultScrollArea.horizontalScrollBar().valueChanged.connect(
            self._ui.referenceScrollArea.horizontalScrollBar().setValue
        )


    @pyqtSlot()
    def swap_results(self):
        """ Shows/hides the differences highlighting """
        image = self._result_image
        if self._ui.highlightButton.isChecked():
            image = self._diff_image

        self._ui.resultImageLabel.setPixmap(image)

    @pyqtSlot()
    def save_images(self):
        """ Exports the original and result images """
        name = 'export.png'
        if CFG['history']['last_files']:
            name = splitext(CFG['history']['last_files'][0])[0] + '.png'

        filename = QFileDialog.getSaveFileName(
            self,
            self.tr("Save as"),
            name,
            'PNG (*.png)'
        )[0]
        if filename:
            self._original_image.save(filename)
            self._result_image.save(splitext(filename)[0] + '.result.png')
