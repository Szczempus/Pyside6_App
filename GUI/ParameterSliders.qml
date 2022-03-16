import QtQuick 2.0
import QtQuick.Controls 2.15
import "./Colors.js" as Colors

Item {
    id: sliderTool

    property bool slidersVisible: false

    signal applyParams()
    signal cancelParams()

    property int minR: rangeSlider.left.value.toFixed()
    property int minG: rangeSlider.left.value.toFixed()
    property int minB: rangeSlider.left.value.toFixed()

    property int maxR: rangeSlider.right.value.toFixed()
    property int maxG: rangeSlider1.right.value.toFixed()
    property int maxB: rangeSlider2.right.value.toFixed()


    property int colorBalnace: rangeSlider3.value

    property var minList: [minB, minG, minR]
    property var maxList: [maxB, maxG, maxR]

    property var paramList: [minList, maxList, colorBalnace]

//    onSlidersVisibleChanged: {
//        if(slidersVisible){
//            paramSliderBgBlocker.visible = true
//        }
//        else
//            paramSliderBgBlocker.visible = false
//    }

    width: 500
    height: 200
    anchors.centerIn: parent
    visible: slidersVisible

//    Rectangle{
//        id: paramSliderBgBlocker
//        anchors.fill:window
//        color: "black"
//        opacity: 0.2
//        visible: false

//        MouseArea{
//            anchors.fill:window
//            enabled: window.visible
//            hoverEnabled: enabled
//        }
//    }

    Rectangle {
        anchors.centerIn: parent
        anchors.fill: parent
        color: "#566855"
        radius: 10
        visible: visibility

        Column {
            id: column
            anchors.fill: parent
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10

            Row {
                id: row
                width: column.width
                height: column.height/5


                Text {
                    id: text1
                    color: "#ffffff"
                    text: qsTr("R")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: minval.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 25
                }

                TextInput {
                    id: minval
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider.first.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: rangeSlider.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider.first.value = parseInt(text)
                    onFocusChanged: rangeSlider.first.value = parseInt(text)
                }

                RangeSlider {
                    id: rangeSlider
                    width: 324
                    height: column.height/5
                    anchors.right: maxval.left
                    stepSize: 1
                    to: 65535
                    anchors.rightMargin: 10
                    first.value: 0
                    second.value: 65535
                    first.onValueChanged: minR = rangeSlider.first.value.toFixed()
                    second.onValueChanged: maxR = rangeSlider.second.value.toFixed()

                }

                TextInput {
                    id: maxval
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider.second.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider.second.value = parseInt(text)
                    onFocusChanged: rangeSlider.second.value = parseInt(text)

                }

            }

            Row {
                id: row1
                width: column.width
                height: column.height/5
                anchors.top: row.bottom
                anchors.topMargin: 0

                Text {
                    id: text2
                    color: "#ffffff"
                    text: qsTr("G")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: minval1.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 25
                }

                TextInput {
                    id: minval1
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider1.first.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: rangeSlider1.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider1.first.value = parseInt(text)
                    onFocusChanged: rangeSlider1.first.value = parseInt(text)
                }

                RangeSlider {
                    id: rangeSlider1
                    width: 324
                    height: column.height/5
                    anchors.right: maxval1.left
                    to: 65535
                    first.value: 0
                    anchors.rightMargin: 10
                    second.value: 65535
                    stepSize: 1
                    first.onValueChanged: minG = rangeSlider1.first.value.toFixed()
                    second.onValueChanged: maxG = rangeSlider1.second.value.toFixed()

                }

                TextInput {
                    id: maxval1
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider1.second.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider1.second.value = parseInt(text)
                    onFocusChanged: rangeSlider1.second.value = parseInt(text)
                }

            }

            Row {
                id: row2
                width: column.width
                height: column.height/5
                anchors.top: row1.bottom
                anchors.topMargin: 0

                Text {
                    id: text3
                    color: "#ffffff"
                    text: qsTr("B")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: minval2.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 25
                }

                TextInput {
                    id: maxval2
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider2.second.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider2.second.value = parseInt(text)
                    onFocusChanged: rangeSlider2.second.value = parseInt(text)
                }

                RangeSlider {
                    id: rangeSlider2
                    width: 324
                    height: column.height/5
                    anchors.right: maxval2.left
                    second.value: 65535
                    first.value: 0
                    touchDragThreshold: 0
                    stepSize: 1
                    to: 65535
                    anchors.rightMargin: 10
                    first.onValueChanged: minB = rangeSlider2.first.value.toFixed()
                    second.onValueChanged: maxB = rangeSlider2.second.value.toFixed()
                }

                TextInput{
                    id: minval2
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider2.first.value.toFixed()
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: rangeSlider2.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 10
                    onAccepted: rangeSlider2.first.value = parseInt(text)
                    onFocusChanged: rangeSlider2.first.value = parseInt(text)

                }
            }

            Row {
                id: row3
                width: column.width
                height: column.height/5
                anchors.top: row2.bottom
                anchors.topMargin: 0

                Slider {
                    id: rangeSlider3
                    width: 324
                    height: column.height/5
                    anchors.right: maxval3.left
                    stepSize: 1
                    to: 100
                    from: 1
                    anchors.rightMargin: 10
                    onValueChanged: colorBalnace = rangeSlider3.value
                }

                Text {
                    id: text4
                    width: 60
                    color: "#ffffff"
                    text: qsTr("Color balance")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: rangeSlider3.left
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.Wrap
                    font.family: "Ubuntu"
                    fontSizeMode: Text.FixedSize
                    anchors.rightMargin: 37
                }

                Label {
                    id: maxval3
                    width: 30
                    color: "#ffffff"
                    text: rangeSlider3.value
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Ubuntu"
                    anchors.rightMargin: 10
                }
            }

            Row{
                id: row4
                width: column.width
                height: column.height/5
                anchors.top: row3.bottom
                anchors.topMargin: 0

                Button{
                    id: applyChanges
                    contentItem: Text{
                        text: "Apply"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
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
                        topMargin: 10
                    }

                    hoverEnabled: false

                    onClicked: {
                        sliderTool.applyParams()
                        menuTop.deactivateTool()
                        slidersWindow.slidersVisible = !slidersWindow.slidersVisible
                    }
                }

                Button{
                    id: refuseChanges
                    contentItem: Text{
                        text: "Cancel"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
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
                        topMargin: 10
                    }

                    hoverEnabled: false

                    onClicked: {
                        sliderTool.cancelParams()
                        menuTop.deactivateTool()
                        slidersWindow.slidersVisible = !slidersWindow.slidersVisible
                    }
                }
            }
        }
    }

}
