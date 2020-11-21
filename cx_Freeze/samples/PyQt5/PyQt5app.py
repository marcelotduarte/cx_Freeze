#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Simple")
window.show()
app.exec_()
