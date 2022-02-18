import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0

import "../GUI/Colors.js" as Colors

Popup{
    id: fileExistsEvent
    property real showDuration: 300
    property real hideDuration: 300
    property int popupPolicy: Popup.NoAutoClose

    signal override()
    signal noOverride()


    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2
//    width: 300
//    height: 50
    implicitHeight: 90
    implicitWidth: 300
    closePolicy: popupPolicy


    background: Rectangle{
        anchors.fill: parent
        color: Colors.main
        radius: 5
    }

    Text {
        id: fileExistsText
        text: "Projekt o takiej nazwie już istnieje. \n Czy chcesz go nadpisać?"
        color: Colors.text
        anchors{
            top: parent.top
            left: parent.left
            right:parent.right
        }

        wrapMode: Text.Wrap
        font{
            family:"Ubuntu"
            pixelSize: 14
            bold: true
        }
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
    }

    Button{
        id: overrideConfirmBt
        contentItem: Text{
            text: "Confirm"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
            color: Colors.highlighted_text
            anchors{
                top: parent.top
                horizontalCenter: parent.horizontalCenter
                verticalCenter: parent.verticalCenter
            }
            font{
                family: "Ubuntu"
                pixelSize: 14
                bold: true
            }
        }
        width: parent.width / 2 - 20
        height: 20
        background: Rectangle{
            color: Colors.highlighted_main
            radius: 5
        }
        hoverEnabled: false

        anchors{
            left: parent.left
            top: fileExistsText.bottom
            topMargin: 10
            leftMargin: 10
            bottomMargin: 10
        }

        onClicked: {
            fileExistsEvent.override()
            fileExistsEvent.close()
        }
    }

    Button{
        id: overrideCancelBt
        contentItem: Text{
            text: "Cancel"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
            color: Colors.highlighted_text
            anchors{
                top: parent.top
                horizontalCenter: parent.horizontalCenter
                verticalCenter: parent.verticalCenter
            }
            font{
                family: "Ubuntu"
                pixelSize: 14
                bold: true
            }
        }
        width: parent.width / 2 - 20
        height: 20
        background: Rectangle{
            color: Colors.highlighted_main
            radius: 5
        }
        hoverEnabled: false

        anchors{
            right: parent.right
            top: fileExistsText.bottom
            topMargin: 10
            leftMargin: 10
            bottomMargin: 10
        }

        onClicked: {
            fileExistsEvent.noOverride()
            fileExistsEvent.close()
        }
    }



}
