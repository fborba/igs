from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from igs.graphics.window import Window
from igs.graphics.shape import Mark, Point


class ListView(QtWidgets.QListView):
    """
    A list view that that can delete objects.
    """

    def __init__(self):
        """
        Creates a new list view.
        """
        super().__init__()

    def keyPressEvent(self, event):
        """
        Handles key press events.

        Parameters
        ----------
        event : QtGui.QKeyEvent
            Type of event.
        """
        if event.key() != Qt.Key_Delete:
            super().keyPressEvent(event)
            return

        for index in self.selectionModel().selectedIndexes():
            self.model().removeRow(index.row())


class Viewport(QtWidgets.QFrame):
    """
    A frame to draw shapes.
    """

    _MARGIN = 10

    def __init__(self):
        """
        Create a new viewport.
        """
        super().__init__()

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setFocusPolicy(Qt.ClickFocus)

        size = min(self.width(), self.height())
        window_size = size - 2

        self.setFixedSize(size, size)

        self._window = Window(
            Point(-window_size / 2, -window_size / 2),
            window_size,
            window_size,
        )

    def set_display_file(self, display_file, center_marker=False):
        """
        Set the display file to draw.

        Parameters
        ----------
        display_file : DisplayFile
            A display file.
        center_marker : bool, optional
            Boolean indicating whether to draw a mark in the center, by
            default False.
        """
        self._display_file = display_file

        if center_marker:
            self._display_file.add(Mark(Point(0, 0)))

    def width(self):
        """
        Return the width of this viewport.

        Returns
        -------
        int
            Width of this viewport.
        """
        return self.contentsRect().width()

    def height(self):
        """
        Return the height of this viewport.

        Returns
        -------
        int
            Height of this viewport.
        """
        return self.contentsRect().height()

    def draw_margin(self, painter):
        """
        Draw a margin in this viewport.

        Parameters
        ----------
        painter : QPainter
            Painter used to paint.
        """
        painter.drawRect(
            self._MARGIN,
            self._MARGIN,
            self.width() - 2 * self._MARGIN,
            self.height() - 2 * self._MARGIN,
        )

    def transform(self, point):
        """
        Apply the viewport transform to a point.

        Parameters
        ----------
        point : Point
            Point to apply the transform.

        Returns
        -------
        Point
            The transformed point.
        """
        point = self._window.normalize(point)

        x = round(point.x() * self.width())
        y = round(point.y() * self.height())

        return Point(x, y)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        key = event.key()

        if key == Qt.Key_Left:
            self._window.move_left()
            self.update()

        elif key == Qt.Key_Right:
            self._window.move_right()
            self.update()

        elif key == Qt.Key_Up:
            self._window.move_up()
            self.update()

        elif key == Qt.Key_Down:
            self._window.move_down()
            self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self._window.zoom_in()
        else:
            self._window.zoom_out()

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QtGui.QPainter(self)

        self.draw_margin(painter)

        for shape in self._display_file:
            transformed_shape = shape.clone().apply(self.transform)
            transformed_shape.draw(painter)
