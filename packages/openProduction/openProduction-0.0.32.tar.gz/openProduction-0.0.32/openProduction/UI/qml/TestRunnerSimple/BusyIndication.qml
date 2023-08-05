import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Controls.Styles 1.4

Item {
    id: busyRoot

    property color secondaryColor: Material.color(Material.Orange);
    property string caption: "Hardware probing"
    property string details: "Drucker abfragen"
    property string errorDetails: "traceback..."
    property int _curIdx: 0

    states: [
        State {
            name: "busy"
            PropertyChanges { target: busy; visible: true}
            PropertyChanges { target: sucIcon; visible: false}
            PropertyChanges { target: errIcon; visible: false}
        },
        State {
            name: "success"
            PropertyChanges { target: busy; visible: false}
            PropertyChanges { target: sucIcon; visible: true}
            PropertyChanges { target: errIcon; visible: false}
        },
        State {
            name: "error"
            PropertyChanges { target: busy; visible: false}
            PropertyChanges { target: sucIcon; visible: false}
            PropertyChanges { target: errIcon; visible: true}
        }
    ]

    onStateChanged: {
        errDetails.visible = false
        if (state === "success")
        {
            sucIcon.animate()
        }
        if (state === "error")
        {
            errIcon.animate()
            errDetails.visible = true
        }
    }

    Pane {
        id: pane
        anchors.fill: parent
        Material.elevation: 6
        Material.background: "white"

        BusyIndicator {
            id: busy
            x:10
            y:10
            width: 64
            height: 64
            Material.accent: busyRoot.secondaryColor
        }

        SuccessIcon {
            id: sucIcon
            x:10
            y:10
            finalRadius: 28
            replayFactor: 2
            circleColor: Material.color(Material.Green)
        }

        ErrorIcon {
            id: errIcon
            x:10
            y:10
            finalRadius: 28
            replayFactor: 2
            circleColor: Material.color(Material.Red)
        }

        Timer {
            interval: 300; running: true; repeat: true
            onTriggered: {
                busyRoot._curIdx = busyRoot._curIdx+1;
                if (busyRoot._curIdx>3)
                    busyRoot._curIdx = 0
            }
        }

        Column {
           y:10
           spacing: 5
           Text {
               function getText() {
                   var txt = busyRoot.caption
                   if (busyRoot.state === "busy")
                   {
                       for (var i=0;i<busyRoot._curIdx%4;i++){
                            txt = txt +"."
                       }
                   }

                   return txt
               }
               id: mainText
               text: getText()
               color:"black"
               font.pointSize: 14
               font.family: "Roboto"
               x:80
               y:10
           }
           Text {
               id: detailedText
               text: busyRoot.details
               font.pointSize: 9
               font.family: "Roboto"
               color: Material.color(Material.Grey, Material.Shade700)
               x:80
               y:20
           }
        }

        MultilineText {
            id: errDetails
            y:80
            anchors.left: parent.left
            anchors.right: parent.right
            height: busyRoot.height -80
            caption: "details"
            text: busyRoot.errorDetails
            styleColor: busyRoot.secondaryColor
            visible: false
        }
    }
}
