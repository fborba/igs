# Interactive Graphics System

## Dependencies

- Qt5
- Poetry (see [installation])

# Installation

```
poetry install
poetry run python igs/runner.py
```

## Instructions

### Controlling the window

To control the window, you need to to click first. Then, you can move it using the keyboard arrows and zoom in and out scrolling the mouse. The window has a `Mark` object on its center to help the user and can be removed if necessary (see below).

### Creating a shape

To add a shape, select it in the dropdown list in the bottom of the program window and click "Create". A dialog will ask for shape parameters such as the x and y coordinates of some points. Fill the form and click "Add". The shape list will display the newly created shape with a name composed of its name (the shape name by default) and the six first digits of its hash. This hash helps in identifying the shape even if its later renamed.

### Removing a shape

To remove a shape, select it in the shape list and press delete on the keyboard.

### Renaming a shape

If the user wants to give a more meaningful name to a shape, he or she can double click on it in the shape list and enter the new name. The hash will still be displayed in list.


<!-- Links -->

[installation]: https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
