from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class DisplayFile(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._shapes = []

    def add(self, shape):
        position = self.rowCount()

        self.insertRows(position, 1)
        self.setData(self.index(position), shape)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= len(self._shapes):
            return QtCore.QVariant()

        object = self._shapes[index.row()]

        if role == Qt.DisplayRole:
            hash_value = hex(hash(object))
            return f"{object} ({hash_value[2:8]})"

        elif role == Qt.EditRole:
            return f"{self._shapes[index.row()]}"

        else:
            return QtCore.QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEditable

        return super().flags(index) | Qt.ItemIsEditable

    def insertRows(self, position, rows):
        self.beginInsertRows(
            QtCore.QModelIndex(),
            position,
            position + rows - 1,
        )

        for _ in range(rows):
            self._shapes.insert(position, None)

        self.endInsertRows()

        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(
            QtCore.QModelIndex(),
            position,
            position + rows - 1,
        )

        for _ in range(rows):
            self._shapes.pop(position)

        self.endRemoveRows()

        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._shapes)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            shape = self._shapes[index.row()]

            if isinstance(value, str):
                shape.set_name(value)
            else:
                self._shapes[index.row()] = value
                self.dataChanged.emit(index, index, [role])

            return True

        return False

    def __iter__(self):
        return iter(self._shapes)
