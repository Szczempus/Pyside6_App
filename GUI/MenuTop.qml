import QtQuick 2.12
import QtQuick.Window 2.12
import "Colors.js" as Colors

Item {
    id: control

    implicitHeight: Screen.height/20
    implicitWidth: parent.width

    height: implicitHeight
    width: implicitWidth

    clip: false

    property bool toolbarVisible: false
    property string projectName: ""

    signal actionTriggered(string action)
    signal toolSelected(string tool, bool active)

    function deactivateTool() {
        toolbarPolygon.deactivateLastTool()
    }

    SlideMenu {
        topOffset: control.height
        state: buttonMenu.state
        onActionTriggered: {
            buttonMenu.state = "menu"
            control.actionTriggered(action)
        }
    }

    Rectangle {
        id: background
        anchors.fill: parent
        color: Colors.main
    }

    ButtonMenu {
        id: buttonMenu
    }

    Image {
        id: imageLogo
        source: "./images/png_images/logo_biale.png"
        antialiasing: true
        smooth: true
        mipmap: true
        fillMode: Image.PreserveAspectFit
        height: parent.height
        width: height*2
        anchors.left: buttonMenu.right
    }

    ToolbarPolygon {
        id: toolbarPolygon
        visible: toolbarVisible
        onActionTriggered: {
            control.actionTriggered(action)
        }
        onToolSelected: {
            control.toolSelected(tool, active)
        }
    }

    Image{
        id: polygonListScroll
        height: Screen.height/20
        width: height
        anchors.right: projectNameText.left
        fillMode: Image.PreserveAspectFit
        source: "./images/png_images/arrow.png"
        antialiasing: true
        mipmap: true
        smooth: true
        opacity: 1
        rotation: 0
        visible: toolbarVisible

        states: [
            State { name: "closed"},
            State { name: "opened"}
        ]

        state: "closed"

        MouseArea{
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                if(polygonListScroll.state == "closed"){
                    polygonListScroll.state = "opened"
                    polygonListScroll.rotation = 90
                    polygonList.state = "shown"
                }else if (polygonListScroll.state == "opened"){
                    polygonListScroll.state = "closed"
                    polygonListScroll.rotation = 0
                    polygonList.state = "hidden"
                }

            }
        }
    }

    Item {
        id: projectNameText
        visible: projectName != ""
        clip: true
        height: parent.height
        width: height*3
        anchors.right: parent.right

        Text {
            text: qsTr("PROJEKT")
            anchors.top: parent.top
            anchors.margins: parent.height/10
            height: parent.height*0.4
            width: parent.width

            minimumPixelSize: 8
            font.pixelSize: 16
            fontSizeMode: Text.Fit
            color: Colors.highlighted_text
            font.bold: true
            font.family: Colors.font

            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            elide: Text.ElideRight

        }
        Text {
            text: appCore.prMeg.project_name
            anchors.bottom: parent.bottom
            anchors.margins: parent.height/10
            height: parent.height*0.4
            width: parent.width

            minimumPixelSize: 8
            font.pixelSize: 16
            fontSizeMode: Text.Fit
            color: Colors.text
            font.family: Colors.font

            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            elide: Text.ElideLeft

        }
    }



}
