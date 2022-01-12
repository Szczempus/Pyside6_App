import QtQuick 2.15
import QtGraphicalEffects 1.15

Rectangle{
    id: background
    anchors.fill: parent

    RectangularGlow{
        id: effect
        anchors.fill: front
        glowRadius: 10
        spread: 0.2
        color: "white"
        cornerRadius: front.radius + glowRadius
    }
     Rectangle{
         id:front
         color: "black"
         anchors.centerIn: parent
         width: Math.round(parent.width/1.5)
         height: Math.round(parent.height/2)
         radius: 25
     }
}
