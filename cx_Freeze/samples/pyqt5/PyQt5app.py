"""A simple script to demonstrate PyQt5."""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Simple")
window.show()
sys.exit(app.exec_())
