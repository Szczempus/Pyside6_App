import QtQuick 2.15
import QtQuick.Controls 2.15

ListModel{
    ListElement { method: "AI Detectron2"; analyzis: "Segmentation"}
    ListElement { method: "OTSU Method"; analyzis: "Segmentation"}
    ListElement { method: "Voronoi diagram"; analyzis: "Segmentation"}
    ListElement { method: "Fixed-window local maximum"; analyzis: "Segmentation"}
    ListElement { method: "Watershed"; analyzis: "Segmentation"}
    ListElement { method: "Variable-window local maximum"; analyzis: "Segmentation"}
    ListElement { method: "CIR"; analyzis: "Index map"}
    ListElement { method: "NIR"; analyzis: "Index map"}
    ListElement { method: "Mistletoe"; analyzis: "Index map"}
    ListElement { method: "NDVI"; analyzis: "Index map"}
}
