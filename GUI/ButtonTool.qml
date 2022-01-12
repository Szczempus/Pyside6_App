import QtQuick 2.12
import "Colors.js" as Colors

Rectangle {
    id: control
    color: Colors.main
    border.width: 0

    implicitHeight: parent.height
    implicitWidth: parent.height

    height: implicitHeight
    width: implicitWidth

    property bool active: false
    property string tool: ""
    property bool isAction: false

    property string icon_source: ""
    property string icon_source_highlighted: ""

    property string text: "TOOL"

    signal clicked(string tool, bool active)

    onActiveChanged: {
        if(!active)
            mouseArea.state = "normal"
    }

    Image {
        id: image
        anchors.fill: parent
        anchors.bottomMargin: parent.height*0.3
        fillMode: Image.PreserveAspectFit
        source: parent.icon_source
        antialiasing: true
        mipmap: true
        smooth: true
        opacity: 1
    }

    Image {
        anchors.fill: parent
        anchors.bottomMargin: parent.height*0.3
        fillMode: Image.PreserveAspectFit
        source: parent.icon_source_highlighted
        antialiasing: true
        mipmap: true
        smooth: true
        opacity: 1 - image.opacity
    }

    Text {
        id: buttonText
        anchors.top: image.bottom
        anchors.topMargin: -parent.height/10
        anchors.bottom: parent.bottom
        width: parent.width
        padding: 5
        text: parent.text
        minimumPixelSize: 6
        font.pixelSize: 16
        font.family: Colors.font
        fontSizeMode: Text.Fit
        color: Colors.text

        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        elide: Text.ElideRight

    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if(!control.isAction)
            {
                control.active = !control.active
                control.clicked(control.tool, control.active)
            }
            else
            {
                control.clicked(control.tool, true)
            }
        }

        onEntered: state = "hovered"
        onExited: {
            if(!control.active)
                state = "normal"
        }

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
                        target: image
                        property: "opacity"
                        to: 0.0
                        duration: 300
                    }
                    PropertyAnimation {
                        target: control
                        property: "color"
                        to: Colors.highlighted_main
                        duration: 300
                    }
                    PropertyAnimation {
                        target: buttonText
                        property: "color"
                        to: Colors.highlighted_text
                        duration: 300
                    }
                }
            },
            Transition {
                from: "hovered"
                to: "normal"
                ParallelAnimation {
                    PropertyAnimation {
                        target: image
                        property: "opacity"
                        to: 1.0
                        duration: 300
                    }
                    PropertyAnimation {
                        target: control
                        property: "color"
                        to: Colors.main
                        duration: 300
                    }
                    PropertyAnimation {
                        target: buttonText
                        property: "color"
                        to: Colors.text
                        duration: 300
                    }
                }
            }
        ]
    }
}
