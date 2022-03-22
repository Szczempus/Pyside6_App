import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import "Colors.js" as Colors
import "./" as GUI

Item {
    id: analysisResultControl

    property int radius: 6
    property double rightOffset: 10
    property var model: undefined

    function getPolygon(polygon){
        console.log(polygon)
        var analysisData = polygon.polygonAnalysis
        polygonNameArea.text = polygon.name
        polygonAnalysisName.text = analysisData.analysisType
        analysisResultControl.model = analysisData.analysisModel

    }

//    property var model: ["Współrzędne: ", "Liczba detekcji: ", "Obiekty zdrowe: ","Obiekty chore: ", "Wartość wskaźnika: "]

    implicitHeight: Screen.height/4
    implicitWidth: Screen.height/3

    anchors.bottom: parent.bottom
    anchors.bottomMargin: 0

    height: implicitHeight
    width: implicitWidth

    clip:true

//    onWidthChanged: {
//        if (state == "hidden")
//        {
//            x = -width + rightOffset
//        }
//        else
//        {
//            x = rightOffset
//        }
//    }

//    onRightOffsetChanged: {
//        if (state == "hidden")
//        {
//            x = -width + rightOffset
//        }
//        else
//        {
//            x = rightOffset
//        }
//    }

//    visible: x == -analysisResultControl.height + analysisResultControl.rightOffset ? false : true

    Component.onCompleted: x = Screen.width - radius

    states:[
        State {name: "hidden"},
        State {name: "shown"}
            ]
    state: "hidden"

    transitions: [
        Transition {
            from: "hidden"
            to: "shown"
            PropertyAnimation{
                target: analysisResultControl
                property: "x"
                to: parent.width - analysisResultControl.width /*- analysisResultControl.radius*/
            }
        },
        Transition {
            from: "shown"
            to: "hidden"
            PropertyAnimation{
                target: analysisResultControl
                property: "x"
                to: Screen.width
            }
        }
    ]

    Rectangle{
        id: analysisResultBackground
        anchors.fill: parent
        anchors.leftMargin: parent.radius
        color: Colors.main
    }

    Rectangle{
        anchors.right: parent.right
        anchors.top: parent.top
        height: parent.radius*2
        width: parent.width - parent.radius*2
        color: Colors.main
    }

    Rectangle{
        anchors.left: parent.left
        anchors.top: parent.top
        radius: parent.radius
        height: parent.radius*2
        width: parent.radius*4
        color: Colors.main
    }

    Rectangle{
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        width: parent.radius*2
        height: parent.height-parent.radius
        color:Colors.main

    }

    Rectangle{
       id: analysisHeader
       anchors.right: parent.right
       anchors.top: parent.top
       anchors.topMargin: parent.radius
       color:Colors.main
       width: parent.width - parent.radius
       height: parent.height/4

       Text{
           id: polygonNameArea
           font.pixelSize: 24
           fontSizeMode: Text.Fit
           font.family: Colors.font
           anchors.left: parent.left
           anchors.top: parent.top
           width: parent.width
           height: parent.height/3 * 2
           text: "POLYGON_NAME"
           verticalAlignment: Text.AlignVCenter
           horizontalAlignment: Text.AlignLeft
           color: Colors.text

       }

       Text{
           id: polygonAnalysisName
           font.pixelSize: 16
           fontSizeMode: Text.Fit
           font.family: Colors.font
           anchors.left: parent.left
           anchors.bottom: parent.bottom
           width: parent.width
           height: parent.height/3
           text: "POLYGON_ANALYSIS_NAME"
           verticalAlignment: Text.AlignVCenter
           horizontalAlignment: Text.AlignLeft
           color: Colors.text
       }
    }

    GUI.Separator{
        id:analysisSeparator
        anchors.top: analysisHeader.bottom
        anchors.left: parent.left
        anchors.leftMargin: parent.radius
        width: parent.width
        height: 5
        anchors.topMargin: 5
        separation: "column"
    }

    Rectangle{
        id: flickableBacground
        anchors.top: analysisSeparator.bottom
        anchors.topMargin: 5
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        color: Colors.main

        Flickable{
            width: parent.width
            height: parent.height

            clip: true

            flickableDirection: Flickable.AutoFlickIfNeeded
            ScrollBar.vertical: ScrollBar{
                policy: "AsNeeded"
            }

            contentHeight: analysisColumn.height

            Column{
                id: analysisColumn

                width: parent.width
                spacing: 0
                clip: true

                Repeater{
                    model:analysisResultControl.model
                    delegate: Item{
                        id: analysisItem

                        property string test: modelData
                        width: 300
                        height: Screen.height/20

                        Rectangle{
                            id: analysisItemBg
                            width: analysisColumn.width
                            height: Screen.height/20
                            color: Colors.main

                        }

                        Text {
                            id: analysisItemName
                            width: analysisColumn.width - height
                            anchors.left: analysisItemBg.left
                            height: Screen.height/20
                            padding: analysisResultControl.radius
                            text: test
                            minimumPixelSize: 8
                            font.pixelSize: 16
                            fontSizeMode: Text.VerticalFit
                            Component.onCompleted: color = Colors.text
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignLeft
                            elide: Text.ElideRight
                        }
                    }
                }
            }
        }
    }
}
