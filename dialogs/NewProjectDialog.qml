import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs
//import QtGraphicalEffects 1.0

import "../GUI/Colors.js" as Colors

import Project

Item{

    id: control

    signal accepted ()
    signal rejected ()
    signal reset()

    state: "closed"

    function open(){
        newProjectDialog.open()
        control.state = "open"
    }

    function clear(){
        projectNameInput.text = ""
        projectDescriptionInput.text = ""
        projectLocationInput.text = ""
        projectDateInput.text = ""
        control.state = "closed"
    }

    function acc(){

//        appCore.prMeg.create_new_project(newProjectDialog.projectName, newProjectDialog.projectDescription, newProjectDialog.projectLocation, newProjectDialog.projectDate)
        papustka.create_new_project(newProjectDialog.projectName, newProjectDialog.projectDescription, newProjectDialog.projectLocation, newProjectDialog.projectDate)
        console.log(papustka.project_name,papustka.project_path)
        control.clear()
        newProjectDialog.close()

    }


    width: 300
    height: 440

    Pr{
        id:papustka
    }

    Dialog{
        id: newProjectDialog

        property string projectName: projectNameInput.text
        property string projectDescription: projectDescriptionInput.text
        property string projectLocation: projectLocationInput.text
        property string projectDate: projectDateInput.text

//        function clear(){
//            projectNameInput.text = ""
//            projectDescriptionInput.text = ""
//            projectLocationInput.text = ""
//            projectDateInput.text = ""
//        }

//        function acc(){
//            appCore.projectMenager.projectName = newProjectDialog.projectName
//            appCore.projectMenager.projectDescription = newProjectDialog.projectDescription
//            appCore.projectMenager.projectLocation = newProjectDialog.projectLocation
//            appCore.projectMenager.projectDate = newProjectDialog.projectDate
//            newProjectDialog.clear()
//        }

        width: parent.width
        height: parent.height


//        title: "New Project"
    //    standardButtons: StandardButton.Ok | StandardButton.Cancel


        Rectangle{
            id: projectNameContent
            height: parent.height / 4
            width: parent.width

            anchors{
                top: newProjectDialog.top
            }

            color: Colors.main

            Text{
                id: projectNameText
                text: "Nazwa Projektu"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                color: Colors.highlighted_text
                anchors{
                    top: projectNameContent.top
                    horizontalCenter: projectNameContent.horizontalCenter
                    topMargin: 10
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                    bold: true
                }

            }
            TextInput{
                id: projectNameInput
                anchors{
                    top: projectNameText.bottom
                    left: parent.left
                    right: parent.right
                    topMargin: 20
                    leftMargin: 2 * parent.width / 50
                    rightMargin: 2 * parent.width / 50
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                }
                activeFocusOnTab: true
//                color: activeFocus ? "lightblue" : "lightgrey"
                color: activeFocus ? Colors.text : Colors.highlighted_text
                maximumLength: parent.width
                focus: false
                clip: true
            }
            Rectangle{
                id: rect1
                anchors{
                    top:projectNameInput.bottom
                    left: projectNameContent.left
                    right: projectNameContent.right
                    leftMargin: 10
                    rightMargin: 10
                }
                radius: 2
                height: 5
                color:Colors.highlighted_main
            }

        }

        Rectangle{
            id: projectDescriptionContent
            width: parent.width
            height: parent.height / 4

            anchors{
                top: projectNameContent.bottom
            }

            color: Colors.main

            Text{
                id: projectDescriptionText
                text: "Opis Projektu"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                color: Colors.highlighted_text
                anchors{
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                    topMargin: 10
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                    bold: true
                }

            }
            TextInput{
                id: projectDescriptionInput
                anchors{
                    top: projectDescriptionText.bottom
                    left: parent.left
                    right: parent.right
                    topMargin: 20
                    leftMargin: 2 * parent.width / 50
                    rightMargin: 2 * parent.width / 50
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                }
                activeFocusOnTab: true
                color: activeFocus ? Colors.text : Colors.highlighted_text
                maximumLength: parent.width
                focus: false
                clip: true
            }
            Rectangle{
                id: rect2
                anchors{
                    top:projectDescriptionInput.bottom
                    left: projectDescriptionContent.left
                    right: projectDescriptionContent.right
                    leftMargin: 10
                    rightMargin: 10
                }
                radius: 2
                height: 5
                color:Colors.highlighted_main
            }

        }

        Rectangle{
            id: projectLocationContent
            width: parent.width
            height: parent.height / 4

            anchors{
                top: projectDescriptionContent.bottom
            }

            color: Colors.main

            Text{
                id: projectLocationText
                text: "Lokalizacja"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                color: Colors.highlighted_text
                anchors{
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                    topMargin: 10
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                    bold: true
                }

            }
            TextInput{
                id: projectLocationInput
                anchors{
                    top: projectLocationText.bottom
                    left: parent.left
                    right: parent.right
                    topMargin: 20
                    leftMargin: 2 * parent.width / 50
                    rightMargin: 2 * parent.width / 50
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                }
                activeFocusOnTab: true
                color: activeFocus ? Colors.text : Colors.highlighted_text
                focus: false
                clip: true
            }
            Rectangle{
                id:rect3
                anchors{
                    top:projectLocationInput.bottom
                    left: projectLocationContent.left
                    right: projectLocationContent.right
                    leftMargin: 10
                    rightMargin: 10
                }
                radius: 2
                height: 5
                color:Colors.highlighted_main
            }

        }

        Rectangle{
            id: projectDateContent
            width: parent.width
            height: parent.height / 4

            anchors{
                top: projectLocationContent.bottom
                bottom: parent.bottom
            }

            color: Colors.main

            Text{
                id: projectDateText
                text: "Data"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                color: Colors.highlighted_text
                anchors{
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                    topMargin: 10
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                    bold: true
                }

            }
            TextInput{
                id: projectDateInput
                anchors{
                    top: projectDateText.bottom
                    left: parent.left
                    right: parent.right
                    topMargin: 20
                    leftMargin: 2 * parent.width / 50
                    rightMargin: 2 * parent.width / 50
                }
                font{
                    family: "Ubuntu"
                    pixelSize: 14
                }
                activeFocusOnTab: true
                color: activeFocus ? Colors.text : Colors.highlighted_text
                focus: false
                clip: true
            }
            Rectangle{
                id:rect4
                anchors{
                    top:projectDateInput.bottom
                    left: projectDateContent.left
                    right: projectDateContent.right
                    leftMargin: 10
                    rightMargin: 10
                }
                radius: 2
                height: 5
                color:Colors.highlighted_main
            }

        }

        Rectangle{
            id: buttonsContainer
            width: parent.width
            height: 30
            anchors.bottom: parent.bottom
            color: Colors.main

            Button{
                id: okBtn
                contentItem: Text{
                    text: "Ok"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignTop
                    color: Colors.highlighted_text
                    anchors{
                        top: parent.top
                        horizontalCenter: parent.horizontalCenter
                        verticalCenter: parent.verticalCenter
                    }
                    font{
                        family: "Ubuntu"
                        pixelSize: 14
                        bold: true
                    }
                }
                width: parent.width / 2 - 20
                height: 20
                background: Rectangle{
                    color: Colors.highlighted_main
                    radius: 5
//                    border.width: 1
//                    border.color: "#ffffff"
                }
                anchors{
                    bottom: parent.bottom
                    left: parent.left
                    top: parent.top
                    leftMargin: 10
                    bottomMargin: 10
                }

                hoverEnabled: false

                onClicked: {
                    control.accepted()
                }
            }

            Button{
                id: cancelBtn
                contentItem: Text{
                    text: "Cancel"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignTop
                    color: Colors.highlighted_text
                    anchors{
                        top: parent.top
                        horizontalCenter: parent.horizontalCenter
                        verticalCenter: parent.verticalCenter
                    }
                    font{
                        family: "Ubuntu"
                        pixelSize: 14
                        bold: true
                    }
                }
                width: parent.width / 2 - 20
                height: 20
                background: Rectangle{
                    color: Colors.highlighted_main
                    radius: 5
                }
                anchors{
                    bottom: parent.bottom
                    right: parent.right
                    top: parent.top
                    rightMargin: 10
                    bottomMargin: 10
                }

                hoverEnabled: false

                onClicked: {
                    control.rejected()
                    newProjectDialog.close()
                }
            }
        }
    }

//    states: [
//        State {
//            name: "open"
//            PropertyChanges {
//                target: control
//            }
//        },
//        State {
//            name: "closed"
//            PropertyChanges {
//                target: control
//            }
//        }
//    ]

//    transitions: [
//        Transition {
//            from: "closed"
//            to: "open"
//            PropertyAnimation { target: control; properties: "visible"; to: "true"; duration: 100; easing: Easing.InOutCirc}
//        },
//        Transition {
//            from: "open"
//            to: "closed"
//            PropertyAnimation { target: control; properties: "visible"; to: "close"; duration: 100; easing: {type: Easing.InOutCirc}}
//        }
//    ]
}



