import QtQuick 2.15


Item {
    anchors.fill: parent

    Column{
        spacing: 10
        anchors.fill: parent

        CustomToolButtonImage{
            id: firstToll
            anchors.right: parent.right
            width: parent.width
            iconSource: "qrc:/images/svg/polygon"
        }

        CustomToolButtonImage{
            id: secondToll
            anchors.right: parent.right
            width: parent.width
            iconSource: "qrc:/images/svg/import"
        }

        CustomToolButtonImage{
            id: thirdToll
            anchors.right: parent.right
            width: parent.width
            iconSource: "qrc:/images/svg/label"
        }
    }
}
