import QtQuick 2.0
import QtQuick.Controls 2.12

Item {
    id: sliderTool
    property bool slidersVisible: false

    anchors.centerIn: parent
    width: 500
    height: 200

    Rectangle {
        anchors.centerIn: parent
        anchors.fill: parent
        color: "#566855"
        radius: 10
        visible: slidersVisible

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
                height: column.height/4



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

                Label {
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
                }

                RangeSlider {
                    id: rangeSlider
                    width: 324
                    height: column.height/4
                    anchors.right: maxval.left
                    stepSize: 1
                    to: 65535
                    anchors.rightMargin: 10
                    first.value: 0
                    second.value: 65535
                }

                Label {
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
                }

            }

            Row {
                id: row1
                width: column.width
                height: column.height/4
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

                Label {
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
                }

                RangeSlider {
                    id: rangeSlider1
                    width: 324
                    height: column.height/4
                    anchors.right: maxval1.left
                    to: 65535
                    first.value: 0
                    anchors.rightMargin: 10
                    second.value: 65535
                    stepSize: 1

                }

                Label {
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
                }

            }

            Row {
                id: row2
                width: column.width
                height: column.height/4
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

                Label {
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
                }

                RangeSlider {
                    id: rangeSlider2
                    width: 324
                    height: column.height/4
                    anchors.right: maxval2.left
                    second.value: 65535
                    first.value: 0
                    touchDragThreshold: 0
                    stepSize: 1
                    to: 65535
                    anchors.rightMargin: 10
                }

                Label {
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
                }
            }

            Row {
                id: row3
                width: column.width
                height: column.height/4
                anchors.top: row2.bottom
                anchors.topMargin: 0

                Slider {
                    id: rangeSlider3
                    width: 324
                    height: column.height/4
                    anchors.right: maxval3.left
                    stepSize: 1
                    to: 100
                    anchors.rightMargin: 10
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
        }
    }

}
