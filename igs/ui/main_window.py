from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from igs.graphics.displayfile import DisplayFile
from igs.graphics.transform import Rotation, Transform, Translation, Scaling, combine
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

        self._shape_list = ListView()
        self._shape_list.setModel(self._display_file)

        self._transform_group = TransformGroup()

        scaling_button = self._transform_group.scaling_button()
        scaling_button.clicked.connect(self.apply_scaling)

        translation_button = self._transform_group.translation_button()
        translation_button.clicked.connect(self.apply_translation)

        rotation_center_button = self._transform_group.rotation_center_button()
        rotation_center_button.clicked.connect(self.apply_rotation_center)

        rotation_origin_button = self._transform_group.rotation_origin_button()
        rotation_origin_button.clicked.connect(self.apply_rotation_origin)

        rotation_point_button = self._transform_group.rotation_point_button()
        rotation_point_button.clicked.connect(self.apply_rotation_point)

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
        control_group.addWidget(self._shape_list)
        control_group.addWidget(self._transform_group)
        control_group.addLayout(shape_creator)

        viewport = Viewport()
        viewport.set_display_file(self._display_file, True)

        viewport_group = QtWidgets.QVBoxLayout()
        viewport_group.addWidget(util.create_label("Viewport"))
        viewport_group.addWidget(viewport, 1, Qt.AlignTop)

        self._display_file.rowsRemoved.connect(viewport.update)
        self._display_file.rowsInserted.connect(viewport.update)
        self._display_file.dataChanged.connect(viewport.update)

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(control_group)
        layout.addLayout(viewport_group, 1)

        self.setLayout(layout)

    def add_shape(self):
        dialog = dialog_factory.get(self._shape_selector.currentText())

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self._display_file.add(dialog.shape())

    def apply_scaling(self):
        scaling = self._transform_group.scaling()

        for index in self._shape_list.selectionModel().selectedIndexes():
            shape = self._display_file.data(index, Qt.UserRole)
            center = shape.center()

            transform = combine(
                Translation(-center.x(), -center.y()),
                scaling,
                Translation(center.x(), center.y()),
            )

            self._display_file.setData(index, shape.apply(transform), Qt.UserRole)

    def apply_translation(self):
        translation = self._transform_group.translation()

        for index in self._shape_list.selectionModel().selectedIndexes():
            shape = self._display_file.data(index, Qt.UserRole)
            self._display_file.setData(index, shape.apply(translation), Qt.UserRole)

    def apply_rotation_center(self):
        rotation = self._transform_group.rotation_center()

        for index in self._shape_list.selectionModel().selectedIndexes():
            shape = self._display_file.data(index, Qt.UserRole)

            center = shape.center()
            x = center.x()
            y = center.y()

            transform = combine(Translation(-x, -y), rotation, Translation(x, y))
            self._display_file.setData(index, shape.apply(transform), Qt.UserRole)

    def apply_rotation_origin(self):
        rotation = self._transform_group.rotation_origin()

        for index in self._shape_list.selectionModel().selectedIndexes():
            shape = self._display_file.data(index, Qt.UserRole)
            self._display_file.setData(index, shape.apply(rotation), Qt.UserRole)

    def apply_rotation_point(self):
        rotation = self._transform_group.rotation_point()

        for index in self._shape_list.selectionModel().selectedIndexes():
            shape = self._display_file.data(index, Qt.UserRole)
            self._display_file.setData(index, shape.apply(rotation), Qt.UserRole)


class TransformGroup(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._translate = QtWidgets.QLineEdit()
        self._scale = QtWidgets.QLineEdit()
        self._rotate_center = QtWidgets.QLineEdit()
        self._rotate_origin = QtWidgets.QLineEdit()
        self._rotate_point = QtWidgets.QLineEdit()

        self._translate_button = QtWidgets.QPushButton("Translate")
        self._scale_button = QtWidgets.QPushButton("Scale")
        self._rotate_center_button = QtWidgets.QPushButton("Rotate center")
        self._rotate_origin_button = QtWidgets.QPushButton("Rotate origin")
        self._rotate_point_button = QtWidgets.QPushButton("Rotate point")

        form = QtWidgets.QFormLayout()

        form.addRow(self._translate, self._translate_button)
        form.addRow(self._scale, self._scale_button)
        form.addRow(self._rotate_center, self._rotate_center_button)
        form.addRow(self._rotate_origin, self._rotate_origin_button)
        form.addRow(self._rotate_point, self._rotate_point_button)

        self.setLayout(form)

    def scaling_button(self):
        return self._scale_button

    def translation_button(self):
        return self._translate_button

    def rotation_center_button(self):
        return self._rotate_center_button

    def rotation_origin_button(self):
        return self._rotate_origin_button

    def rotation_point_button(self):
        return self._rotate_point_button

    def scaling(self):
        text = self._scale.text()
        sx, sy = eval(text) if text else (1, 1)

        return Scaling(sx, sy)

    def translation(self):
        text = self._translate.text()
        tx, ty = eval(text) if text else (0, 0)

        return Translation(tx, ty)

    def rotation_center(self):
        text = self._rotate_center.text()
        theta = eval(text) if text else 0

        return Rotation(theta)

    def rotation_origin(self):
        text = self._rotate_origin.text()
        theta = eval(text) if text else 0

        return Rotation(theta)

    def rotation_point(self):
        text = self._rotate_point.text()
        theta, (x, y) = eval(text) if text else (0, 0, 0)

        return combine(Translation(-x, -y), Rotation(theta), Translation(x, y))
