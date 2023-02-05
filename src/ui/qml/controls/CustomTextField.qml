import QtQuick
import QtQuick.Controls

TextField {
    id: control
    placeholderText: qsTr("Enter description")
    color: "#F1F1F3"
    placeholderTextColor: "#6a6a6a"
    verticalAlignment: Qt.AlignVCenter
    horizontalAlignment: Qt.AlignLeft

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 40
        color: control.enabled ? "#17161B" : "#17161B"
        border.color: control.pressed ? "#9092DA": "#BFBEE3"
        radius: 5
    }
}
