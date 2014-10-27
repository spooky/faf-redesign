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
        width: 150

        Text {
            text: "User Name"
            // font.capitalization: Font.SmallCaps
            color: textColor
        }

        TextField {
            width: parent.width
        }

        Text {
            text: "Password"
            // font.capitalization: Font.SmallCaps
            color: textColor
        }

        TextField {
            echoMode: TextInput.Password
            width: parent.width
        }

        Button {
            text: "Log In"
            anchors.right: parent.right
        }
    }
}
