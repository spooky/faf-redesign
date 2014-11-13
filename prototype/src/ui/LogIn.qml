import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2


Rectangle {
    property string background
    property string textColor
    property int padding: 5

    function login() {
        loginModel.login(userName.text, password.text, remember.checked)
    }

    id: wrapper
    color: background
    width: childrenRect.width + 2*padding
    height: childrenRect.height + 2*padding
    Keys.onReturnPressed: login()
    Keys.onEscapePressed: loginModel.panel_visible = false

    Column {
        spacing: padding
        x: padding
        y: padding
        width: 150

        Text {
            text: qsTr("User Name")
            color: textColor
        }

        TextField {
            id: userName
            width: parent.width
            text: loginModel.user
        }

        Text {
            text: qsTr("Password")
            color: textColor
        }

        TextField {
            id: password
            echoMode: TextInput.Password
            width: parent.width
            text: loginModel.password
        }

        Item {
            width: parent.width
            height: loginButton.height

            CheckBox {
                id: remember
                checked: loginModel.remember
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                style: CheckBoxStyle {
                    label: Text {
                        text: qsTr("Remember")
                        color: textColor
                    }
                }
            }

            Button {
                id: loginButton
                text: qsTr("Log In")
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                onClicked: login()
            }
        }
    }
}
