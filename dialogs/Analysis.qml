import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        id: parentBg
        color: "#566855"
        anchors.fill: parent

        Row {
            id: row
            anchors.fill: parent

            Rectangle {
                id: leftSpace
                color: "#ffffff"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: 0
                anchors.topMargin: 0
                anchors.bottomMargin: 0

                Flickable {
                    id: flickable
                    width: 300
                    height: 300

                    Column {
                        id: column
                        width: 200
                        height: 400

                        Button {
                            id: button
                            text: qsTr("Button")
                        }

                        Button {
                            id: button1
                            text: qsTr("Button1")
                        }

                        Button {
                            id: button2
                            text: qsTr("Button2")
                        }

                        Button {
                            id: button3
                            text: qsTr("Button3")
                        }
                    }
                }
            }


            Rectangle {
                id: rightSpace
                color: "#ffffff"
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 0
                anchors.topMargin: 0
                anchors.bottomMargin: 0
            }

        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:6}D{i:7}D{i:8}D{i:9}D{i:5}D{i:4}D{i:3}
D{i:10}D{i:2}D{i:1}
}
##^##*/
