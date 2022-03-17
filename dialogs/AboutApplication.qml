import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0

import "../GUI/Colors.js" as Colors

Popup{

    id: popupAbout
    property real showDuration: 300
    property real hideDuration: 300
    property int popupPolicy: Popup.NoAutoClose

    x: window.width / 2 - width / 2
    y: window.height / 2 - height / 2

    implicitHeight: 500
    implicitWidth: 650
    closePolicy: popupPolicy


    background: Rectangle{
        anchors.fill: parent
        color: Colors.main
        radius: 5
    }

    Image{
       id: baner
       source: "../GUI/images/png_images/Logotypy_do_aplikacji.png"
       width: parent.width
       fillMode: Image.PreserveAspectFit
       antialiasing: true
       mipmap: true
       smooth: true
       anchors.top: parent.top
       anchors.horizontalCenter: parent.horizontalCenter

    }

    Text{
        id: description
        width: parent.width
        text:"<font size=5><b><p>Realizacja projektu nr POPW.01.01.02-18-0023/19
„Oprogramowanie do analizy danych z kamer multispektralnych”<br>
w ramach Programu Operacyjnego Polska Wschodnia 2014-2020</p></b></font>

<font size=4><p>Oś priorytetowa I: Przedsiębiorcza Polska Wschodnia<br>
Działanie 1.1 Platformy startowe dla nowych pomysłów<br>
Poddziałanie 1.1.2 Rozwój startupów w Polsce Wschodniej</p>

<p>Tytuł projektu: Oprogramowanie do analizy danych z kamer multispektralnych</p>

<p>Cel projektu: stworzenie produktu skierowanego do sektorów rolniczego i leśnego
w postaci analitycznego oprogramowania pozwalającego na szczegółową ocenę stanu upraw
oraz drzewostanów, które wykorzystuje do analizy zdjęcia rejestrowane kamerami multispektralnymi
wykonywanymi z powietrza przy pomocy urządzeń bezzałogowych, załogowych oraz satelit.</p>

<p>Planowane efekty: redukcja kosztów i negatywnego wpływu na środowisko poprzez zmniejszenie użycia
pestycydów, herbicydów i nawozów; oszczędność czasu i ułatwienie pracy w sektorze rolnym i leśnym;
maksymalizacja plonów; wsparcie w podejmowaniu decyzji w sektorze rolnym i leśnym;
zapobieganie stratom powodowanym przez patogeny i szkodniki;
wsparcie zarządzania gospodarstwami rolnymi i działami leśnymi;
lepsze zrozumienie procesów naturalnych zachodzących na obszarze gospodarstw rolnych i lasów.</p>

<p>Wartość projektu: całkowita wartość projektu wynosi 1 287 350, 00 zł<br>
Wkład Funduszu Europejskiego: 997 475,00 zł </p><font>"

        color: Colors.highlighted_text
        wrapMode: Text.Wrap
        textFormat: Text.RichText
        anchors{
            top: baner.bottom
            topMargin: 10
        }
//        font{
//            bold: true
//            family: Colors.font
//            pixelSize: 8
//        }
    }




    Button{
        id: closePopupAbout
        contentItem: Text{
            text: "Close"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
            color: Colors.highlighted_text
            anchors{
                bottom: parent.bottom
                horizontalCenter: parent.horizontalCenter
                verticalCenter: parent.verticalCenter
            }
            font{
                family: "Ubuntu"
                pixelSize: 14
                bold: true
            }
        }
        width: parent.width
        height: 20
        background: Rectangle{
            color: Colors.highlighted_main
            radius: 5
        }
        hoverEnabled: false

        anchors{
            bottom: parent.bottom
            right: parent.right
            topMargin: 10
            leftMargin: 10
            bottomMargin: 10
        }

        onClicked: {
            popupAbout.close()
        }
    }


}


