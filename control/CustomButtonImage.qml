import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id:customBtnImg

    property url btnIconSource: "qrc:/images/svg/plus"
    property color colorDefault: "green"
    property color colorMouseOver: "limegreen"
    property color colorPressed: "lime"

    QtObject{
        id: internal

        property var dynamicColor: if(customBtnImg.down){
                                       customBtnImg.down ? colorPressed : colorDefault
                                   }else{
                                       customBtnImg.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitHeight: 60
    implicitWidth: 60

    background: Rectangle {
        id: bcgBtn
        color: internal.dynamicColor
        radius: 10
        border.color: Qt.lighter(color)

        Image {
            id: iconBtn
            source: btnIconSource
            anchors.fill: parent
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            height: 25
            width: 25
            fillMode: Image.PreserveAspectFit

//            MouseArea{
//                anchors.fill: parent
//                onClicked: {
//                    customBtnImg.clicked()
//                    console.log("Clicked customBtnImg from onClicked MouseArea")}
//            }
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            antialiasing: false
        }
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.66;height:100;width:200}
}
##^##*/
