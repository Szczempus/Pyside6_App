import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0

Popup{
    id: loadingProgress

    property real showDuration: 300
    property real hideDuration: 300
    property int popupPolicy: Popup.NoAutoClose


    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2
    width: 300
    height: 300
    closePolicy: popupPolicy


    Text {
        id: mapLoadingScreen
        text: "Mapa ci się ładuje. I co się dziwisz? Duży plik to i chwilę to schodzi"
        anchors.fill: parent
        wrapMode: Text.Wrap
    }

    Text {
        id: spin
        text: "You spin me right round, baby"
        anchors.centerIn: parent

        NumberAnimation on rotation{
            from: 0; to: 360; running: spin.visible == true;
            loops: Animation.Infinite; duration: 700;
        }

    }

    enter: Transition {
         ParallelAnimation{
             NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: loadingProgress.showDuration }
             NumberAnimation { property: "y"; from: 1920; to: parent.height / 2 - height / 2 ; duration: loadingProgress.showDuration; easing.type: Easing.InOutQuad }
         }

        }
    exit: Transition {
        ParallelAnimation{
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0;  duration: loadingProgress.hideDuration}
            NumberAnimation { property: "y"; from: parent.height / 2 - height / 2 ; to: 1920; duration: loadingProgress.hideDuration; easing.type: Easing.InOutQuad}
        }


    }
}
