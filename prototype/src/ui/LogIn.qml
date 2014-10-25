import QtQuick 2.2
import QtQuick.Controls 1.2

Rectangle {
    property string background
    property string textColor
    property int padding: 5

    color: background
    width: childrenRect.width + 2*padding
    height: childrenRect.height + 2*padding

    Column {
        spacing: padding
        x: padding
        y: padding

        Text {
            text: "user name"
            color: textColor
        }

        TextField {
        }

        Text {
            text: "password"
            color: textColor
        }

        TextField {
            echoMode: TextInput.Password
        }

        Button {
            text: "log in"
            anchors.right: parent.right
        }
    }
}
