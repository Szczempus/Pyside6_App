import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id:toolButton

    property url iconSource: "qrc:/images/svg/tools"
    property string btnString: "Tools"
    property bool animation: false
    property int expectedWidth: 300
    property string fontFamily: "Ubuntu"
    signal click()

    implicitHeight: 50
    implicitWidth: toolButton.expectedWidth

    background: Rectangle{
        id:buttonBackground

        anchors.centerIn: parent
        anchors.fill: parent
        radius: buttonBackground.height * 0.5

        rotation: 180
        gradient: Gradient{
            orientation: Gradient.Horizontal
            GradientStop{ position:0.0; color:"#e6ff56" }
            GradientStop{ position:0.125; color:"#caff5e" }
            GradientStop{ position:0.25; color:"#a7ff62" }
            GradientStop{ position:0.375; color:"#76ff63" }
            GradientStop{ position:0.5; color:"#10f861" }
            GradientStop{ position:0.625; color:"#00e862" }
            GradientStop{ position:0.75; color:"#00dd6b" }
            GradientStop{ position:0.875; color:"#00d679" }
            GradientStop{ position:1; color:"#00d38d" }
        }
    }

    contentItem: Item{
        anchors.fill: parent
        width: parent.width
        id: content
        Text {
            id: buttonText
            clip:true
            text: toolButton.btnString
            font{
                pixelSize: 24
                family: toolButton.fontFamily
                bold: false
                styleName: "Regular"
            }
            anchors{
                verticalCenter: parent.verticalCenter
                horizontalCenter: parent.horizontalCenter
            }
            layer{
                enabled: true
                effect: DropShadow{
                    verticalOffset: 2
                    color: "#80000000"
                    radius: 1
                    samples: 3
                }
            }

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "#ffffff"



            property bool expanded: false

            width: expanded ? parent.width : 0

            Behavior on width{
                NumberAnimation {duration: 300}
            }

        }
    }

    MouseArea{
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: toolButton.animation

        onEntered: {
            if(toolButton.animation)
            {
                toolButton.state === "" ? toolButton.state = "show" : toolButton.state = ""
                buttonText.expanded = true
            }
        }
        onExited: {
            if(toolButton.animation)
            {
                toolButton.state === "show" ? toolButton.state = "" : toolButton.state = "show"
                buttonText.expanded = false
            }
        }

        onClicked: {
            toolButton.click()
        }
    }


    states: State{
        name: 'show'
        PropertyChanges {
            target: toolButton
            width: toolButton.implcitWidth
        }
    }

    transitions: Transition {
        from: ""
        to: "show"
        reversible:  true
        NumberAnimation{
            properties: "width"
            duration: 300
            easing.type: Easing.InOutCirc
        }

    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:2}
}
##^##*/
