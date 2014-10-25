import QtQuick 2.2

Rectangle {
    id: wrapper
    anchors.verticalCenter: parent.verticalCenter
    anchors.rightMargin: 5
    width: childrenRect.width
    state: "closed"
    states: [
        State {
            name: "open"
            PropertyChanges { target: wrapper; color: background }
        },
        State {
            name: "closed"
            PropertyChanges { target: wrapper; color: "transparent" }
        }
    ]

    property string background
    signal clicked

    Row {
        spacing: 5
        x: 5

        Text {
            text: "log in"
            anchors.verticalCenter: parent.verticalCenter
            color: "#969696"
        }

        ActionIcon {
            source: "icons/user.svg"
            size: 30
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: wrapper.clicked()
    }
}
