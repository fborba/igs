from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from igs.graphics.displayfile import DisplayFile
from igs.ui import util
from igs.ui.view import Viewport, ListView
from igs.ui.dialog import dialog_factory


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Interactive Graphics System")

        self.setFixedHeight(600)
        self.setFixedWidth(800)

        self._display_file = DisplayFile()

        shape_list = ListView()
        shape_list.setModel(self._display_file)

        self._shape_selector = QtWidgets.QComboBox()
        self._shape_selector.addItems(
            [
                "Closed Polyline",
                "Line",
                "Point",
                "Polyline",
                "Rectangle",
                "Square",
            ]
        )

        shape_create_button = QtWidgets.QPushButton("Create")
        shape_create_button.clicked.connect(self.add_shape)

        shape_creator = QtWidgets.QFormLayout()
        shape_creator.addRow(self._shape_selector, shape_create_button)

        control_group = QtWidgets.QVBoxLayout()
        control_group.addWidget(util.create_label("Shapes"))
        control_group.addWidget(shape_list)
        control_group.addLayout(shape_creator)

        viewport = Viewport()
        viewport.set_display_file(self._display_file, True)

        viewport_group = QtWidgets.QVBoxLayout()
        viewport_group.addWidget(util.create_label("Viewport"))
        viewport_group.addWidget(viewport, 1, Qt.AlignTop)

        self._display_file.rowsRemoved.connect(viewport.update)
        self._display_file.rowsInserted.connect(viewport.update)

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(control_group)
        layout.addLayout(viewport_group, 1)

        self.setLayout(layout)

    def add_shape(self):
        dialog = dialog_factory.get(self._shape_selector.currentText())

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self._display_file.add(dialog.shape())
