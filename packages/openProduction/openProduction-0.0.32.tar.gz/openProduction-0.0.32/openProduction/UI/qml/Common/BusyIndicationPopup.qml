import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Controls.Styles 1.4

Item {
    id: root

    property string overlayColor: "#aacfdbe7"
    property string caption: "Conversion"
    anchors.fill: parent
    z:100
    visible: false

    signal errorOccured;

    function open(productName, productVersion, productRevision) {
        busyIndicationLoader.item.caption = root.caption;
        visible = true;
        overlay.visible = true;
        overlayFadeIn.start();
        popup.open();
    }

    function close(message, details, success) {
        if (success)
        {
            successTimer.start();
            busyIndicationLoader.item.state = "success";
        }
        else
        {
            busyIndicationLoader.item.state = "error";
        }
        if (message !== null)
            busyIndicationLoader.item.caption = message;
        if (details !== null)
            busyIndicationLoader.item.details = details;
    }

    Timer {
        id: successTimer
        interval: 2000
        repeat: false
        running: false
        onTriggered: {
            overlayFadeOut.start();
            popup.close();
        }

    }

    Timer {
        id: errorTimer
        interval: 75
        repeat: false
        running: false
        onTriggered: { errorOccured() }

    }

    function closeByButton() {
        errorTimer.start()
        overlayFadeOut.start();
        popup.close();
    }

    Rectangle {
        id: overlay
        anchors.fill: parent
        color: root.overlayColor
        z: 100
        visible: false

        NumberAnimation {
            id: overlayFadeOut;
            target: overlay;
            property: "opacity";
            from: 1.0;
            to: 0.0;
            duration: 75;
            easing.type: Easing.InOutQuad
        }
        NumberAnimation {
            id: overlayFadeIn;
            target: overlay;
            property: "opacity";
            from: 0.0;
            to: 1.0;
            duration: 150;
            easing.type: Easing.InOutQuad
        }
    }

    Popup {
        id: popup
        padding:0
        width: 560
        height: 182*2
        modal: true
        focus: true
        closePolicy: Popup.NoAutoClose
        property string productName;
        property string productVersion;
        property string productRevision;
        dim: true


        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)

        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 75 }
        }

        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 150 }
        }

        Loader {
            anchors.fill: parent
            id: busyIndicationLoader
            source: "BusyIndication.qml"

            onLoaded: {
                busyIndicationLoader.item.errorBtnPressed.connect(root.closeByButton);
            }
        }

    } /* Popup */

}
