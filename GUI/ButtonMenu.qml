import QtQuick 2.12
import "Colors.js" as Colors

// Menu animated button (On top green bar)
Rectangle {
    id: control
    color: Colors.main
    border.width: 0

    implicitHeight: parent.height
    implicitWidth: parent.height

    height: implicitHeight
    width: implicitWidth

    states: [
        State {
            name: "menu"
        },
        State {
            name: "close"
        }
    ]
    state: "menu"

    transitions: [Transition {
        from: "menu"
        to: "close"
        SequentialAnimation{
            NumberAnimation{
                targets: [top_bar, bot_bar]
                property: "y"
                to: mid_bar.y
                duration: 150
            }
            NumberAnimation{
                targets: [top_bar, bot_bar]
                property: "opacity"
                to: 0.0
                duration: 1
            }
            ParallelAnimation{
                NumberAnimation{
                    target: mid_bar
                    property: "rotation"
                    to: 45
                    duration: 150
                }
                NumberAnimation{
                    target: mid_bar_2
                    property: "rotation"
                    to: -45
                    duration: 150
                }
            }
        }
    },
    Transition {
            from: "close"
            to: "menu"
            SequentialAnimation{
                NumberAnimation{
                    targets: [mid_bar, mid_bar_2]
                    property: "rotation"
                    to: 0
                    duration: 150
                }
                NumberAnimation{
                    targets: [top_bar, bot_bar]
                    property: "opacity"
                    to: 1.0
                    duration: 1
                }
                ParallelAnimation{
                    NumberAnimation{
                        target: top_bar
                        property: "y"
                        to: top_bar.parent.height*0.35
                        duration: 150
                    }
                    NumberAnimation{
                        target: bot_bar
                        property: "y"
                        to: bot_bar.parent.height*0.6
                        duration: 150
                    }
                }
            }
        }
    ]

    Rectangle {
        id: top_bar
        border.width: 0
        width: parent.width*0.5
        height: parent.height*0.05
        radius: height/2
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height*0.35
    }

    Rectangle {
        id: mid_bar
        border.width: 0
        width: parent.width*0.5
        height: parent.height*0.05
        radius: height/2
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height*0.475
    }
    Rectangle {
        id: mid_bar_2
        border.width: 0
        width: parent.width*0.5
        height: parent.height*0.05
        radius: height/2
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height*0.475
    }

    Rectangle {
        id: bot_bar
        border.width: 0
        width: parent.width*0.5
        height: parent.height*0.05
        radius: height/2
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height*0.6
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if(parent.state == "menu")
                parent.state = "close"
            else
                parent.state = "menu"
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
                        targets: [top_bar, mid_bar, mid_bar_2, bot_bar]
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
                        targets: [top_bar, mid_bar, mid_bar_2, bot_bar]
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

    Component.onCompleted: {
        top_bar.color = Colors.text
        mid_bar.color = Colors.text
        mid_bar_2.color = Colors.text
        bot_bar.color = Colors.text
    }
}
