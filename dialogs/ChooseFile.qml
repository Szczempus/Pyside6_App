import QtQuick 2.15
import QtQuick.Dialogs 1.2


FileDialog {
    id: fileDialog

    property var filetypes: filetypes = [ "Image files (*.jpg *.png *.tiff *.tif *.bmp)", "Project files (*.cud)", "All files (*)" ]

    title: "Import file"
    folder: fileDialog.fileUrl

//    currentFolder: fileDialog.fileUrl
    nameFilters: filetypes


}
