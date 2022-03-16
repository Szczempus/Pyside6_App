import QtQuick 2.12
import QtQuick.Window 2.12
import "Colors.js" as Colors

Item {
    id: control

    implicitHeight: column.implicitHeight + radius
    implicitWidth: parent.height*3

    height: implicitHeight
    width: implicitWidth

    onHeightChanged: {
        if(state == "menu")
        {
            y = -height + topOffset
        }
        else
        {
            y = topOffset
        }
    }

    visible: y == -control.height + control.topOffset ? false : true

    Component.onCompleted: y = -height + topOffset

    clip: true

    property int radius: 6
    property double topOffset: 0

    signal actionTriggered(string action)

    states: [
        State {
            name: "menu"
        },
        State {
            name: "close"
        }
    ]
    state: "menu"

    transitions: [
        Transition {
            from: "menu"
            to: "close"
            PropertyAnimation {
                target: control
                property: "y"
                to: 0 + control.topOffset
            }
        },
        Transition {
            from: "close"
            to: "menu"
            PropertyAnimation {
                target: control
                property: "y"
                to: -control.height + control.topOffset
            }
        }
    ]

    Rectangle {
        id: background
        anchors.fill: parent
        anchors.bottomMargin: parent.radius
        color: Colors.main
    }

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        height: parent.radius*2
        width: parent.width - parent.radius*2
        color: Colors.main
    }

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        radius: parent.radius
        height: parent.radius*2
        width: parent.radius*4
        color: Colors.main
    }

    Column {
        id: column
        enabled: control.y == control.topOffset
        width: parent.width
        height: parent.height - parent.radius
        spacing: 0

        ButtonText {
            text: qsTr("NEW PROJECT")
            action: "action_newProject"
            onClicked: control.actionTriggered(action)
        }
        ButtonText {
            text: qsTr("OPEN PROJECT")
            action: "action_openProject"
            onClicked: control.actionTriggered(action)
        }
        ButtonText {
            text: qsTr("SAVE PROJECT")
            action: "action_saveProject"
            onClicked: control.actionTriggered(action)
        }
        Separator {
            separation: "column"
        }
        ButtonText {
            text: qsTr("IMPORT IMAGE")
            action: "action_importImage"
            onClicked: control.actionTriggered(action)
        }
        ButtonText {
            text: qsTr("SAVE IMAGE")
            action: "action_saveImage"
            onClicked: control.actionTriggered(action)
        }

        Separator {
            separation: "column"
        }
        ButtonText {
            text: qsTr("RUN ANALYSIS")
            action: "action_runAnalysis"
            onClicked: control.actionTriggered(action)
        }
        ButtonText {
            text: qsTr("CREATE REPORT")
            action: "action_createReport"
            onClicked: control.actionTriggered(action)
        }
        Separator {
            separation: "column"
        }
        ButtonText {
            text: qsTr("ABOUT")
            action: "action_about"
            onClicked: control.actionTriggered(action)
        }

    }
}
