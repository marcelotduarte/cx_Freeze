#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication, QDialog

app = QApplication(sys.argv)
form = QDialog()
form.show()
app.exec_()
