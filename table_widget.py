from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cellChanged.connect(self.handleCellChange)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def contextMenu(self, position):
        """Кастомное меню, удаляет колонку и делает дубли"""
        index = self.indexAt(position)
        if not index.isValid():
            return

        row = index.row()
        menu = QMenu(self)

        deleteRow = QAction("Delete", self)
        doubleRow = QAction("Double", self)

        deleteRow.triggered.connect(lambda: self.removeRow(row))
        doubleRow.triggered.connect(lambda: self.duplicateRow(row))

        menu.addAction(deleteRow)
        menu.addAction(doubleRow)
        menu.exec_(self.viewport().mapToGlobal(position))

    def duplicateRow(self, row):
        """Дублировать строку"""
        self.insertRow(row + 1)
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                new_item = QTableWidgetItem(item.text())
                self.setItem(row + 1, col, new_item)


    def handleCellChange(self, row, column):
        """События на изменения таблицы"""
        if row == self.rowCount() - 1:
            if self.item(row, column) and self.item(row, column).text():
                self.addNewRow()
        self.deleteDoubleEmptyRow()

    def addNewRow(self):
        """Добавления новой колонки"""
        self.insertRow(self.rowCount())

    def deleteDoubleEmptyRow(self):
        """Удаляем дубли"""
        if self.rowCount() <= 1:
            return
        last = self.rowCount()
        for col in range(self.columnCount()):
            item = self.item(last, col)
            if item and item.text():
                return
        self.removeRow(last)



