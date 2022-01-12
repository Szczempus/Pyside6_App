import QtQuick 2.15
import QtQuick.Controls 2.15

Button{
    id: root
    implicitHeight: 50
    implicitWidth: 200
    background:
        Rectangle{
            color: "lime"
            border.color: Qt.darker(color)
            radius: 10
           }
/*
    contentItem: MenuBarItem{
        Menu{
            title: qsTr("&File")
            Action {text: qsTr("&New Project")}
            Action {text: qsTr("&Open Project")}
            Action {text: qsTr("&Load Project")}
        }
    }
*/

    contentItem: Row {

    }


}

