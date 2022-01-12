import QtQuick 2.12
import "Colors.js" as Colors

Item {
    id: control

    clip: true

    property string separation: "column" // "column" or "row" - depending on usage

    implicitHeight: separation == "row" ? parent.height - 10 : 2
    implicitWidth: separation == "row" ? 2 : parent.width - 10

    anchors.verticalCenter: separation == "row" ? parent.verticalCenter : undefined
    anchors.horizontalCenter: separation == "row" ? undefined : parent.horizontalCenter

    Rectangle {
        anchors.fill: parent
        color: Colors.highlighted_text
        radius: 2
    }

}
