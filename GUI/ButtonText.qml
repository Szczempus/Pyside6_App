import QtQuick 2.12
import QtQuick.Window 2.12
import "Colors.js" as Colors

Rectangle {
    id: control
    color: Colors.main
    border.width: 0

    implicitHeight: Screen.height/30
    implicitWidth: parent.width

    height: implicitHeight
    width: implicitWidth

    property bool alignHCenter: false

    property string action: "action"
    property string text: "Text"

    signal clicked(string action)

    Text {
        id: buttonText
        anchors.fill: parent
        padding: 10
        text: parent.text
        minimumPixelSize: 8
        font.pixelSize: 16
        font.family: Colors.font
        fontSizeMode: Text.VerticalFit
        color: Colors.text

        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: control.alignHCenter ? Text.AlignHCenter : Text.AlignLeft
//        horizontalAlignment: Text.AlignLeft
        elide: Text.ElideRight

    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            control.clicked(parent.action)
        }

        onEntered: state = "hovered"
        onExited: state = "normal"

        state: "normal"

        states: [
            State {
                name: "hovered"
            },
            State {
                name: "normal"
            }
        ]

        transitions: [
            Transition {
                from: "normal"
                to: "hovered"
                ParallelAnimation {
                    PropertyAnimation {
                        targets: [buttonText]
                        property: "color"
                        to: Colors.highlighted_text
                        duration: 300
                    }
                    PropertyAnimation {
                        target: control
                        property: "color"
                        to: Colors.highlighted_main
                        duration: 300
                    }
                }
            },
            Transition {
                from: "hovered"
                to: "normal"
                ParallelAnimation {
                    PropertyAnimation {
                        targets: [buttonText]
                        property: "color"
                        to: Colors.text
                        duration: 300
                    }
                    PropertyAnimation {
                        target: control
                        property: "color"
                        to: Colors.main
                        duration: 300
                    }
                }
            }
        ]
    }

}
