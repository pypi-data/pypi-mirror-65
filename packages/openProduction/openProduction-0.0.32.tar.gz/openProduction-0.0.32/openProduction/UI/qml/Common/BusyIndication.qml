import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3

Item {
    id: busyRoot

    property color secondaryColor: Material.color(Material.Orange);
    property string caption: "Conversion"
    property string details: ""
    property string errorDetails: "traceback..."

    signal errorBtnPressed;

    QtObject {
        id: internal
        property int _curIdx: 0
    }

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

    function onNewLogMessage(message, level) {
        busyRoot.details = message
    }

    Component.onCompleted: {
        logger.newLogMessage.connect(onNewLogMessage)
        logger.resetLog()
        busyRoot.state = "busy";
    }

    Component.onDestruction: {
        logger.newLogMessage.disconnect(onNewLogMessage)
    }

    onStateChanged: {
        //errDetails.visible = false
        if (state === "success")
        {
            sucIcon.animate()
        }
        if (state === "error")
        {
            errIcon.animate()
            errDetails.visible = true
            okButton.visible = true
            errorDetails = logger.getErrorLog()
            logger.newLogMessage.disconnect(onNewLogMessage)
        }
    }

    Pane {
        id: pane
        anchors.fill: parent
        Material.elevation: 6
        Material.background: "white"
        padding: 0

        ColumnLayout {
            x:0
            y:0
            width:parent.width
            height: parent.height
            Layout.maximumWidth: parent.width
            Layout.maximumHeight: parent.height
            spacing: 0

            Rectangle {
                id: header
                Layout.fillWidth: true
                Layout.minimumHeight: 64//+20+28
                Layout.maximumHeight: 64//+20+28
                Layout.leftMargin: 24
                Layout.rightMargin: 32
                Layout.topMargin: 20
                Layout.bottomMargin: 14
                color: "transparent"

                RowLayout{
                    /* header */
                    Layout.minimumHeight: 64
                    Layout.maximumHeight: 64
                    spacing: 0
                    Layout.minimumWidth: header.width
                    Layout.maximumWidth: header.width

                    Rectangle {
                        /* icon placeholder */
                        Layout.minimumWidth: 64
                        Layout.maximumWidth: 64
                        Layout.minimumHeight: 64
                        Layout.maximumHeight: 64
                        BusyIndicator {
                            id: busy
                            anchors.fill: parent
                            Material.accent: busyRoot.secondaryColor
                        }
                        SuccessIcon {
                            id: sucIcon
                            finalRadius: 28
                            replayFactor: 2
                            anchors.fill: parent
                            circleColor: Material.color(Material.Green)
                        }
                        ErrorIcon {
                            id: errIcon
                            finalRadius: 28
                            replayFactor: 2
                            anchors.fill: parent
                            circleColor: Material.color(Material.Red)
                        }
                    } /* Icon placeholder */

                    ColumnLayout {
                        Layout.leftMargin: 8
                        spacing: 0
                        Text {
                            Layout.minimumHeight: 20
                            Layout.maximumHeight: 20
                            Layout.maximumWidth: header.width - 64-8
                            id: mainText
                            text: ""
                            font.pixelSize: 20
                            color: "#de000000"
                            font.family: "roboto"
                            font.bold: true
                            elide: Text.ElideRight
                            maximumLineCount: 1
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.minimumHeight: 20
                            Layout.maximumHeight: 20
                            color: "transparent"
                        }

                        Text {
                            Layout.fillHeight: true
                            Layout.maximumWidth: header.width - 64-8
                            id: detailedText
                            text: busyRoot.details
                            font.pixelSize: 16
                            color: "#99000000"
                            font.family: "roboto"
                            elide: Text.ElideRight
                            verticalAlignment: Text.AlignTop
                            maximumLineCount: 1
                        }

                    } /* ColumnLayout of heading and details label */
                } /* inner RowLayout of first line */

            }/* row with indicator and main labels */

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 100
                Layout.fillHeight: true
                Layout.leftMargin: 24
                Layout.rightMargin: 32
                Layout.bottomMargin: 14
                color: "transparent"

                MultilineText {
                    id: errDetails
                    caption: "details"
                    text: errorDetails
                    styleColor: busyRoot.secondaryColor
                    visible: false
                    anchors.fill: parent
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 52
                Layout.maximumHeight: 52
                //Layout.fillHeight: false
                Layout.leftMargin: 24
                Layout.rightMargin: 8
                Layout.topMargin: 0
                color: "transparent"

                RowLayout {
                    spacing:0
                    Layout.margins: 0
                    anchors.fill: parent
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "transparent"
                    }
                    Button {
                        id: okButton
                        text: qsTr("fortfahren")
                        Material.foreground: busyRoot.secondaryColor
                        flat: true
                        onClicked: {
                            busyRoot.errorBtnPressed();
                        }
                        visible: false
                    }
                }
            }
        } /* top ColumnLayout */

    } /* Pane */

    Timer {
        id: busyTxtTimer
        interval: 300; running: true; repeat: true
        onTriggered: {
            internal._curIdx = internal._curIdx+1;
            if (internal._curIdx>3)
                internal._curIdx = 0;

            var txt = busyRoot.caption
            if (busyRoot.state === "busy")
            {
                for (var i=0;i<internal._curIdx%4;i++){
                     txt = txt +"."
                }
            }
            mainText.text = txt;
        }
    }
}
