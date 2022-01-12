import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: fileMenu

    property string headerText: "File"
    property variant items: ["New Project", "Open Project", "Load Report"]
    signal comboClicked;
    property int selectedIndex: listView.currentIndex;

    function newProjectCreated(){
        fileMenu.items = ["New Project", "Save Report ", "Open Project", "Load Report", "Import Image"]
    }

    radius: 10
    anchors{
        fill: parent
        leftMargin: 10
        rightMargin: 10
        topMargin: 10
        bottomMargin: 10
    }


    Rectangle {
        id:comboBox
        property alias selectedItem: chosenItemText.text;

        anchors.fill: parent
        z: 100;
        smooth:true;

        Rectangle {
            id:chosenItem
            radius:4;
            width:parent.width;
            height:comboBox.height;
            color: "lightsteelblue"
            smooth:true;
            Text {
                id:chosenItemText
                anchors{
                    top: parent.top
                    left: parent.left
                    margins: 8
//                    horizontalCenter: parent.horizontalCenter
//                    verticalCenter: parent.verticalCenter
                    centerIn: parent
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 18
                }
                text:fileMenu.headerText
                smooth:true
            }

            MouseArea {
                anchors.fill: parent;
                onClicked: {
                    comboBox.state = comboBox.state==="dropDown"?"":"dropDown"
                }
            }
        }

        Rectangle {
            id:dropDown
            width:comboBox.width;
            height:0;
            clip:true;
            radius:4;
            anchors{
                top:chosenItem.bottom
                margins: 2
            }
            color: "lightgray"

            ListView {
                id:listView
                height:500;
                model: fileMenu.items
                currentIndex: 0
                delegate: Item{
                    width:comboBox.width;
                    height: comboBox.height;

                    Text {
                        text: modelData
                        anchors{
                            top:parent.top
                            left: parent.left
                            margins: 5
                            horizontalCenter: parent.horizontalCenter
                            verticalCenter: parent.verticalCenter
                        }
                    }
                    MouseArea {
                        anchors.fill: parent;
                        onClicked: {
                            comboBox.state = ""
//                            var prevSelection = chosenItemText.text
//                            chosenItemText.text = modelData
//                            if(chosenItemText.text !== prevSelection){
                            listView.currentIndex = index;
                            fileMenu.comboClicked();

//                            }

                        }
                    }
                }
            }
        }
        Component {
            id: highlight
            Rectangle {
                width:comboBox.width;
                height:comboBox.height;
                color: "red";
                radius: 4
            }
        }

        states: State {
            name: "dropDown";
            PropertyChanges { target: dropDown; height:28*fileMenu.items.length }
        }

        transitions: Transition {
            NumberAnimation { target: dropDown; properties: "height"; easing.type: Easing.InOutQuad; duration: 500 }
        }
    }
}
