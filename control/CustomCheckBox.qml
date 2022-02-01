import QtQuick 2.15
//import QtGraphicalEffects 1.15
import "../GUI/Colors.js" as Colors

Item {
    id: control

    property bool isChecked: undefined

    signal checkedChange(var checkStatus)

    implicitHeight: parent.height
    implicitWidth: parent.width



    Rectangle {
        id: rectangle
        width: parent.width
        height: parent.height
        color: "#ffffff"
        radius: 6
    }

    Image {
        id: image
        width: parent.width * 0.6
        height: parent.height * 0.6
        source: "../GUI/images/png_images/checked.png"
        fillMode: Image.PreserveAspectFit
        visible: isChecked
        anchors.verticalCenter: rectangle.verticalCenter
        anchors.horizontalCenter: rectangle.horizontalCenter
        antialiasing: true
        mipmap: true

    }

//    ColorOverlay{
//        anchors.fill: image
//        source: image
//        color: Colors.main
//        visible: control.isChecked
//    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: {
            control.isChecked ? control.isChecked = false : control.isChecked = true
            control.checkedChange(control.isChecked)
        }
    }

}
