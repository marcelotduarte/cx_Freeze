import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

DEFAULT_HTML = '<!DOCTYPE html><html lang="en">' \
               '<body style="text-align: center; vertical-align: middle;">' \
               '<div style = "margin-top: 200px;">If you see this, it is working.</div></div>' \
               '</body></html>'


class WebEngineTestWindow(QMainWindow):

    def __init__(self):
        super(WebEngineTestWindow, self).__init__()
        self.setObjectName("WebEngineTestWindow")
        self.setWindowTitle(self.tr(self.__class__.__name__))
        self.resize(640, 480)
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.webview = QWebEngineView(self)
        self.verticalLayout.addWidget(self.webview)
        self.webview.setHtml(DEFAULT_HTML)


def main():
    QApplication.setDesktopSettingsAware(False)
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    app = QApplication(sys.argv)
    window = WebEngineTestWindow()
    window.show()
    ret = app.exec_()
    return ret


if __name__ == '__main__':
    sys.exit(main())
