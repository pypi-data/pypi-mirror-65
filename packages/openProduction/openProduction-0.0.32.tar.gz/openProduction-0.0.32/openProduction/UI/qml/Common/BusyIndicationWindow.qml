import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4

Window {
    id: root
    width: 560
    height: 100//*2
    visible: false


    property string caption: "test";
    color: "#00000000"
    //color: "#00FFFFFF"

    //flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint // Disable window frame
    flags: Qt.ToolTip | Qt.FramelessWindowHint | Qt.WA_TranslucentBackground | Qt.WindowStaysOnTopHint
    modality: Qt.ApplicationModal

    signal errorBtnPressed;

    x: Math.round((Screen.width - width) / 2)
    y: Math.round((Screen.height - height) / 2)

    function setErrorState() {
        busyIndicationLoader.item.state = "error";
        root.height = 182*2
    }

    onVisibilityChanged: {
        if (visible)
        {
            root.height = 100
            busyIndicationLoader.item.state = "busy";
        }
    }

    onCaptionChanged: {
        busyIndicationLoader.item.caption = root.caption;
    }


    Loader {
        anchors.fill: parent
        id: busyIndicationLoader
        source: "BusyIndication.qml"

        onLoaded: {
            busyIndicationLoader.item.errorBtnPressed.connect(root.errorBtnPressed);
            busyIndicationLoader.item.caption = root.caption;
        }
    }

}
