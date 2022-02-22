import QtQuick 2.15
//import "../control/" as Control
import "../GUI" as GUI

Image{

    id: imageItem

    property bool drawPolygon: false
    property real polygonCounter: 0

    function singleClick(){
        // On clicked event handle the mouse X and Y position on the image
        //        console.log("Mouse X:", mouse_area.mouseX, " Mouse Y:", mouse_area.mouseY)
        //        pointList.append({"Px":mouse_area.mouseX, "Py":mouse_area.mouseY }) // Append listModel with x, y coords
        polygonList.get(polygonCounter).polygon.append({"Px":mouse_area.mouseX, "Py":mouse_area.mouseY})
        console.log(polygonList.get(polygonCounter).polygon.get(polygonList.get(polygonCounter).polygon.count-1).Px)

    }

    fillMode: Image.PreserveAspectFit
    asynchronous: true
    onStatusChanged: if(imageItem.status == Image.Ready | Image.Error) {
                         loading.close()
                     }

    // Scaling image by pinch area variables
    transform: Scale{
        id: imageScaler
        origin.x: pinchArea.m_x2
        origin.y: pinchArea.m_y2
        xScale: pinchArea.m_zoom2
        yScale: pinchArea.m_zoom2

    }

    sourceSize: {
        width: parent.width
        height: parent.height
    }

    // Handling image scalig by pinch on touch screen
    PinchArea {
        id: pinchArea
        anchors.fill:parent
        property real m_x1: 0
        property real m_y1: 0
        property real m_y2: 0
        property real m_x2: 0
        property real m_zoom1: 0.1
        property real m_zoom2: 0.1
        property real m_max: 4
        property real m_min: 0.01

        onPinchStarted: {
            m_x1 = imageScaler.origin.x
            m_y1 = imageScaler.origin.y
            m_x2 = pinch.startCenter.x
            m_y2 = pinch.startCenter.y
            imageItem.x = imageItem.x + (pinchArea.m_x1 - pinchArea.m_x2)*(1-pinchArea.m_zoom1)
            imageItem.y = imageItem.y + (pinchArea.m_y1 - pinchArea.m_y2)*(1-pinchArea.m_zoom1)

        }

        onPinchUpdated: {
            m_zoom1 = imageScaler.xScale
            var dz = pinch.scale - pinch.previousScale
            var newZoom = m_zoom1+dz
            if (newZoom <= m_max && newZoom >= m_min){
                m_zoom2 = newZoom
            }
        }


//        GUI.ParameterSliders{
//            id: slidersWindow
//        }



        // Placing mouse area on the top of the image
        MouseArea{
            id: mouse_area

            anchors.fill: parent
            hoverEnabled: true

            // Enabling draging the image
            drag {
                target: imageItem
                axis: Drag.XandYAxis
                filterChildren: true
            }

            //Threshold for single click
            Timer{
                id: mouseTimer
                interval: 200
                onTriggered: singleClick()
            }

            // Handling image scaling by mouse wheel scrolling
            onWheel: {

                pinchArea.m_x1 = imageScaler.origin.x
                pinchArea.m_y1 = imageScaler.origin.y
                pinchArea.m_zoom1 = imageScaler.xScale

                pinchArea.m_x2 = mouseX
                pinchArea.m_y2 = mouseY

                var newZoom
                if (wheel.angleDelta.y > 0){
                    newZoom = pinchArea.m_zoom1 + 0.01
                    if (newZoom <= pinchArea.m_max){
                        pinchArea.m_zoom2 = newZoom
                    }else{
                        pinchArea.m_zoom2 = pinchArea.m_max
                    }
                }else{
                    newZoom = pinchArea.m_zoom1 - 0.01
                    if(newZoom >= pinchArea.m_min){
                        pinchArea.m_zoom2 = newZoom
                    }else{
                        pinchArea.m_zoom2 = pinchArea.m_min
                    }
                }
                imageItem.x = imageItem.x + (pinchArea.m_x1 - pinchArea.m_x2) * (1-pinchArea.m_zoom1)
                imageItem.y = imageItem.y + (pinchArea.m_y1 - pinchArea.m_y2) * (1-pinchArea.m_zoom1)

            }

            onClicked: {
                if(mouse.button == Qt.LeftButton){
                    if(mouseTimer.running)
                    {
                        mouseTimer.stop()
                    }
                    else{
                        mouseTimer.restart()
                    }
                }
            }
        }
    }
}                // Image loading through image provider in choose file dialog
