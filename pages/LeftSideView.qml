import QtQuick 2.0
import QtQuick.Controls 2.15
import "../control" as Control


Rectangle{
    id: sideBar

    signal toolSelected(string toolName, bool polygonState)

    implicitHeight: 500
    implicitWidth: 60
    color: "lime"
    border.color: Qt.lighter(color)
    radius: 10


    Column{
        spacing: 10
        anchors.fill: parent

        Control.CustomToolButtonImage{
            id: addPolygon

            property bool addIcon: true
            property bool addPolygonState: false

            property string iconsPath: "qrc:/images/svg/polygonAdd"

            function iconImage(iconState){
                if (iconState){
                    iconsPath =  "qrc:/images/svg/polygonAdd"
                }else{
                    iconsPath = "qrc:/images/svg/polygonClose"
                }
            }

            anchors.right: parent.right
            width: parent.width
            iconSource: iconsPath
            onClick: {
                addIcon = !addIcon
                addPolygonState = !addPolygonState
                toolSelected("addPolygon", addPolygonState)
                iconImage(addIcon)
            }
        }

        Control.CustomToolButtonImage{
            id: importPolygon
            anchors.right: parent.right
            width: parent.width
            iconSource: "qrc:/images/svg/import"
            onClick: {
                toolSelected("importPolygon")
            }
        }

        Control.CustomToolButtonImage{
            id: addLabel
            anchors.right: parent.right
            width: parent.width
            iconSource: "qrc:/images/svg/label"
            onClick: {
                toolSelected("addLabel")
            }

        }
    }

    states: State {
        name: "show"
        PropertyChanges {
            target: left_bar
            width: 50
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


