import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.1
import QtQuick.Controls.Styles 1.1
import Qt.labs.settings 1.0

Window {
    id: root
    title: "FA Forever"
    width: 1024
    height: 768
    minimumWidth: 400
    minimumHeight: 300
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
    color: backgroundColor

    property string backgroundColor: "#111111"
    property string highlightColor: "#2f2f2f"
    property string altHighlightColor: "#454545"
    property string textColor: "#969696"

    // remember window geometry
    Settings {
        property alias x: root.x
        property alias y: root.y
        property alias width: root.width
        property alias height: root.height
        // property alias visibility: root.visibility // TODO : maximized
    }

    Action {
        id: closeWindow
        shortcut: "Ctrl+Q"
        onTriggered: Qt.quit();
    }

    Action {
        id: toggleDebug
        shortcut: "Ctrl+`"
        onTriggered: {
            if (debugWindow.state == "open") {
                debugWindow.state = "closed"
            } else {
                debugWindow.state = "open"
            }
        }
    }

    Action {
        id: toggleSideMenu
        shortcut: "Ctrl+D"
        onTriggered: {
            if (sideMenu.state == "open") {
                sideMenu.state = "closed"
            } else {
                sideMenu.state = "open"
            }
        }
    }

    Rectangle {
        id: borderResizeHook // use to allow resizing through edge drag - not implemented yet
        anchors.fill: parent
        border.width: root.visibility == Window.Maximized ? 0 : 1
        border.color: root.highlightColor
        color: "transparent"
        z: 300
    }

    Rectangle {
        id: topArea
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.topMargin: borderResizeHook.border.width
        anchors.rightMargin: borderResizeHook.border.width
        anchors.leftMargin: borderResizeHook.border.width
        height: childrenRect.height
        color: root.color
        z: 400

        ActionIcon {
            id: actionIcon
            source: "icons/faf.png"
            overlayColor: "#44f1c240"
            glowColor: "white"
            glowRadius: 3
            size: 30
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin: 2
            anchors.leftMargin: 5 + borderResizeHook.border.width
            onClicked: { toggleSideMenu.trigger() }
        }

        Item { // to hold main menu, top action menu, user widget...
            anchors.top: parent.top
            anchors.left: actionIcon.right
            anchors.right: parent.right
            anchors.margins: 5
            height: childrenRect.height + 5
            z:400

            Row {
                anchors.top: parent.top
                anchors.left: parent.left

                width: 24
                height: 24
            }
        }

        User {
                id: user
                anchors.top: parent.top
                anchors.right: windowControls.left
                background: root.highlightColor
                hover: root.altHighlightColor
                state: loginModel.panel_visible ? "open" : "closed"
                onClicked: loginModel.panel_visible = !loginModel.panel_visible
        }

        Row {
                id: windowControls
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.rightMargin: 5

                Rectangle {
                    width: 26
                    height: 26
                    color: minimizeMouseArea.containsMouse ? root.highlightColor : "transparent"

                    Image {
                        source: "icons/minimize.svg"
                        sourceSize: Qt.size(10, 10)
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        id: minimizeMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.showMinimized()
                    }
                }

                Rectangle {
                    width: 26
                    height: 26
                    color: maximizeMouseArea.containsMouse ? root.altHighlightColor : "transparent"

                    Image {
                        source: root.visibility == Window.Maximized ? "icons/restore.svg" : "icons/maximize.svg"
                        sourceSize: Qt.size(10, 10)
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        id: maximizeMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.visibility == Window.Maximized ? root.showNormal() : root.showMaximized()
                    }
                }

                Rectangle {
                    width: 32
                    height: 26
                    color: closeMouseArea.containsMouse ? root.altHighlightColor : "transparent"

                    Image {
                        source: "icons/close.svg"
                        sourceSize: Qt.size(10, 10)
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        id: closeMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: closeWindow.trigger(closeMouseArea)
                    }
                }
        }

        MouseArea {
            id: topAreaMouseHandle
            anchors.top: parent.top
            anchors.right: user.left
            anchors.bottom: parent.bottom
            anchors.left: actionIcon.right

            onDoubleClicked: root.visibility == Window.Maximized ? root.showNormal() : root.showMaximized()

            property variant previousPosition
            onPressed: { previousPosition = Qt.point(mouseX, mouseY) }
            onPositionChanged: {
                if (pressedButtons == Qt.LeftButton && root.visibility != Window.Maximized) {
                    var dx = mouseX - previousPosition.x
                    var dy = mouseY - previousPosition.y
                    root.x += dx
                    root.y += dy
                }
            }
        }
    }

    Item {
        id: userPanel
        visible: loginModel.panel_visible
        x: user.mapFromItem(user, user.x, 0).x - (width - user.width) + borderResizeHook.border.width // absolute positioning to user control's right
        y: user.mapFromItem(user, 0, user.y).y + user.height + borderResizeHook.border.width // absolute positioning to user control's bottom
        z: 500
        width: childrenRect.width
        height: childrenRect.height

        LogIn {
            visible: !loginModel.logged_in
            background: root.highlightColor
            textColor: root.textColor
        }

        UserPanel {
            visible: loginModel.logged_in
            background: root.highlightColor
            textColor: root.textColor
        }
    }

    Item {
        id: debugWindow
        anchors.top: topArea.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        height: 0.8*parent.height
        z: 200
        transform: Translate {
            id: debugWindowOffset
            y: -debugWindow.height
        }
        state: "closed"
        states: [
            State {
                name: "open"
                PropertyChanges { target: debugWindowOffset; y: 0 }
            },
            State {
                name: "closed"
                PropertyChanges { target: debugWindowOffset; y: -debugWindow.height }
            }
        ]
        transitions: Transition { NumberAnimation { target: debugWindowOffset; property: "y"; duration: 200 } }

        TextArea {
            objectName: "console"
            anchors.fill: parent
            frameVisible: false
            readOnly: true
            style: TextAreaStyle {
                textColor: root.textColor
                backgroundColor: root.highlightColor
            }
        }
    }

    Rectangle {
        id: sideMenu
        anchors.left: parent.left
        anchors.top: topArea.bottom
        anchors.bottom: bottomArea.top
        anchors.leftMargin: borderResizeHook.border.width
        anchors.bottomMargin: 5
        width: 32+2*5
        z: 100
        transform: Translate {
            id: sideMenuOffset
            x: -sideMenu.width
        }
        color: root.color
        state: "closed"
        states: [
            State {
                name: "open"
                PropertyChanges { target: sideMenuOffset; x: 0 }
            },
            State {
                name: "closed"
                PropertyChanges { target: sideMenuOffset; x: -sideMenu.width }
            }
        ]
        transitions: Transition { NumberAnimation { target: sideMenuOffset; property: "x"; duration: 200 } }

        Column {
            spacing: 10
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            anchors.bottomMargin: 10

            ActionIcon {
                source: "icons/rss.svg"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            ActionIcon {
                source: "icons/lightbulb.svg"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            ActionIcon {
                source: "icons/point.svg"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            ActionIcon {
                source: "icons/world.svg"
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }

    Item {
        id: centralArea
        anchors.top: topArea.bottom
        anchors.bottom: bottomArea.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.bottomMargin: 5
        anchors.leftMargin: 5
        z: 0

        Rectangle {
            id: centralWidget
            color: "#202025"
            anchors.fill: parent

            Games { }
        }
    }

    Item {
        id: bottomArea
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottomMargin: 5
        height: 13 // childrenRect.height // this reports binding loop for some reason
        z: 400

        Label {
            id: label
            text: windowModel.label
            color: root.altHighlightColor
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.leftMargin: 2*5
        }

        Row {
            id: status
            visible: windowModel.taskRunning
            anchors.right: resizer.left
            anchors.bottom: parent.bottom
            anchors.rightMargin: 2*5
            width: childrenRect.width
            spacing: 5

            Label {
                id: actionLabel
                text: windowModel.taskStatusText
                color: root.textColor
            }

            ProgressBar {
                visible: !windowModel.taskStatusIsIndefinite
                width: visible ? 128 : 0
                height: actionLabel.height / 2
                anchors.verticalCenter: parent.verticalCenter
                value: windowModel.taskStatusProgress
                style: ProgressBarStyle {
                    background: Rectangle {
                        color: "transparent"
                        border.color: root.textColor
                        border.width: 1
                        implicitWidth: 200
                        implicitHeight: 24
                    }
                    progress: Rectangle {
                        color: root.textColor
                        border.color: root.textColor
                    }
                }
            }
        }

        Image {
            id: resizer
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 5
            source: "icons/corner.svg"
            sourceSize: Qt.size(label.height, label.height)

            MouseArea {
                anchors.fill: parent

                property variant previousPosition
                onPressed: {
                    previousPosition = Qt.point(mouseX, mouseY)
                }
                onPositionChanged: {
                    if (pressedButtons == Qt.LeftButton && root.visibility != Window.Maximized) {
                        var dx = mouseX - previousPosition.x
                        var dy = mouseY - previousPosition.y
                        root.width = Math.max(root.width + dx, root.minimumWidth)
                        root.height = Math.max(root.height + dy, root.minimumHeight)
                    }
                }
            }
        }
    }
}
