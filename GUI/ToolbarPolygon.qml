import QtQuick 2.12
import QtQuick.Window 2.12
import "Colors.js" as Colors

Item {
    id: control

    implicitHeight: parent.height
    implicitWidth: parent.width - Screen.height*6/20

    anchors.horizontalCenter: parent.horizontalCenter

    width: row.implicitWidth
    height: implicitHeight

    signal actionTriggered(string action)
    signal toolSelected(string tool, bool active)

    property var lastActiveTool: undefined

    onVisibleChanged: lastActiveTool = undefined

    function deactivateLastTool() {
        lastActiveTool.active = false
        control.toolSelected(lastActiveTool.tool, false)
        lastActiveTool = undefined
    }

    Row {
        id: row
        height: parent.height
        width: parent.width
        spacing: 0

        ButtonTool {
            icon_source: "qrc:/images/png/polygon"
            icon_source_highlighted: "qrc:/images/png/polygon_highlighted"
            tool: "tool_drawPolygon"
            text: qsTr("DRAW")
            visible: visibility
            onClicked: {
                if(isAction)
                {
                    control.actionTriggered(tool)
                }
                else
                {
                    if(active)
                    {
                        if(lastActiveTool != undefined)
                        {
                            lastActiveTool.active = false
                            control.toolSelected(lastActiveTool.tool, false)
                        }
                        lastActiveTool = this
                    }
                    else
                    {
                        lastActiveTool = undefined
                    }
                    control.toolSelected(tool, active)
                }
            }
        }
        ButtonTool {
            icon_source: "qrc:/images/png/nametag"
            icon_source_highlighted: "qrc:/images/png/nametag_highlighted"
            tool: "tool_namePolygon"
            text: qsTr("NAME")
            visible: visibility
            onClicked: {
                if(isAction)
                {
                    control.actionTriggered(tool)
                }
                else
                {
                    if(active)
                    {
                        if(lastActiveTool != undefined)
                        {
                            lastActiveTool.active = false
                            control.toolSelected(lastActiveTool.tool, false)
                        }
                        lastActiveTool = this
                    }
                    else
                    {
                        lastActiveTool = undefined
                    }
                    control.toolSelected(tool, active)
                }
            }
        }
        Separator {
            separation: "row"
        }
        ButtonTool {
            icon_source: "qrc:/images/png/load"
            icon_source_highlighted: "qrc:/images/png/load_highlighted"
            tool: "action_loadPolygon"
            text: qsTr("LOAD")
            isAction: true
            onClicked: {
                if(isAction)
                {
                    control.actionTriggered(tool)
                }
                else
                {
                    if(active)
                    {
                        if(lastActiveTool != undefined)
                        {
                            lastActiveTool.active = false
                            control.toolSelected(lastActiveTool.tool, false)
                        }
                        lastActiveTool = this
                    }
                    else
                    {
                        lastActiveTool = undefined
                    }
                    control.toolSelected(tool, active)
                }
            }
        }
        ButtonTool {
            icon_source: "qrc:/images/png/save"
            icon_source_highlighted: "qrc:/images/png/save_highlighted"
            tool: "action_savePolygon"
            text: qsTr("SAVE")
            visible: visibility
            isAction: true
            onClicked: {
                if(isAction)
                {
                    control.actionTriggered(tool)
                }
                else
                {
                    if(active)
                    {
                        if(lastActiveTool != undefined)
                        {
                            lastActiveTool.active = false
                            control.toolSelected(lastActiveTool.tool, false)
                        }
                        lastActiveTool = this
                    }
                    else
                    {
                        lastActiveTool = undefined
                    }
                    control.toolSelected(tool, active)
                }
            }
        }
    }

}
