"""PyQt6 WebEngineWidgets Example."""

from __future__ import annotations

import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QToolBar,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PyQt6 WebEngineWidgets Example")

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.backButton = QPushButton()
        self.backButton.setIcon(
            QIcon(":/qt-project.org/styles/commonstyle/images/left-32.png")
        )
        self.backButton.clicked.connect(self.back)
        self.toolBar.addWidget(self.backButton)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(
            QIcon(":/qt-project.org/styles/commonstyle/images/right-32.png")
        )
        self.forwardButton.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forwardButton)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.addressLineEdit)

        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)
        initialUrl = "https://marcelotduarte.github.io/cx_Freeze/"
        self.addressLineEdit.setText(initialUrl)
        self.webEngineView.load(QUrl(initialUrl))
        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)

    def load(self) -> None:
        url = QUrl.fromUserInput(self.addressLineEdit.text())
        if url.isValid():
            self.webEngineView.load(url)

    def back(self) -> None:
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self) -> None:
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def urlChanged(self, url) -> None:
        self.addressLineEdit.setText(url.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(
        availableGeometry.width() * 2 // 3, availableGeometry.height() * 2 // 3
    )
    mainWin.show()
    sys.exit(app.exec())
