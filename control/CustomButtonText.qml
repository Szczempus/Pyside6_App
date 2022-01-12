import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
     id: customBtn

     property color colorDefault: "green"
     property color colorMouseOver: "limegreen"
     property color colorPressed: "lime"
     signal clicked

     onPressed: {
         customBtn.clicked()
         console.log("Clicked", customBtn.text)
     }


     QtObject{
         id: internal

         property var dynamicColor: if(customBtn.down){
                                        customBtn.down ? colorPressed : colorDefault
                                    }else{
                                        customBtn.hovered ? colorMouseOver : colorDefault
                                    }
     }
     text: qsTr("Default")
     implicitWidth: 200
     implicitHeight: 60

     background: Rectangle{
         color: internal.dynamicColor
         radius: 10
         border.color: Qt.lighter(color)
     }


     contentItem:
         Item{
         id: content
         anchors.fill: parent
               Text{
                     id: textField
                     text: customBtn.text
                     anchors.verticalCenter: parent.verticalCenter
                     anchors.horizontalCenter: parent.horizontalCenter
                 }

     }


}

/*##^##
Designer {
    D{i:0;formeditorZoom:4}
}
##^##*/
