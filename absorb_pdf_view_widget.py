from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel
from PySide6.QtPdfWidgets import QPdfView


class AbsorbPdfViewWidget(QPdfView):
    def __init__(self, pdf_document: QPdfDocument, parent=None) -> None:
        super().__init__()

        self.setPageMode(self.PageMode.MultiPage)
        self.setDocument(pdf_document)

        # Track middle mouse state and initial press position
        self.middle_mouse_pressed = False
        self.middle_mouse_start_pos = QPoint()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            # Start tracking middle mouse press and position
            self.middle_mouse_pressed = True
            self.middle_mouse_start_pos = event.position().toPoint()
            # Change cursor to indicate scroll mode (optional)
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.middle_mouse_pressed:
            # Calculate how far the mouse has moved since the start of the press
            delta_y = event.position().toPoint().y() - self.middle_mouse_start_pos.y()
            # Adjust the vertical scroll based on the delta
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta_y
            )

            # Update the starting position for smooth scrolling
            self.middle_mouse_start_pos = event.position().toPoint()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            # Stop the middle mouse scrolling effect
            self.middle_mouse_pressed = False
            # Reset the cursor
            self.unsetCursor()
        else:
            super().mouseReleaseEvent(event)
