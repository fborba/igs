from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets


def create_label(text):
    label = QtWidgets.QLabel(text)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    return label


class IntValidator(QtGui.QIntValidator):
    # This is a workaround to prevent leading zeros and to provide bottom and
    # top values at initialization.
    def __init__(self, bottom=None, top=None):
        super().__init__()

        if bottom is not None:
            self.setBottom(bottom)
        if top is not None:
            self.setTop(top)

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)

        if self.bottom() < 0 and self.top() > 0:
            return state, input, pos

        if state != QtGui.QValidator.Invalid:
            if len(input) != 0 and input[0] == "0":
                input = input[1:]

        return state, input, pos


class IntLineEdit(QtWidgets.QLineEdit):
    def __init__(self, bottom=None, top=None):
        super().__init__()
        self.setValidator(IntValidator(bottom, top))
