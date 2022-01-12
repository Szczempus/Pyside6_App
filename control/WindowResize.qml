import QtQuick 2.15
import QtGraphicalEffects 1.0

Item {
    anchors.fill: parent

    DropShadow{
        anchors.fill: backgroud
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        samples: 16
        color: "#80000000"
        source:  backgroud
        z: 0
    }

    MouseArea {
        id: leftArea
        anchors{
            left: parent.left
            right: backgroud.left
            top: upperLeftCornerArea.bottom
            bottom: lowerLeftCornerArea.top
            topMargin: 0
            rightMargin: 0
            leftMargin: 0
        }
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: topArea
        anchors{
            left: upperLeftCornerArea.right
            right: upperRightCornerArea.left
            top: parent.top
            bottom: backgroud.top
            rightMargin: 0
            leftMargin: 0
            bottomMargin: 0
            topMargin: 0
        }
        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.TopEdge)}
        }
    }

    MouseArea {
        id: upperLeftCornerArea
        width: 10
        height: 10
        anchors{
            left: parent.left
            top: parent.top
            leftMargin: 0
            topMargin: 0
        }
        cursorShape: Qt.SizeFDiagCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: upperRightCornerArea
        width: 10
        height: 10
        anchors{
            right: parent.right
            top: parent.top
            topMargin: 0
            rightMargin: 0
        }
        cursorShape: Qt.SizeBDiagCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.TopEdge | Qt.RightEdge)}
        }
    }

    MouseArea {
        id: lowerRightCornerArea
        width: 10
        height: 10
        anchors{
            right: parent.right
            bottom: parent.bottom
            bottomMargin: 0
            rightMargin: 0
        }
        cursorShape: Qt.SizeFDiagCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)}
        }
    }

    MouseArea {
        id: lowerLeftCornerArea
        width: 10
        height: 10
        anchors{
            left: parent.left
            bottom: parent.bottom
            leftMargin: 0
            bottomMargin: 0
        }
        cursorShape: Qt.SizeBDiagCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: downArea
        anchors{
            left: lowerLeftCornerArea.right
            right: lowerRightCornerArea.left
            top: backgroud.bottom
            bottom: parent.bottom
            rightMargin: 0
            leftMargin: 0
            bottomMargin: 0
            topMargin: 0
        }
        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.BottomEdge)}
        }
    }

    MouseArea {
        id: rightArea
        anchors{
            left: backgroud.right
            right: parent.right
            top: upperRightCornerArea.bottom
            bottom: lowerRightCornerArea.top
            rightMargin: 0
            leftMargin: 0
            bottomMargin: 0
            topMargin: 0
        }
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active) { window.startSystemResize(Qt.RightEdge)}
        }
    }

}
