import QtQuick 2.15
//import QtQuick.Dialogs 1.2
import Qt.labs.platform 1.1

FileDialog {
    id: saveFileDialog

    property var filetypes: filetypes = [" CSV File (*.csv)"]

    title: "Save Dialog"
    folder: saveFileDialog.fileUrl

//    currentFolder: fileDialog.fileUrl
    nameFilters: filetypes
    fileMode: FileDialog.SaveFile
    acceptLabel: "Zapisz"
}
