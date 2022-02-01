import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import "Colors.js" as Colors

Item {
    id: control

    property var polygonManager: undefined

    implicitHeight: column.implicitHeight + radius
    implicitWidth: Screen.height*4/20

    anchors.right: parent.right

    height: implicitHeight > Screen.height/3 ? Screen.height/3 : implicitHeight
    width: implicitWidth

    onHeightChanged: {
        if(state == "hidden")
        {
            y = -height + topOffset
        }
        else
        {
            y = topOffset
        }
    }

    onTopOffsetChanged: {
        if(state == "hidden")
        {
            y = -height + topOffset
        }
        else
        {
            y = topOffset
        }
    }

    visible: y == -control.height + control.topOffset ? false : true

    Component.onCompleted: y = -height + topOffset

    clip: true

    property int radius: 6
    property double topOffset: 0

    states: [
        State {
            name: "hidden"
        },
        State {
            name: "shown"
        }
    ]
    state: "hidden"

    transitions: [
        Transition {
            from: "hidden"
            to: "shown"
            PropertyAnimation {
                target: control
                property: "y"
                to: 0 + control.topOffset
            }
        },
        Transition {
            from: "shown"
            to: "hidden"
            PropertyAnimation {
                target: control
                property: "y"
                to: -control.height + control.topOffset
            }
        }
    ]

    Rectangle {
        id: background
        anchors.fill: parent
        anchors.bottomMargin: parent.radius
        color: Colors.main
    }

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        height: parent.radius*2
        width: parent.width - parent.radius*2
        color: Colors.main
    }

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        radius: parent.radius
        height: parent.radius*2
        width: parent.radius*4
        color: Colors.main
    }

    Flickable {
        width: parent.width
        height: parent.height - control.radius
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
                model: control.polygonManager.polygonList

                delegate: Item {
                    id: polyItem
                    width: column.width
                    height: polyItem.listOpened ? Screen.height/30 + subcolumn.implicitHeight : Screen.height/30
                    property string name: modelData.name
                    property bool listOpened: false
                    property var polygon: modelData
                    onStateChanged: {
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

                    Image {
                        id: image
                        height: Screen.height/60
                        width: height
                        anchors.verticalCenter: polyName.verticalCenter
                        fillMode: Image.PreserveAspectFit
                        source: "./images/png_images/arrow"
                        antialiasing: true
                        mipmap: true
                        smooth: true
                        opacity: 1
                        x: polyName.padding/2
                        rotation: polyItem.listOpened ? 90 : 0
                    }

                    Image {
                        height: Screen.height/60
                        width: height
                        anchors.verticalCenter: polyName.verticalCenter
                        fillMode: Image.PreserveAspectFit
                        source: "./images/png_images/arrow_highlighted.png"
                        antialiasing: true
                        mipmap: true
                        smooth: true
                        opacity: 1 - image.opacity
                        rotation: image.rotation
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
                        width: column.width
                        height: Screen.height/30
                        hoverEnabled: true
                        onEntered: parent.state = "hovered"
                        onExited: parent.state = "normal"
                        onClicked: {
                            if(polyItem.listOpened == true)
                                polyItem.listOpened = false
                            else
                                polyItem.listOpened = true
                        }
                    }

                    Image {
                        height: Screen.height/60
                        width: height
                        anchors.right: parent.right
                        anchors.verticalCenter: polyName.verticalCenter
                        fillMode: Image.PreserveAspectFit
                        source: "./images/png_images/delete_cross.png"
                        antialiasing: true
                        mipmap: true
                        smooth: true
                        opacity: 1 - image.opacity
                        rotation: image.rotation
                        anchors.rightMargin: polyName.padding/2
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {control.polygonManager.deletePolygon(polyItem.polygon)
//                                appManager.polygonManager.deletePolygon(polyItem.polygon)
                            }
                        }
                    }


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

                                Image {
                                    id: deleteCoordImage
                                    height: Screen.height/60
                                    width: height
                                    anchors.right: parent.right
                                    anchors.verticalCenter: coordsBg.verticalCenter
                                    fillMode: Image.PreserveAspectFit
                                    source: "./images/png_images/delete_cross.png"
                                    antialiasing: true
                                    mipmap: true
                                    smooth: true
                                    opacity: 0
                                    visible: opacity > 0.0 ? true : false
                                    rotation: image.rotation
                                    anchors.rightMargin: polyName.padding/2
                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            if(polyItem.polygon.pointList.length > 3)
                                                polyItem.polygon.removePoint(coordsItem)
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
}
