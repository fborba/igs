from PyQt5 import QtWidgets

from igs.graphics.shape import Line, Point, Position, Rectangle, Square

from igs.ui import util


class ShapeDialog(QtWidgets.QDialog):
    def __init__(self, shape):
        super().__init__()

        self.setWindowTitle(f"Add {shape}")

        self._form = QtWidgets.QFormLayout()

        form_group = QtWidgets.QGroupBox("Input")
        form_group.setLayout(self._form)

        button_box = QtWidgets.QDialogButtonBox()

        button_box.addButton("Cancel", QtWidgets.QDialogButtonBox.RejectRole)
        button_box.addButton("Add", QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.validate_and_accept)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(form_group)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def add_input(self, label, input):
        self._form.addRow(util.create_label(label), input)

    def validate_and_accept(self):
        for i in range(1, self._form.rowCount(), 2):
            input = self._form.itemAt(i).widget()
            if not input.hasAcceptableInput():
                return

        self.accept()

    def shape(self):
        NotImplemented

    def add_shape(self, display_file):
        display_file.add(self.shape())


class LineDialog(ShapeDialog):
    def __init__(self, shape):
        super().__init__(shape)

        self._x0 = util.IntLineEdit()
        self._y0 = util.IntLineEdit()
        self._x1 = util.IntLineEdit()
        self._y1 = util.IntLineEdit()

        self.add_input("First point x", self._x0)
        self.add_input("First point y", self._y0)
        self.add_input("Second point x", self._x1)
        self.add_input("Second point y", self._y1)

    def shape(self):
        x0 = int(self._x0.text())
        y0 = int(self._y0.text())
        x1 = int(self._x1.text())
        y1 = int(self._y1.text())

        return Line(Position(x0, y0), Position(x1, y1))


class PointDialog(ShapeDialog):
    def __init__(self, shape):
        super().__init__(shape)

        self._x = util.IntLineEdit()
        self._y = util.IntLineEdit()

        self.add_input("x-coordinate", self._x)
        self.add_input("y-coordinate", self._y)

    def shape(self):
        x = int(self._x.text())
        y = int(self._y.text())

        return Point(Position(x, y))


class RectangleDialog(ShapeDialog):
    def __init__(self, shape):
        super().__init__(shape)

        self._x = util.IntLineEdit()
        self._y = util.IntLineEdit()
        self._width = util.IntLineEdit(1)
        self._height = util.IntLineEdit(1)

        self.add_input("Top-left x", self._x)
        self.add_input("Top-left y", self._y)
        self.add_input("width", self._width)
        self.add_input("height", self._height)

    def shape(self):
        x = int(self._x.text())
        y = int(self._y.text())
        width = int(self._width.text())
        height = int(self._height.text())

        return Rectangle(Position(x, y), width, height)


class SquareDialog(ShapeDialog):
    def __init__(self, shape):
        super().__init__(shape)

        self._x = util.IntLineEdit()
        self._y = util.IntLineEdit()
        self._size = util.IntLineEdit(1)

        self.add_input("Top-left x", self._x)
        self.add_input("Top-left y", self._y)
        self.add_input("size", self._size)

    def shape(self):
        x = int(self._x.text())
        y = int(self._y.text())
        size = int(self._size.text())

        return Square(Position(x, y), size)


class DialogFactory:
    def __init__(self) -> None:
        self._dialogs = {}

    def register(self, shape, dialog):
        self._dialogs[shape] = dialog

    def get(self, shape):
        dialog = self._dialogs.get(shape)

        if not dialog:
            raise ValueError(shape)

        return dialog(shape)


dialog_factory = DialogFactory()

dialog_factory.register("Line", LineDialog)
dialog_factory.register("Point", PointDialog)
dialog_factory.register("Rectangle", RectangleDialog)
dialog_factory.register("Square", SquareDialog)
