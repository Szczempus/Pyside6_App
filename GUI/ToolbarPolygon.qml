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
            icon_source: "./images/png_images/slider.png"
            icon_source_highlighted: "./images/png_images/slider_highlighted.png"
            tool: "slider"
            text: qsTr("PARAMETERS")
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
            icon_source: "./images/png_images/polygon.png"
            icon_source_highlighted: "./images/png_images/polygon_highlighted.png"
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
            icon_source: "./images/png_images/nametag.png"
            icon_source_highlighted: "./images/png_images/nametag_highlighted.png"
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
            icon_source: "./images/png_images/load.png"
            icon_source_highlighted: "./images/png_images/load_highlighted.png"
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
            icon_source: "./images/png_images/save.png"
            icon_source_highlighted: "./images/png_images/save_highlighted.png"
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
