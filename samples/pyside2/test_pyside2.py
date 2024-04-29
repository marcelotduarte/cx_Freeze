"""A simple script to demonstrate PySide2."""

import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QWidget


def main() -> int:
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Simple")
    window.setGeometry(300, 300, 300, 300)
    label = QLabel(window)
    label.setText("Hello World!")
    label.setGeometry(0, 0, 300, 300)
    label.setAlignment(Qt.AlignCenter)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
