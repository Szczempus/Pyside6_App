import QtQuick 2.15
import QtQuick.Controls 2.12

Item {
    id: control

    property var polygonManager: undefined

    property var polygon: undefined

    property bool nameToolActive: false

    property bool result: false

    Connections{
        target: appCore.polyMeg
        function onNewPolygonCreated(poly){
            polygon = poly
        }
    }

    Connections{
        target: polygon
        function onAddPointResult(res){
            result = res
        }
    }


    function startDrawing(polygonName) {
//        console.log("Nowy Poligon QML") //Działa
        control.polygonManager.startNewPolygon(polygonName);
        canvasArea.enabled = true
    }

    function endDrawing() {
        if(polygon != undefined)
        {
            if(polygon.pointList.length > 2)
            {
                polygon.finished = true
            }
            else
            {
                control.polygonManager.deletePolygon(polygon)
            }
            polygon = undefined
            control.polygonManager.polygonListChanged()
        }
        canvasArea.enabled = false
    }

    signal polygonSelected(var polygon)

    Repeater {
        model: control.polygonManager.polygonList

        delegate: Canvas {
            id: poliDraw
            anchors.fill: parent
            property var polygon: modelData
            property bool finished: polygon.finished
            property bool hovered: polygon.hovered
            property var list: polygon.pointList
            property var polygonPredictions: undefined
            onPolygonChanged: requestPaint()
            onFinishedChanged: requestPaint()
            onHoveredChanged: requestPaint()
            onListChanged: requestPaint()
            renderStrategy: Canvas.Threaded
            renderTarget: Canvas.FramebufferObject

            Connections{
                target: appCore.proces

                 function onIsProcessing(val, status){
                     if (val === false){
                         console.log("Processing false")
                         if (status === "Success"){

//                             console.log("Poligonu analiza: ", polygon.polygonAnalysis)
//                             poliDraw.polygonPredictions = polygon.polygonAnalysis.predictionsList
//                             predictionsRepeater.model = poliDraw.polygonPredictions
                         }
                      }
                }
            }

            onPaint: {

                console.log("Polygony predykcji: ", polygonPredictions)
                var context = getContext("2d");
                context.reset()

                if(finished === true)
                {

                    context.lineWidth = 1
                    context.setLineDash([2000,1])

                    if(hovered)
                        context.strokeStyle = "#FF0000"
                    else
                        context.strokeStyle = "#C00000"
                    context.beginPath()
                    context.moveTo(polygon.pointList[0].x, polygon.pointList[0].y)
                    for(var j=1; j<polygon.pointList.length; j++)
                    {
                        context.lineTo(polygon.pointList[j].x, polygon.pointList[j].y)
                    }
                    context.closePath()
                    context.stroke()
                    if(hovered)
                        context.fillStyle = "#3000FF55"
                    else
                        context.fillStyle = "#300000DD"
                    context.fill();
                }
                else
                {
                    if(polygon.pointList.length > 0)
                    {
                        context.lineWidth = 1
                        context.setLineDash([2000,1])

                        if(hovered)
                            context.strokeStyle = "#FF0000"
                        else
                            context.strokeStyle = "#C00000"
                        context.beginPath()
                        context.moveTo(polygon.pointList[0].x, polygon.pointList[0].y)
                        for(var k=1; k<polygon.pointList.length; k++)
                        {
                            context.lineTo(polygon.pointList[k].x, polygon.pointList[k].y)
                        }
                        context.stroke()
                        context.setLineDash([2,3])
                        context.closePath()
                        context.stroke()
                    }
                }
            }

            Item {
                x: polygon.polygonCenter.x
                y: polygon.polygonCenter.y
                width: 1
                height: 1
                clip: false
                Text {
                    text: polygon.name
                    anchors.centerIn: parent
                    color: "magenta"
                    font.bold: true
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    visible: hovered
                }

            }

                Repeater{
                    id: predictionsRepeater
                    model: poliDraw.polygonPredictions

                    Component.onCompleted: console.log("predictionsRepeater created")

                    delegate: Canvas{
                        id: predictions

                        property var predictionPolygon: modelData

                        anchors.fill: parent


                        onPredictionPolygonChanged: {
                            console.log("Paint requested")
                            predictions.requestPaint()
                        }

                        renderStrategy: Canvas.Threaded
                        renderTarget: Canvas.FramebufferObject

                        onPaint: {
                            var context = getContext("2d");
                            context.reset()

                            if(predictionPolygon.finished === true)
                            {

                                context.lineWidth = 1

                                if(predictionPolygon.hovered)
                                    context.strokeStyle = "#ff7373"
                                else
                                    context.strokeStyle = "#f00"
            //                    context.beginPath()

                                console.log("Poligon: ",predictionPolygon)
                                console.log("Poligon list: ",predictionPolygon.pointList)
                                console.log("Poligon points: ",predictionPolygon.pointList[0].x,predictionPolygon.pointList[0].y,
                                            predictionPolygon.pointList[1].x,predictionPolygon.pointList[1].y,
                                            predictionPolygon.pointList[2].x,predictionPolygon.pointList[2].y,
                                            predictionPolygon.pointList[3].x,predictionPolygon.pointList[3].y,)

                                context.rect(predictionPolygon.pointList[0].x,predictionPolygon.pointList[0].y, 50, 50)

                                context.strokeRect(predictionPolygon.pointList[0].x,predictionPolygon.pointList[0].y, 50, 50)
                                if(predictionPolygon.hovered)
                                    context.fillStyle = "#3000FF55"
                                else
                                    context.fillStyle = "#300000DD"
                                context.fill();
                            }
                        }
                    }
                }

            Repeater {
                model: list

                delegate: Image {
                    source: parent.hovered || coordHovered ? "./images/png_images/pin_hovered.png" : "./images/png_images/pin.png"
                    width: 14
                    height: 17
                    fillMode: Image.PreserveAspectFit
                    x: modelData.x - width/2 + 1
                    y: modelData.y - height
                    mipmap: true
                    antialiasing: true
                    smooth: true

                    property bool coordHovered: modelData.hovered
                }
            }


        }
    }

    MouseArea {
        id: canvasArea
        anchors.fill: parent
        hoverEnabled: control.nameToolActive
        onHoverEnabledChanged: enabled = hoverEnabled
        enabled: false

        property var poly: undefined
        property var previousPoly: undefined

        onPolyChanged: {
            if(previousPoly != undefined)
                previousPoly.hovered = false
            previousPoly = poly
            if(poly != undefined)
                poly.hovered = true
        }

        onClicked: {
            if(control.polygon != undefined)
            {
                control.polygon.addPoint(mouseX, mouseY)

                if(control.result === true)
                {
                    control.polygonManager.polygonListChanged()
                    control.polygon.pointListChanged()
                }
            }
            else if(hoverEnabled && poly != undefined)
            {
                control.polygonSelected(poly)
            }
        }
        onMouseXChanged: {
            if(hoverEnabled)
            {
                var foundPoly = control.polygonManager.isPolygonHovered(mouseX, mouseY)
                if(foundPoly !== null)
                    poly = foundPoly
                else
                    poly = undefined
            }
        }
        onMouseYChanged: {
            if(hoverEnabled)
            {
                var foundPoly = control.polygonManager.isPolygonHovered(mouseX, mouseY)
                if(foundPoly !== null)
                    poly = foundPoly
                else
                    poly = undefined
            }
        }

    }

}
