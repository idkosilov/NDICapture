import QtQuick
import QtQuick.Controls

ComboBox {
    id: control
    model: []

    delegate: ItemDelegate {
        width: control.width
        background: Rectangle {
            color: control.highlightedIndex === index ? "#9092DA" : "#17161B"
        }
        contentItem: Text {
            text: control.textRole ? (Array.isArray(
                                          control.model) ? modelData[control.textRole] : model[control.textRole]) : modelData
            color: control.highlightedIndex === index ? "#F1F1F3" : "#F1F1F3"
            font: control.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: control.highlightedIndex === index
    }

    indicator: Canvas {
        id: canvas
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 12
        height: 8
        contextType: "2d"

        Connections {
            target: control
            function onPressedChanged() {
                canvas.requestPaint()
            }
        }

        onPaint: {
            context.reset()
            context.moveTo(0, 0)
            context.lineTo(width, 0)
            context.lineTo(width / 2, height)
            context.closePath()
            context.fillStyle = control.pressed ? "#BFBEE3" : "#9092DA"
            context.fill()
        }
    }

    contentItem: Text {
        leftPadding: 0
        rightPadding: control.indicator.width + control.spacing

        text: control.displayText
        font: control.font
        color: "#F1F1F3"
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 120
        implicitHeight: 40
        color: "#17161B"
        border.color: control.pressed ? "#BFBEE3" : "#9092DA"
        border.width: control.visualFocus ? 2 : 1
        radius: 5
    }

    popup: Popup {
        y: control.height - 1
        width: control.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator {}
        }

        background: Rectangle {
            border.color: "#17161B"
            radius: 2
        }
    }
}
