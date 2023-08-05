from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize

class AspectRatioPixmapLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(1, 1)
        self.setScaledContents(False)
        self._pixmap = None

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        super().setPixmap(self._scaled_pixmap())

    def heightForWidth(self, width):
        if self._pixmap:
            return self._pixmap.height() / self._pixmap.width() * width
        return self.height()

    def sizeHint(self):
        return QSize(self.width(), self.heightForWidth(self.width()))

    def resizeEvent(self, event):
        # pylint: disable=unused-argument
        if self._pixmap:
            super().setPixmap(self._scaled_pixmap())

    def _scaled_pixmap(self):
        return self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
