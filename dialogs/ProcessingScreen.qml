import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0

import "../GUI/Colors.js" as Colors


Popup{
    id: loadingProgress

    property real showDuration: 500
    property real hideDuration: 500
    property int popupPolicy: Popup.NoAutoClose


    x: parent.width / 2 - width / 2
//    y: parent.height / 2 - height / 2
    implicitWidth: 300
    implicitHeight: 200
    closePolicy: popupPolicy

    background: Rectangle{
        anchors.fill: parent
        color: Colors.main
        radius: 5
    }

    Image{
        id: loadingMessageImage
        source: "../GUI/images/png_images/logo_biale.png"
        antialiasing: true
        smooth: true
        mipmap: true
        fillMode: Image.PreserveAspectFit
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        height: 100
    }


    Text{
        id: loadingText
        text: "PROCESSING..."
        wrapMode: Text.Wrap

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 10
        anchors.top: loadingMessageImage.bottom
        anchors.topMargin: 10
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        minimumPixelSize: 8
        font.pixelSize: 24
        fontSizeMode: Text.Fit
        color: Colors.text
        font.family: Colors.font

        SequentialAnimation on opacity {
            loops: Animation.Infinite

            NumberAnimation{
                from: 0.0
                to: 1.0
                duration:1000
                easing.type: Easing.InOutQuad
            }

            NumberAnimation{
                from: 1.0
                to: 0
                duration:1000
                easing.type: Easing.InOutQuad
            }
        }
    }



    enter: Transition {
         ParallelAnimation{
             NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: loadingProgress.showDuration }
             NumberAnimation { property: "y"; from: 1920; to: parent.height / 2 - implicitHeight / 2 ; duration: loadingProgress.showDuration; easing.type: Easing.OutCirc}
         }
    }
    exit: Transition {
        ParallelAnimation{
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0;  duration: loadingProgress.hideDuration}
            NumberAnimation { property: "y"; from: parent.height / 2 - implicitHeight / 2 ; to: 1920; duration: loadingProgress.hideDuration; easing.type: Easing.OutCirc}
        }
    }
}



