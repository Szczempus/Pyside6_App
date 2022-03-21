import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import "Colors.js" as Colors

Item {
    id: analysisResultControl

    property int radius: 6
    property double rightOffset: 10


    implicitHeight: Screen.height/4
    implicitWidth: Screen.height/3

    anchors.bottom: parent.bottom

    height: implicitHeight
    width: implicitWidth

    clip:true

    onWidthChanged: {
        if (state == "hidden")
        {
            x = -width + rightOffset
        }
        else
        {
            x = rightOffset
        }
    }

    onRightOffsetChanged: {
        if (state == "hidden")
        {
            x = -width + rightOffset
        }
        else
        {
            x = rightOffset
        }
    }

    visible: x == -analysisResultControl.height + analysisResultControl.rightOffset ? false : true

    Component.onCompleted: x = -width + rightOffset

    states:[
        State {name: "hidden"},
        State {name: "shown"}
            ]
    state: "hidden"

    transitions: [
        Transition {
            from: "hidden"
            to: "shown"
            PropertyAnimation{
                target: analysisResultControl
                property: "x"
                to: 0 + analysisResultControl.rightOffset
            }
        },
        Transition {
            from: "shown"
            to: "hidden"
            PropertyAnimation{
                target: analysisResultControl
                property: "x"
                to: -analysisResultControl.width + analysisResultControl.rightOffset
            }
        }
    ]

    Rectangle{
        id: analysisResultBackground
        anchors.fill: parent
        anchors.bottomMargin: parent.radius
        color: Colors.main
    }




}
