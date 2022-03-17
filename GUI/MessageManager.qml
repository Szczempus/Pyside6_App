import QtQuick 2.12
import "Colors.js" as Colors

Item {
    id: manager
    anchors.fill: parent

    property var receiverObject: undefined

    signal stringSet(string text, bool success)

    function getString(blocking, defaultString)
    {
        if(blocking)
        {
            bgBlocker.visible = true
        }
        stringInput.text = defaultString
        getStringItem.visible = true
        stringInput.focus = true

    }

    Rectangle {
        id: bgBlocker
        anchors.fill: parent
        color: "black"
        opacity: 0.2
        visible: false

        MouseArea {
            anchors.fill: parent
            enabled: parent.visible
            hoverEnabled: enabled
        }
    }


    Item {
        id: getStringItem
        anchors.centerIn: parent
        width: parent.width/4
        height: width/2
        visible: false

        Rectangle {
            anchors.fill: parent
            radius: 6
            color: Colors.main
            Column {
                anchors.fill: parent
                spacing: 0
                Text {
                    text: qsTr("Nowy poligon:")
                    color: Colors.text
                    width: parent.width
                    height: parent.height/3 - 4

                    padding: 8
                    minimumPixelSize: 8
                    font.pixelSize: 16
                    fontSizeMode: Text.VerticalFit

                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    elide: Text.ElideRight
                }

                Separator {
                    separation: "column"
                }

                TextInput {
                    id: stringInput
                    text: "input"
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    color: Colors.text
                    width: parent.width-16
                    height: parent.height/3
                    clip: true
                    leftPadding: 3
                    rightPadding: 3
                    maximumLength: 32
                    selectByMouse: true
                    selectedTextColor: Colors.highlighted_text
                    selectionColor: Colors.highlighted_main

                    font.pixelSize: 0.16 * parent.height

                    focus: false
                    Keys.onPressed: {
                        if (event.key == Qt.Key_Return)
                        {
                            if(stringInput.text != "")
                            {
                                manager.stringSet(stringInput.text, true)
                                bgBlocker.visible = false
                                getStringItem.visible = false
                                stringInput.focus = false
                            }
                        }
                        else if(event.key == Qt.Key_Escape)
                        {
                            manager.stringSet(stringInput.text, false)
                            bgBlocker.visible = false
                            getStringItem.visible = false
                            stringInput.focus = false
                        }
                    }

                }
                Separator {
                    separation: "column"
                }

                Row {
                    width: parent.width
                    height: parent.height/3 - 6
                    spacing: 0
                    ButtonText {
                        height: parent.height
                        width: parent.width/2
                        alignHCenter: true
                        text: qsTr("Back")
                        onClicked: {
                            manager.stringSet(stringInput.text, false)
                            bgBlocker.visible = false
                            getStringItem.visible = false
                            stringInput.focus = false
                        }
                    }
                    ButtonText {
                        height: parent.height
                        width: parent.width/2
                        alignHCenter: true
                        text: qsTr("Create")
                        onClicked: {
                            if(stringInput.text != "")
                            {
                                manager.stringSet(stringInput.text, true)
                                bgBlocker.visible = false
                                getStringItem.visible = false
                                stringInput.focus = false
                            }
                        }
                    }
                }
            }
        }
    }

}
