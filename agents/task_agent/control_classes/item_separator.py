from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QFont

class ItemSeparator(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item_class = index.data(Qt.ItemDataRole.UserRole)
        if item_class == "separator_date":
            painter.save()
            painter.fillRect(option.rect, QColor(45, 45, 45))
            #painter.setPen(QColor("white"))
            font = QFont()
            font.setBold(True)
            painter.setFont(font)
            text = index.data(Qt.ItemDataRole.DisplayRole)
            padding = 10
            text_rect = QRect(option.rect)
            text_rect.adjust(padding, 0, -padding, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
            painter.restore()
        else:
            super().paint(painter, option, index)