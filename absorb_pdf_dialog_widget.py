import os
import sys

from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QFileDialog, QApplication, QWidget

import constants


class AbsorbPdfDialogWidget(QFileDialog):
    def __init__(self, parent=None) -> None:
        super().__init__()

        self.settings = QSettings("Tectonic Shift Studios", "Absorb PDF")

        self.setNameFilter("Adobe PDF Files (*.pdf)")
        self.setViewMode(QFileDialog.ViewMode.Detail)
        self.setAcceptMode(self.AcceptMode.AcceptOpen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AbsorbPdfDialogWidget()
    sys.exit(app.exec())
