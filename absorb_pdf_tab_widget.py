from typing import Any

from PySide6.QtCore import QUrl, Signal, Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout


class AbsorbPdfTabWidget(QTabWidget):
    def __init__(self, parent: Any =None) -> None:
        super().__init__()
        self.setTabShape(self.TabShape.Rounded)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.tabCloseRequested.connect(self.remove_tab)

    def create_tab(self, pdf_view: QPdfView, name_of_pdf_file: str, ) -> None:
        wid = QWidget()
        self.addTab(wid, name_of_pdf_file)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setStyleSheet(
            "QTabBar::tab { height: 20; width: 100px;} QTabWidget::pane { /* The tab widget frame */border-top: 2px "
            "solid #C2C7CB;} QTabWidget::tab-bar {left: 5px; /* move to the right by 5px */} QTabBar::tab {"
            "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, "
            "stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB; /* same "
            "as the pane color */border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 8ex; padding: "
            "2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
            "stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);} QTabBar::tab:selected {"
            "border-color: #9B9B9B; border-bottom-color: #C2C7CB; /* same as pane color */} QTabBar::tab:!selected {"
            "margin-top: 2px; /* make non-selected tabs look smaller */}")

        vlayout = QVBoxLayout(wid)
        vlayout.addWidget(pdf_view)
        wid.setLayout(vlayout)

    def remove_tab(self, index: int) -> None:
        self.removeTab(index)
