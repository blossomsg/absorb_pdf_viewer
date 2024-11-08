"""Modules for UI"""
import os
import sys

from PySide6.QtCore import QUrl, Qt, QSize, Slot, QStandardPaths, QSettings, QDir
from PySide6.QtGui import QAction, QKeyEvent, QWheelEvent, QPixmap, QScreen, QCloseEvent
from PySide6.QtPdf import QPdfDocument
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListView, QListWidget, QWidget, QHBoxLayout, \
    QFileDialog, QDialog

import absorb_pdf_dialog_widget
import absorb_pdf_view_widget
import constants
import images.window_app_icon
from absorb_pdf_dialog_widget import AbsorbPdfDialogWidget


class AbsorbWidget(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()

        self.open_action = QAction("Open")
        self.open_action.setShortcut("Ctrl+O")
        self.quit_action = QAction("Exit Absorb")
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

        self.file_menu = self.menuBar().addMenu("File")
        self.about_menu = self.menuBar().addMenu("About")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.quit_action)

        self.dialog = AbsorbPdfDialogWidget()
        self.open_action.triggered.connect(self.launch_browser)

        self.pdf_document = QPdfDocument()
        self.pdf_view = absorb_pdf_view_widget.AbsorbPdfViewWidget(self.pdf_document)

        self.pdf_widget = QWidget()
        self.pdf_horizontal_layout = QHBoxLayout(self.pdf_widget)

        self.pdf_horizontal_layout.addWidget(self.pdf_view)
        self.setCentralWidget(self.pdf_widget)

        self.setWindowTitle("Absorb PDF Viewer")
        self.setWindowIcon(QPixmap(":/windowAppPrefix/window_app_icon.ico"))
        self.setWindowState(Qt.WindowState.WindowMaximized)

        self.show()

    def launch_browser(self):
        documents_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        default_path = self.dialog.settings.value(constants.DIALOG_LAST_DIRECTORY, documents_path)
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", default_path, "PDF Files (*.pdf)")
        if file_path:
            # Load the selected PDF file
            self.pdf_document.load(QUrl.fromLocalFile(file_path).toLocalFile())

            # Save the directory of the opened file to settings
            self.dialog.settings.setValue(constants.DIALOG_LAST_DIRECTORY, os.path.dirname(file_path))

    def closeEvent(self, event: QCloseEvent) -> None:
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AbsorbWidget()
    sys.exit(app.exec())
