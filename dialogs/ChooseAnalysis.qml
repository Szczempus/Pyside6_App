import QtQuick 2.15
import QtQuick.Controls 2.15
//import QtGraphicalEffects
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
//import QtQuick.Controls.Styles
import "../GUI/Colors.js" as Colors
import "../GUI" as GUI
import "../control" as Control

Dialog{

    id: rootDialog

    property var polygonManager: undefined
    property int chosedAnalysis: 1

    implicitHeight: parent.height * 0.6
    implicitWidth: parent.width * 0.4

    //    width: 640
    //    height: 360

    anchors.centerIn: Overlay.overlay

    modal: true

    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: Item {

        id: control

        anchors.fill: parent

        Rectangle{
            id: background
            anchors.fill: parent
            color:Colors.main
            radius: 7
        }

        // Devide window by two columns
        Row{
            anchors.fill: parent

            // Left column with analysis radio buttons
            Column{
                id: leftColumn
                width: parent.width/2

                // Header
                Rectangle{
                    id:topTextAnalysis
                    width: parent.width
                    height: 20
                    color: Colors.main

                    Text{
                        anchors.fill: parent
                        text: "Analysis"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        color: Colors.text
                        font{
                            family: "Ubuntu"
                            pixelSize: 14
                            bold: true
                        }

                    }
                }

                // Content
                ButtonGroup{id: firstGroup}

                ColumnLayout{
                    spacing: 2

                    Control.CustomRadioButton{
                        checked: true
                        text: "NDVI MAP"
                        ButtonGroup.group: firstGroup
                        onClicked: {
                            rootDialog.chosedAnalysis = 1
                        }
                    }

                    Control.CustomRadioButton{
                        text: "LCI MAP"
                        ButtonGroup.group: firstGroup
                        onClicked: {
                            rootDialog.chosedAnalysis = 2
                        }
                    }

                    Control.CustomRadioButton{
                        text: "Segmentation"
                        ButtonGroup.group: firstGroup
                        onClicked: {
                            rootDialog.chosedAnalysis = 3
                        }
                    }

                    Control.CustomRadioButton{
                        text: "Counting"
                        ButtonGroup.group: firstGroup
                        onClicked: {
                            rootDialog.chosedAnalysis = 4
                        }
                    }
                }
            }

            // Columns separator
            GUI.Separator{
                separation: "row"
            }

            // Right column with polygon list and combo boxes
            Flickable {
                width: background.width/2
                height: background.height
                clip: true

                flickableDirection: Flickable.AutoFlickIfNeeded
                ScrollBar.vertical: ScrollBar {
                    policy: "AsNeeded"
                }

                contentHeight: column.height

                Column {
                    id: column
                    width: parent.width
                    spacing: 0

                    Repeater {
                        model: rootDialog.polygonManager.polygonList

                        delegate:
                            Item {
                            id: polyItem
                            width: column.width
                            height: polyItem.listOpened ? Screen.height/30 + subcolumn.implicitHeight : Screen.height/30
                            property string name: modelData.name
                            property bool listOpened: false
                            property var polygon: modelData
                            onStateChanged: {
                                console.log(polygon.isChecked)
                                if(state == "hovered")
                                    polygon.hovered = true
                                else
                                    polygon.hovered = false
                            }

                            states: [
                                State { name: "normal" },
                                State { name: "hovered" }
                            ]
                            state: "normal"

                            transitions: [
                                Transition {
                                    from: "normal"
                                    to: "hovered"
                                    ParallelAnimation {
                                        PropertyAnimation {
                                            target: image
                                            property: "opacity"
                                            to: 0.0
                                            duration: 300
                                        }
                                        PropertyAnimation {
                                            target: polyItemBg
                                            property: "color"
                                            to: Colors.highlighted_main
                                            duration: 300
                                        }
                                        PropertyAnimation {
                                            target: polyName
                                            property: "color"
                                            to: Colors.highlighted_text
                                            duration: 300
                                        }
                                    }
                                },
                                Transition {
                                    from: "hovered"
                                    to: "normal"
                                    ParallelAnimation {
                                        PropertyAnimation {
                                            target: image
                                            property: "opacity"
                                            to: 1.0
                                            duration: 300
                                        }
                                        PropertyAnimation {
                                            target: polyItemBg
                                            property: "color"
                                            to: Colors.main
                                            duration: 300
                                        }
                                        PropertyAnimation {
                                            target: polyName
                                            property: "color"
                                            to: Colors.text
                                            duration: 300
                                        }
                                    }
                                }
                            ]

                            Rectangle {
                                id: polyItemBg
                                width: column.width
                                height: Screen.height/30
                                Component.onCompleted: color = Colors.main
                            }

                            Item {
                                id: image
                                height: Screen.height/60
                                width: height
                                anchors.verticalCenter: polyName.verticalCenter
                                antialiasing: true
                                smooth: true
                                opacity: 1
                                x: polyName.padding/2

                                Control.CustomCheckBox{
                                    id:checkBox
                                    width: image.height
                                    height: image.height
                                    anchors.left: image.anchors.left
                                    isChecked: false
                                    onCheckedChange: {
                                        polyItem.polygon.isChecked = checkStatus
                                    }
                                }
                            }

                            Image {
                                height: Screen.height/60
                                width: height
                                anchors.verticalCenter: polyName.verticalCenter
                                fillMode: Image.PreserveAspectFit
                                source: "qrc:/images/png/arrow_highlighted"
                                antialiasing: true
                                mipmap: true
                                smooth: true
                                opacity: 1 - image.opacity
                                rotation: polyItem.listOpened ? 90 : 0
                                x: polyName.padding/2
                            }

                            Text {
                                id: polyName
                                width: column.width - height
                                anchors.right: parent.right
                                anchors.rightMargin: height/2
                                height: Screen.height/30
                                padding: 6
                                text: parent.name
                                minimumPixelSize: 8
                                font.pixelSize: 16
                                fontSizeMode: Text.VerticalFit
                                Component.onCompleted: color = Colors.text

                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignLeft
                                elide: Text.ElideRight

                            }

                            MouseArea {
                                width: column.width - checkBox.width
                                height: Screen.height/30
                                hoverEnabled: true
                                anchors.right: parent.right
                                onEntered: parent.state = "hovered"
                                onExited: parent.state = "normal"
                                onClicked: {
                                    if(polyItem.listOpened == true)
                                        polyItem.listOpened = false
                                    else
                                        polyItem.listOpened = true
                                }
                            }


                            // Deleting polygon
                            //                            Image {
                            //                                height: Screen.height/60
                            //                                width: height
                            //                                anchors.right: parent.right
                            //                                anchors.verticalCenter: polyName.verticalCenter
                            //                                fillMode: Image.PreserveAspectFit
                            //                                source: "qrc:/images/png/delete_cross"
                            //                                antialiasing: true
                            //                                mipmap: true
                            //                                smooth: true
                            //                                opacity: 1 - image.opacity
                            //                                rotation: image.rotation
                            //                                anchors.rightMargin: polyName.padding/2
                            //                                MouseArea {
                            //                                    anchors.fill: parent
                            //                                    onClicked: {rootDialog.polygonManager.deletePolygon(polyItem.polygon)
                            //                                        //                                appManager.polygonManager.deletePolygon(polyItem.polygon)
                            //                                    }
                            //                                }
                            //                            }


                            Column {
                                id: subcolumn
                                anchors.topMargin: Screen.height/30
                                anchors.fill: parent
                                spacing: 0
                                height: polyItem.listOpened ? implicitHeight : 0
                                visible: polyItem.listOpened
                                Repeater {
                                    model: modelData.pointList

                                    delegate: Item {
                                        width: subcolumn.width
                                        height: Screen.height/40
                                        property var coordsItem: modelData
                                        property double xCoord: modelData.x
                                        property double yCoord: modelData.y

                                        states: [
                                            State { name: "normal" },
                                            State { name: "hovered" }
                                        ]
                                        state: "normal"

                                        onStateChanged: {
                                            if(state == "hovered")
                                                coordsItem.hovered = true
                                            else
                                                coordsItem.hovered = false
                                        }

                                        transitions: [
                                            Transition {
                                                from: "normal"
                                                to: "hovered"
                                                ParallelAnimation {
                                                    PropertyAnimation {
                                                        target: deleteCoordImage
                                                        property: "opacity"
                                                        to: 1.0
                                                        duration: 300
                                                    }
                                                    PropertyAnimation {
                                                        target: coordsBg
                                                        property: "color"
                                                        to: Colors.highlighted_main
                                                        duration: 300
                                                    }
                                                    PropertyAnimation {
                                                        targets: [xText, yText]
                                                        property: "color"
                                                        to: Colors.highlighted_text
                                                        duration: 300
                                                    }
                                                }
                                            },
                                            Transition {
                                                from: "hovered"
                                                to: "normal"
                                                ParallelAnimation {
                                                    PropertyAnimation {
                                                        target: deleteCoordImage
                                                        property: "opacity"
                                                        to: 0.0
                                                        duration: 300
                                                    }
                                                    PropertyAnimation {
                                                        target: coordsBg
                                                        property: "color"
                                                        to: Colors.main
                                                        duration: 300
                                                    }
                                                    PropertyAnimation {
                                                        targets: [xText, yText]
                                                        property: "color"
                                                        to: Colors.text
                                                        duration: 300
                                                    }
                                                }
                                            }
                                        ]

                                        Rectangle {
                                            id: coordsBg
                                            anchors.fill: parent
                                            Component.onCompleted: color = Colors.main
                                        }

                                        Text {
                                            id: xText
                                            text: "x: " + xCoord
                                            width: subcolumn.width/2 - padding
                                            height: Screen.height/40
                                            color: Colors.text

                                            leftPadding: 3 + Screen.height/40
                                            padding: 3
                                            minimumPixelSize: 8
                                            font.pixelSize: 13
                                            fontSizeMode: Text.VerticalFit

                                            verticalAlignment: Text.AlignVCenter
                                            horizontalAlignment: Text.AlignLeft
                                            elide: Text.ElideRight
                                        }

                                        Text {
                                            id: yText
                                            text: "y: " + yCoord
                                            anchors.left: xText.right
                                            width: subcolumn.width/2 - xText.leftPadding
                                            height: Screen.height/40
                                            color: Colors.text

                                            leftPadding: 3
                                            padding: 3
                                            minimumPixelSize: 8
                                            font.pixelSize: 13
                                            fontSizeMode: Text.VerticalFit

                                            verticalAlignment: Text.AlignVCenter
                                            horizontalAlignment: Text.AlignLeft
                                            elide: Text.ElideRight
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            onEntered: parent.state = "hovered"
                                            onExited: parent.state = "normal"
                                        }

                                        // Deleting polygon coordinates

                                        //                                        Image {
                                        //                                            id: deleteCoordImage
                                        //                                            height: Screen.height/60
                                        //                                            width: height
                                        //                                            anchors.right: parent.right
                                        //                                            anchors.verticalCenter: coordsBg.verticalCenter
                                        //                                            fillMode: Image.PreserveAspectFit
                                        //                                            source: "qrc:/images/png/delete_cross"
                                        //                                            antialiasing: true
                                        //                                            mipmap: true
                                        //                                            smooth: true
                                        //                                            opacity: 0
                                        //                                            visible: opacity > 0.0 ? true : false
                                        //                                            rotation: image.rotation
                                        //                                            anchors.rightMargin: polyName.padding/2
                                        //                                            MouseArea {
                                        //                                                anchors.fill: parent
                                        //                                                onClicked: {
                                        //                                                    if(polyItem.polygon.pointList.length > 3)
                                        //                                                        polyItem.polygon.removePoint(coordsItem)
                                        //                                                }
                                        //                                            }
                                        //                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
