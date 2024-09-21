"""A simple script to demonstrate PySide6."""

import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

VIEW_DATA = b"""
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow {
    id: main

    title: qsTr("app")
    width: 1100
    minimumWidth: 1100
    height: 800
    minimumHeight: 800
    visible: true

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 5

        TabBar {
            id: tab_bar
            TabButton {
                text: qsTr("Tab 1")
                width: implicitWidth
            }
            TabButton {
                text: qsTr("Tab 2")
                width: implicitWidth
            }
            TabButton {
                text: qsTr("Tab 3")
                width: implicitWidth
            }
        }

        StackLayout {
            currentIndex: tab_bar.currentIndex
            Rectangle {
                Layout.fillHeight: true
                Layout.fillWidth: true
                color: "red"
            }
            GridLayout {
                columns: 3
                Rectangle {
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.columnSpan: 3
                    color: "green"
                }
            }
            ColumnLayout {
                GroupBox {
                    Layout.fillWidth: true
                    RowLayout {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter

                        Rectangle {
                            color: "blue"
                            height: 50
                            width: 100
                        }
                    }
                }
            }
        }
    }
}
"""


def main() -> int:
    app = QGuiApplication()
    app.setOrganizationName("example")
    app.setOrganizationDomain("example.com")
    QQuickStyle.setStyle("Universal")
    engine = QQmlApplicationEngine()
    engine.loadData(VIEW_DATA)

    if not engine.rootObjects():
        return -1

    app.aboutToQuit.connect(engine.rootObjects()[0].deleteLater)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
