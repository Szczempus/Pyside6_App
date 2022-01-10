import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    Button{
       id: but
       anchors.centerIn: parent
       width: 200
       height: 100
       text: qsTr("Click me")
       onClicked: {
           appCore.changeNameProject()
       }
    }
}
