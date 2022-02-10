import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12

import "./control" as Control
import "./pages" as Pages
import "./list_models" as Lists
import "./dialogs" as Dialogs
import "./styles" as Styles
import "./content" as Content
import "./GUI" as GUI

//TODO Zablokować możliwośc analizy dopóki nie zostanie wgrana mampa.
//Wówczas if no polygons (analizujemy całą mapę) else (analizujemy dane poligony)
//TODO obsłużyć sygnał o stanie procesu żeby wyskakiwała odpowiedna plansza/znaczek

Window {
    id: window
    width: 1280
    height: 720
    minimumWidth: 640
    minimumHeight: 360
    visible: true
    color: "#ffffffff"
    title: qsTr("Main window")

    property int windowStatus: 0
    property int windowMargin: 10
    property string path: ""

    // Image Container
    Rectangle{
        id: imageContainer
        anchors.fill: parent

        Content.ImageContent{
            id: imageItem

            GUI.PolygonCanvas {
                id: polygonCanvas
                anchors.fill: parent
                polygonManager: appCore.polyMeg
                property string nameToSet: ""
                onPolygonSelected: {
                    if(nameToolActive)
                    {
                        polygon.name = nameToSet
                        menuTop.deactivateTool()
                        polygon.hovered = false
                    }
                }
            }
        }                // Image loading through image provider in choose file dialog
    }

    // Polygons list
    GUI.SlideListPolygon {
        id: polygonList
        topOffset: menuTop.height
        polygonManager: polygonCanvas.polygonManager
    }


    // Menu TopBar Object
    GUI.MenuTop {
        id: menuTop

        property int counter: 0

        projectName: "TEST_name.pro"
        //        toolbarVisible: true // polygon top toolbar

        //        onActionTriggered: console.log(action) // handle actions here
        onActionTriggered: {

            if(action == "action_newProject"){
                newProjectDialog.open()
            }
            else if (action == "action_openProject"){
                console.log("Work in progress...")
                chooseFile.open()
                // Todo: signal openProject -> load project entities to backend
            }
            else if (action == "action_saveProject"){
                console.log("Work in progress...")
            }
            else if (action == "action_importImage"){
                chooseImageFile.open()
            }
            else if (action == "action_runAnalysis"){
                analysis.open()
//                analysis.getString(true, "Papustka")
//                appCore.scriptHandler.runScript()
                // Todo: running python script

            }
            else if (action == "action_createReport"){
                console.log("Work in progress...")
            }
        }

        //onToolSelected: console.log(tool, active) // handle tool (de)selections here
        onToolSelected: {
            if(tool == "tool_drawPolygon")
            {
                if(active == true)
                    messageManager.getString(true, "Polygon " + (++counter).toString())
                else
                    polygonCanvas.endDrawing()
            }
            else if(tool == "tool_namePolygon")
            {
                polygonCanvas.nameToolActive = active
                if(active)
                    messageManager.getString(true, qsTr("New name"))
            }
        }
    }

    // Polygon Massage menager
    GUI.MessageManager {
        id: messageManager
        onStringSet: {
            if(success == true)
            {
                if(polygonCanvas.nameToolActive)
                {
                    polygonCanvas.nameToSet = text
                }
                else
                    polygonCanvas.startDrawing(text)
            }
            else
                menuTop.deactivateTool()
        }
    }

    // New Project Dialog Window
    Dialogs.NewProjectDialog{
        id:newProjectDialog
        width: 300
        height: 440
        x: (window.width - width)/2
        y: (window.height - height)/2
        onAccepted: {
            newProjectDialog.acc()
        }
        onRejected: {
            newProjectDialog.clear()
        }
//        onReset: newProjectDialog.clear()

    }


    // Choose image file dialog window
    Dialogs.ChooseFile{
        id: chooseImageFile
        onAccepted: {
            console.log("Wybrałeś: " + chooseImageFile.fileUrl)
            path = chooseImageFile.fileUrl.toString()
            imageItem.source = "image://opencvImage/" + path
            loading.open()
        }
    }


    // Choose project file dialog
    Dialogs.ChooseFile{
        id: chooseProject
        onAccepted: {
            console.log("Wybrałeś: " + chooseFile.fileUrl)
            path = chooseFile.fileUrl.toString()
        }
    }

    // Map loading popup window
    Dialogs.MapLoadingScreen{
        id:loading
    }

    Dialogs.OverrideConfirmDialog{
        id: override
        onOverride: appCore.prMeg.override_project()
    }

    // Choose analysis popup window
//    Dialogs.AnalysisMessageMenager{
//        id:analysis
//    }

    Dialogs.ChooseAnalysis{
        id:analysis
        polygonManager: polygonCanvas.polygonManager
        onAccepted: {
            appCore.proces.start_analysis(analysis.chosedAnalysis)
        }
    }


    Connections{
        target: appCore.proces

        function onIsProcessing(val){
            if (val === true){
                console.log("Processing true")

            }
            if (val === false){
                console.log("Processing false")
                imageItem.source = ""
                imageItem.source = "image://opencvImage/reload"

            }
        }
    }

    Connections{
         target: appCore.prMeg

         function onFileExists(){
             override.open()
         }
         function onProjectNameChanged (){
             menuTop.toolbarVisible = true
         }
    }

}
