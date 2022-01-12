import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

RoundButton {
    id: minMaxButton

    property real buttonRadius: 100
    property string buttonColor: "red"
    property string iconUrl: "qrc:/images/svg/newCls"
    signal click()

    background: Rectangle{
        id: buttonBackground
        anchors{
            centerIn: parent
            fill: parent
        }
        color: minMaxButton.buttonColor
        width: minMaxButton.buttonRadius
        height: minMaxButton.buttonRadius
        radius: minMaxButton.buttonRadius * 0.5
    }

    contentItem: Item {
        id: content
        anchors{
            fill: parent
            margins: 5
        }

        width: parent.width
        Image {
            id: contentImage
            source: minMaxButton.iconUrl
            anchors{
                fill: parent
            }
            fillMode: Image.PreserveAspectFit
            antialiasing: true
            smooth: true
                       layer{
                enabled: true
                effect: DropShadow{
                    verticalOffset: 2
                    horizontalOffset: 2
                    color: "#80000000"
                    radius: 1
                    samples: 3
                }
            }
        }
        ColorOverlay{
            anchors.fill: contentImage
            source: contentImage
            color: "#ffffff"
        }
    }

    onClicked: {
        minMaxButton.click()
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:10}
}
##^##*/
