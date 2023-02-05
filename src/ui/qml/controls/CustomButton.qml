import QtQuick
import QtQuick.Controls

Button {
    id: butoon
    implicitWidth: 100
    implicitHeight: 50
    hoverEnabled: false

    text: qsTr("Single")

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 50
        color: butoon.down ? "#BFBEE3" :"#9092DA"
        border.color: "#28272C"
        border.width: 1
        radius: 5
    }

    contentItem: Item {
        id: content

        Text {
            color: "#F1F1F3"
            text: butoon.text
            font: butoon.font
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
