import QtQuick
import QtQuick.Window
import QtMultimedia
import QtQuick.Controls
import QtQuick.Layouts
import "controls"

Window {
    id: mainWindow
    width: 1000
    height: 580
    minimumHeight: 500
    minimumWidth: 800
    title: "NDI Capture"
    visible: true
    color: "#00000000"

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#17161B"

        Row {
            id: applicationTitle
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.leftMargin: 10
            spacing: 10
            Image {
                id: appLogo
                width: 140
                height: 30
                source: "logo.png"
                fillMode: Image.PreserveAspectFit
            }
        }
        Rectangle {
            id: controlMenu
            x: 782
            width: 250
            color: "#28272c"
            radius: 5
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            clip: true
            anchors.bottomMargin: 10
            anchors.topMargin: 60
            anchors.rightMargin: 10

            Rectangle {
                id: controlHeader
                height: 22
                color: "#9092da"
                radius: 5
                border.width: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                clip: true
                anchors.topMargin: 0
                anchors.leftMargin: 0
                anchors.rightMargin: 0

                Text {
                    id: controlLabel
                    color: "#f1f1f3"
                    text: qsTr("Controls")
                    anchors.fill: parent
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.bold: true
                    font.family: "Proxima Nova"
                }

                Rectangle {
                    id: controlFooter
                    x: 0
                    y: 0
                    height: 5
                    color: "#9092da"
                    radius: 0
                    border.width: 0
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.leftMargin: 0
                    clip: true
                    anchors.rightMargin: 0
                }
            }

            Column {
                id: formColumn
                height: 120
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: controlHeader.bottom
                anchors.topMargin: 10
                anchors.rightMargin: 5
                anchors.leftMargin: 5
                spacing: 20
                Row {
                    id: windowRow
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    spacing: 10
                    Text {
                        id: windowLabel
                        width: 90
                        height: 15
                        color: "#f1f1f3"
                        text: qsTr("Window")
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.family: "Proxima Nova"
                        font.bold: true
                    }

                    CustomComboBox {
                        id: windowComboBox
                        width: 140
                        height: 25
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                Row {
                    id: ndiOutputRow
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    spacing: 10
                    Text {
                        id: ndiOutputLabel
                        width: 90
                        height: 15
                        color: "#f1f1f3"
                        text: qsTr("NDI Output")
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        font.family: "Proxima Nova"
                        font.bold: true
                    }

                    CustomTextField {
                        id: ndiOutputField
                        width: 140
                        height: 25
                        anchors.verticalCenter: parent.verticalCenter
                        placeholderText: qsTr("Enter NDI Output")
                    }
                }

                RowLayout {
                    id: buttonsLayout
                    height: 30
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    spacing: 5

                    CustomButton {
                        id: addButton
                        width: 120
                        height: 30
                        text: qsTr("Add")
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                    }

                    CustomButton {
                        id: removeButton
                        width: 120
                        height: 30
                        text: qsTr("Remove")
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                    }
                }
            }

            Text {
                id: ndiOutputsLabel
                height: 15
                color: "#f1f1f3"
                text: qsTr("NDI Outputs")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: formColumn.bottom
                font.pixelSize: 12
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                anchors.topMargin: 20
                anchors.rightMargin: 5
                anchors.leftMargin: 5
                font.family: "Proxima Nova"
                font.bold: true
            }

            ListModel {
                    id: ndiOutputsModel
                    ListElement { name: "Alice" }
                    ListElement { name: "Bob" }
                    ListElement { name: "Jane" }
                    ListElement { name: "Harry" }
                    ListElement { name: "Wendy" }
                }

            Component {
                id: ndiOutputDelegate

                Text {
                    readonly property ListView __lv: ListView.view

                    height: 25
                    text: model.name
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 5
                    anchors.rightMargin: 5
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: 14
                    color: "#f1f1f3"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: __lv.currentIndex = model.index
                    }
                }
            }

            Rectangle {
                id: ndiOutputsViewBackground
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: ndiOutputsLabel.bottom
                anchors.bottom: startStopButton.top
                anchors.bottomMargin: 5
                anchors.topMargin: 5
                anchors.leftMargin: 5
                anchors.rightMargin: 5
                color: "#17161B"
                radius: 5

                ListView {
                    id: ndiOutputsView
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 5
                    anchors.bottomMargin: 5
                    anchors.leftMargin: 5
                    anchors.rightMargin: 5
                    model: ndiOutputsModel
                    delegate: ndiOutputDelegate
                    focus: true
                    clip: true

                    highlight: Rectangle {
                        anchors { left: parent.left; right: parent.right;}
                        color: "#BFBEE3"
                    }
                }
            }

            CustomButton {
                id: startStopButton
                y: 472
                height: 30
                text: qsTr("Start")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 5
                anchors.leftMargin: 5
                anchors.rightMargin: 5
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }

        Rectangle {
            id: ndiOutputTitle
            width: 150
            height: 22
            color: "#9092da"
            radius: 5
            border.width: 0
            anchors.left: parent.left
            anchors.top: applicationTitle.bottom
            anchors.leftMargin: 10
            anchors.topMargin: 20
            Text {
                id: text3
                color: "#f1f1f3"
                text: qsTr("NDI Output")
                anchors.fill: parent
                font.pixelSize: 12
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                anchors.rightMargin: 5
                anchors.leftMargin: 5
                font.family: "Proxima Nova"
                font.bold: true
            }

            Rectangle {
                id: rectangle4
                x: 0
                y: 0
                height: 5
                color: "#9092da"
                radius: 0
                border.width: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.leftMargin: 0
                clip: true
                anchors.bottomMargin: 0
                anchors.rightMargin: 0
            }
            clip: true
        }

        Rectangle {
            id: ndiOutputBackgorund
            color: "#28272c"
            radius: 5
            anchors.left: parent.left
            anchors.right: controlMenu.left
            anchors.top: ndiOutputTitle.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 0
            anchors.bottomMargin: 10
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            clip: true

            VideoOutput {
                id: ndiOutput
                anchors.fill: parent
                fillMode: VideoOutput.PreserveAspectFit
                anchors.rightMargin: 5
                anchors.leftMargin: 5
                anchors.bottomMargin: 5
                anchors.topMargin: 5
            }

            Rectangle {
                id: rectangle5
                x: 0
                width: 200
                height: 5
                color: "#28272c"
                radius: 0
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.leftMargin: 0
                clip: true
            }
        }
    }
}
