import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "qrc:/qml/GUI/qml/GUI/Colors.js" as Colors
import "qrc:/qml/GUI/qml/GUI" as GUI

Item {
    id: control
    anchors.fill: parent


    property var receiverObject: undefined

    signal stringSet(string text, bool success)

    function getString(blocking, defaultString)
    {
        if(blocking)
        {
            background.visible = true
        }
        stringInput.text = defaultString
        selectAnalysisItemRoot.visible = true
        stringInput.focus = true

    }


    Rectangle{
        id: background
        anchors.fill: parent
        color: "black"
        opacity: 0.2
        visible: false

        MouseArea{
            anchors.fill: parent
            enabled: parent.visible
            hoverEnabled: enabled
        }
    }

    Item{
        id: selectAnalysisItemRoot
        anchors.centerIn: parent
        width: parent.width/2
        height: width/2
        visible: false

        Rectangle{
            anchors.fill: parent
            radius: 6
            color: Colors.main

            Column {
                anchors.fill: parent
                spacing: 0
                Text {
                    text: qsTr("New polygon name:")
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

                GUI.Separator {
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
                                control.stringSet(stringInput.text, true)
                                background.visible = false
                                selectAnalysisItemRoot.visible = false
                                stringInput.focus = false
                            }
                        }
                        else if(event.key == Qt.Key_Escape)
                        {
                            control.stringSet(stringInput.text, false)
                            background.visible = false
                            selectAnalysisItemRoot.visible = false
                            stringInput.focus = false
                        }
                    }

                }
                GUI.Separator {
                    separation: "column"
                }

                Row {
                    width: parent.width
                    height: parent.height/3 - 6
                    spacing: 0
                    GUI.ButtonText {
                        height: parent.height
                        width: parent.width/2
                        alignHCenter: true
                        text: qsTr("Back")
                        onClicked: {
                            control.stringSet(stringInput.text, false)
                            background.visible = false
                            selectAnalysisItemRoot.visible = false
                            stringInput.focus = false
                        }
                    }
                    GUI.ButtonText {
                        height: parent.height
                        width: parent.width/2
                        alignHCenter: true
                        text: qsTr("Create")
                        onClicked: {
                            if(stringInput.text != "")
                            {
                                control.stringSet(stringInput.text, true)
                                background.visible = false
                                selectAnalysisItemRoot.visible = false
                                stringInput.focus = false
                            }
                        }
                    }
                }
            }
        }
    }
}
