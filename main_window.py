"""Modules for UI"""
import os
import sys
from typing import Any

from PySide6.QtCore import QStandardPaths, Qt, QUrl
from PySide6.QtGui import QAction, QCloseEvent, QPixmap
from PySide6.QtPdf import QPdfDocument
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

import absorb_pdf_dialog_widget
import absorb_pdf_tab_widget
import absorb_pdf_view_widget
import constants

# pylint: disable=unused-import
import images.window_app_icon


class AbsorbWidget(QMainWindow):
    """This is main class to launch PDF viewer."""

    # pylint: disable=unused-argument
    def __init__(self, parent: Any = None) -> None:
        super().__init__()

        self.open_action = QAction("Open")
        self.open_action.setShortcut("Ctrl+O")
        self.quit_action = QAction("Exit Absorb")
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.quit_action)

        self.dialog = absorb_pdf_dialog_widget.AbsorbPdfDialogWidget()
        self.open_action.triggered.connect(self.launch_browser)

        self.tab = absorb_pdf_tab_widget.AbsorbPdfTabWidget()

        self.setCentralWidget(self.tab)

        self.setWindowTitle("Absorb PDF Viewer")
        self.setWindowIcon(QPixmap(":/windowAppPrefix/window_app_icon.ico"))
        self.setWindowState(Qt.WindowState.WindowMaximized)

    def launch_browser(self) -> None:
        """This function launches the pdf selection dialog box.
        The last selected file path is set in the QSettings."""

        documents_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        default_path = self.dialog.settings.value(
            constants.DIALOG_LAST_DIRECTORY, documents_path
        )
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF File", str(default_path), "PDF Files (*.pdf)"
        )
        if file_path:
            pdf_view = absorb_pdf_view_widget.AbsorbPdfViewWidget()
            pdf_document = QPdfDocument(pdf_view)
            pdf_view.setDocument(pdf_document)
            self.tab.create_tab(pdf_view, os.path.basename(file_path))
            pdf_document.load(QUrl.fromLocalFile(file_path).toLocalFile())
            self.dialog.settings.setValue(
                constants.DIALOG_LAST_DIRECTORY, os.path.dirname(file_path)
            )

    # pylint: disable=invalid-name
    def closeEvent(self, event: QCloseEvent) -> None:
        """This function overrides the PySide event for closing window."""
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AbsorbWidget()
    window.show()
    sys.exit(app.exec())
