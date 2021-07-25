"""A simple script to demonstrate PySide2."""

import sys
from PySide2.QtWidgets import QApplication, QWidget


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Simple")
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
