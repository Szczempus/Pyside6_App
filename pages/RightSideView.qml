import QtQuick 2.0
import QtQuick.Controls 2.15
import "../control" as Control


Rectangle{
    id: sideBar
    implicitHeight: 500
    implicitWidth: 60
    color: "lime"
    border.color: Qt.lighter(color)
    radius: 10

    states: State {
        name: "show"
        PropertyChanges {
            target: right_bar
            width: window.width * 0.25
        }
    }

    transitions: Transition {
        from: ""
        to: "show"
        reversible: true
        NumberAnimation{
            properties: "width"
            duration: 500
            easing.type: Easing.InOutCirc
        }
    }

}


