#!/usr/bin/env python

import sys
from PySide2.QtWidgets import QApplication, QWidget

# import QtGui and QtCore only so that they are also frozen
import PySide2.QtGui
import PySide2.QtCore


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Simple")
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
