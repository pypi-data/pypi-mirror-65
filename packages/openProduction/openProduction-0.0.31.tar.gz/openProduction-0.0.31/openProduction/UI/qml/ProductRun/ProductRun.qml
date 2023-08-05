import QtQuick.Controls 1.4
import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import QtCharts 2.3
import "../Common"

Item {
    id: root
    anchors.fill: parent

    property string primaryColor: Material.Red
    property string secondaryColor: Material.Green
    property string backgroundColor: Material.color(Material.Grey,
                                                    Material.Shade50)

    property QtObject testSuite: null

    property var locale: Qt.locale()

    QtObject {
        id: internal
        property int _curIdx: 0
    }

    onTestSuiteChanged: {
        if (testSuite !== null) {
            testSuite.setStepType("regular")
            testSuite.sequenceComplete.connect(onSequenceComplete)
            testSuite.sequenceStart.connect(onSequenceStart)
            testSuite.stepStart.connect(onStepStart)
            testSuite.stepComplete.connect(onStepComplete)
            testSuite.deviceIDSet.connect(onDeviceID)
            tempParamsViewer.model = testSuite.getTempParams()
            var iohandler = station.getIOHandler()
            iohandler.newImageDataGUI.connect(onNewImageData)
            iohandler.newMessage.connect(onNewMessage)
            iohandler.newPlot.connect(onNewPlot)
        }
    }

    property alias plotResultItem: plotResultsLoader.item
    property int num: 0

    Component {
        id: imgDisplayComponent
        Image {
            id: myImg
            anchors.fill: parent
            property alias image: myImg.source
            property bool busy: false

            onSourceChanged: {
                busy = false
            }
        }
    }

    Component {
        id: plotComponent

        ChartView {
            id: myPlot
            title: ""
            titleFont.family: "roboto"
            titleFont.pointSize: 12
            legend.font.family: "roboto"
            legend.font.pointSize: 10
            anchors.fill: parent
            antialiasing: false
            legend.visible: false
            /*
            margins.top: 0
            margins.bottom: 0
            margins.left: 0
            margins.right: 0
            */


            MouseArea {
                id: selectArea;
                anchors.fill: parent;
                property int xStart;
                property int yStart;
                acceptedButtons: Qt.LeftButton | Qt.RightButton

                onClicked: {
                    if(mouse.button & Qt.RightButton)
                        myPlot.zoomReset();
                }

                onPressed: {
                    if(mouse.button & Qt.RightButton)
                        return

                    if (highlightItem !== null) {
                        // if there is already a selection, delete it
                        highlightItem.destroy ();
                    }

                    xStart = mouse.x;
                    yStart = mouse.y;
                    // create a new rectangle at the wanted position
                    highlightItem = highlightComponent.createObject (selectArea, {
                        "x" : mouse.x, "y": mouse.y
                    });
                    // here you can add you zooming stuff if you want
                }
                onPositionChanged: {
                    // on move, update the width of rectangle
                    highlightItem.width = (Math.abs (mouse.x - xStart));
                    highlightItem.height = (Math.abs (mouse.y - yStart));

                    if (mouse.x < xStart)
                        highlightItem.x = mouse.x;
                    if (mouse.y < yStart)
                        highlightItem.y = mouse.y;

                }
                onReleased: {
                    // here you can add you zooming stuff if you want
                    var r = Qt.rect(highlightItem.x, highlightItem.y, highlightItem.width, highlightItem.height)
                    myPlot.zoomIn(r)
                    highlightItem.destroy ();
                }

                onDoubleClicked: myPlot.zoomReset();

                property Rectangle highlightItem : null;

                Component {
                    id: highlightComponent;

                    Rectangle {
                        color: "blue";
                        opacity: 0.35;
                    }
                }
            }

            /*
            MouseArea{
                anchors.fill: parent
                onDoubleClicked: myPlot.zoomReset();
            }


            PinchArea{
                id: pa
                anchors.fill: parent
                onPinchUpdated: {
                    myPlot.zoomReset();
                    var center_x = pinch.center.x
                    var center_y = pinch.center.y
                    var width_zoom = height/pinch.scale;
                    var height_zoom = width/pinch.scale;
                    var r = Qt.rect(center_x-width_zoom/2, center_y - height_zoom/2, width_zoom, height_zoom)
                    myPlot.zoomIn(r)
                }

            }
            */

            ScatterSeries  {
                markerSize: 5
                //useOpenGL: true
                axisX: ValueAxis {
                    min: 0
                    max: 10000
                    titleText: "x-axis"
                }
                axisY: ValueAxis {
                    min: 0
                    max: 1
                    titleText: "y-axis"
                }
                XYPoint { x: 0; y: 10 }
                XYPoint { x: 1; y: 10.1 }
                XYPoint { x: 2; y: 10.2 }
                XYPoint { x: 3; y: 10.0 }
                XYPoint { x: 4; y: 10.3 }
                XYPoint { x: 5; y: 15 }
                XYPoint { x: 6; y: 10.1 }

            }
        }

    }

    Component {
        id: txtDisplayComponent
        Text {
            id: myTxt
            anchors.fill: parent
            text: ""
            font.family: "Concert One"
            font.weight: Font.Light
            font.pointSize: 16
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    function onNewPlot() {

        plotResults.Layout.minimumHeight = 400;
        plotResultsLoader.sourceComponent = plotComponent;

        /*
        var myAxisX = plotResultsLoader.item.series(0).axisX;
        var myAxisY = plotResultsLoader.item.series(0).axisY;

        plotResultsLoader.item.series(0).name = label;

        Array.prototype.max = function() {
          return Math.max.apply(null, this);
        };

        Array.prototype.min = function() {
          return Math.min.apply(null, this);
        };

        if (title !== "")
            plotResultsLoader.item.title = title;
        if (xlabel !== "")
            myAxisX.titleText = xlabel;
        if (ylabel !== "")
            myAxisY.titleText = ylabel;

        myAxisY.min = ydata.min();
        myAxisY.max = ydata.max();
        myAxisX.min = xdata.min();
        myAxisX.max = xdata.max();
        */

        ioHandler.plotDataUpdate(plotResultsLoader.item.series(0));
    }

    function onNewMessage(msg) {
        plotResultsLoader.sourceComponent = txtDisplayComponent
        plotResultsLoader.item.text = msg
    }

    function onNewImageData() {
        num = num + 1
        plotResultsLoader.sourceComponent = imgDisplayComponent
        if (plotResultItem.busy === true)
            return
        else
            plotResultItem.busy = true
        plotResultItem.image = "image://myprovider/ioHandler" + num
    }

    function onStepStart(caseName, idx, numCases) {
        var myIdx = idx + 1
        curResult.text = curResult.text + caseName + "(" + myIdx + " von " + numCases + "): ... "
    }

    function onStepComplete(state, result, msg, fullName, idx, numCases) {
        var resStr
        if (result === 2)
            resStr = "Exception"
        else if (result === 1)
            resStr = "Failure"
        else if (result === 0)
            resStr = "Ok"
        else if (result === 4)
            resStr = "Skip"
        else if (result === 3)
            resStr = "Abort"
        else
            resStr = "UNKNOWN"

        curResult.text = curResult.text + resStr + "\n"
    }

    function onDeviceID(deviceID) {
        resultDevID.text = deviceID
    }

    function onSequenceStart() {
        var now = new Date()

        manualStart.text = qsTr("Abbrechen")
        sucIcon.visible = false
        errIcon.visible = false
        busy.visible = true
        resultCaption.text = qsTr("Busy")
        resultDevID.text = qsTr("Unbekanntes Gerät")
        txtStart.text = qsTr("Start: " + now.toLocaleTimeString(Qt.locale(),
                                                                "hh:mm:ss"))
        curResult.text = ""
    }

    function onSequenceComplete(suiteState, success, duration, suiteResultStr) {
        txtCancel.visible = false
        manualStart.text = qsTr("manueller Start")
        txtDuration.text = qsTr("Dauer: " + Number.parseFloat(duration).toFixed(
                                    2) + " s")
        var resultStr
        if (success) {
            playSound.playSuccess()
            sucIcon.visible = true
            errIcon.visible = false
            sucIcon.animate()
            busy.visible = false
            resultCaption.text = qsTr("Pass")
            resultStr = 'OK'
        } else {
            playSound.playError()
            sucIcon.visible = false
            errIcon.visible = true
            errIcon.animate()
            busy.visible = false
            resultCaption.text = qsTr("Fail")
            resultStr = 'FAIL'
        }

        curResult.text = curResult.text + "\n" + suiteResultStr
    }

    Popup {
        width: 400
        height: 200
        anchors.centerIn: parent
        id: ioHandlerPopUp
        objectName: "ioHandlerPopUp"
        property string title: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        property string supportText: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        property string btnRetryTxt: "Wiederholen"
        property string btnCancelTxt: "Abbrechen"
        property string btnOkayTxt: "Bestätigen"
        property bool btnRetryVisible: false
        padding: 0

        signal okButtonPressed
        signal retryButtonPressed
        signal cancelButtonPressed

        Shortcut {
            id: enterShortCut
            enabled: false
            sequence: "Return"
            onActivated: {
                ioHandlerPopUp.okButtonPressed()
                ioHandlerPopUp.close()
            }
        }

        onClosed: {
            enterShortCut.enabled = false
        }

        onVisibleChanged: {
            if (visible === true)
                enterShortCut.enabled = true
        }

        closePolicy: Popup.NoAutoClose
        ColumnLayout {
            anchors.fill: parent
            Rectangle {
                Layout.leftMargin: 24
                Layout.rightMargin: 24
                Layout.topMargin: 24
                Layout.minimumHeight: 24
                Layout.fillWidth: true
                //Layout.maximumWidth: parent.width - 24 -24
                color: "transparent"
                Text {
                    id: title
                    font.pixelSize: 20
                    font.bold: true
                    font.family: "Roboto"
                    text: ioHandlerPopUp.title
                    elide: Text.ElideRight
                    maximumLineCount: 1
                    anchors.fill: parent
                }
            }
            Rectangle {
                Layout.minimumHeight: 16 * 4
                Layout.leftMargin: 24
                Layout.rightMargin: 24
                Layout.topMargin: 20
                Layout.fillWidth: true
                color: "transparent"
                Text {
                    id: supportText
                    font.pixelSize: 16
                    font.family: "Roboto"
                    text: ioHandlerPopUp.supportText
                    elide: Text.ElideRight
                    wrapMode: Text.WordWrap
                    maximumLineCount: 3
                    anchors.fill: parent
                }
            }
            Rectangle {
                Layout.fillHeight: true
                Layout.minimumWidth: 80
                color: "transparent"
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 24 * 2
                color: "transparent"
                RowLayout {
                    anchors.fill: parent
                    spacing: 8
                    Rectangle {
                        Layout.fillWidth: true
                        color: "transparent"
                    }

                    Button {
                        Layout.leftMargin: 8
                        Layout.rightMargin: 8
                        Layout.bottomMargin: 8
                        Visible: ioHandlerPopUp.btnRetryVisible
                        text: ioHandlerPopUp.btnRetryTxt
                        Material.elevation: 0
                        highlighted: false
                        Material.foreground: Material.color(root.primaryColor)
                        onClicked: {
                            ioHandlerPopUp.retryButtonPressed()
                            ioHandlerPopUp.close()
                        }
                    }
                    Button {
                        Layout.leftMargin: 8
                        Layout.bottomMargin: 8
                        text: ioHandlerPopUp.btnCancelTxt
                        Material.elevation: 0
                        highlighted: false
                        Material.foreground: Material.color(root.primaryColor)
                        onClicked: {
                            ioHandlerPopUp.cancelButtonPressed()
                            ioHandlerPopUp.close()
                        }
                    }
                    Button {
                        Layout.leftMargin: 8
                        Layout.rightMargin: 8
                        Layout.bottomMargin: 8
                        text: ioHandlerPopUp.btnOkayTxt
                        Material.elevation: 0
                        highlighted: false
                        Material.foreground: Material.color(root.primaryColor)
                        onClicked: {
                            ioHandlerPopUp.okButtonPressed()
                            ioHandlerPopUp.close()
                        }
                    }
                }
            }
        }
    }

    ColumnLayout {
        id: col
        anchors.fill: parent
        spacing: 16

        RowLayout {
            Layout.minimumWidth: col.width
            Layout.maximumWidth: col.width
            spacing: 16
            Pane {
                id: equippedDevice
                Material.elevation: 6
                Layout.minimumWidth: 200
                Layout.minimumHeight: 200
            }

            Pane {
                id: plotResults
                Material.elevation: 6
                Layout.fillWidth: true
                //Layout.minimumWidth: 400
                Layout.minimumHeight: 200
                Layout.maximumHeight: 400
                Loader {
                    objectName: "plotResultsLoader"
                    id: plotResultsLoader
                    anchors.fill: parent
                }
            }

            Pane {
                id: runResults
                Material.elevation: 6
                Layout.minimumWidth: 344
                Layout.maximumWidth: 344
                Layout.minimumHeight: 200
                Layout.maximumHeight: 200
                padding: 0

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0
                    Layout.margins: 0

                    RowLayout {
                        Layout.leftMargin: 16
                        Layout.rightMargin: 32
                        Layout.topMargin: 24
                        Layout.bottomMargin: 8
                        spacing: 16
                        Layout.minimumWidth: 344 - 80 - 32 - 16
                        Layout.maximumWidth: 344 - 80 - 32 - 16

                        ColumnLayout {

                            Layout.minimumWidth: 344 - 80 - 32 - 16
                            Layout.maximumWidth: 344 - 80 - 32 - 16
                            spacing: 0
                            Layout.margins: 0

                            TextEdit {
                                Layout.fillWidth: true
                                id: resultDevID
                                font.family: "Roboto"
                                font.pixelSize: 10
                                text: "Unbekanntes Gerät"
                                color: "#de000000"
                                readOnly: true
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.WordWrap
                                selectByMouse: true
                            }

                            Text {
                                Layout.topMargin: 14
                                Layout.fillWidth: true
                                id: resultCaption
                                font.family: "Roboto"
                                font.pixelSize: 24
                                text: "INIT"
                                color: "#de000000"
                            }
                            Text {
                                Layout.topMargin: 12
                                Layout.fillWidth: true
                                id: txtStart
                                font.family: "Roboto"
                                font.pixelSize: 14
                                text: "Start: xxx"
                                color: "#99000000"
                                elide: Text.ElideRight
                                verticalAlignment: Text.AlignTop
                                maximumLineCount: 1
                            }
                            Text {
                                Layout.fillWidth: true
                                Layout.topMargin: 2
                                id: txtDuration
                                font.family: "Roboto"
                                font.pixelSize: 14
                                text: "Dauer: xxx"
                                color: "#99000000"
                                elide: Text.ElideRight
                                verticalAlignment: Text.AlignTop
                                maximumLineCount: 1
                            }
                        } /* ColumnLayout Text */

                        ColumnLayout {
                            Rectangle {
                                /* icon placeholder */
                                id: iconRect
                                Layout.minimumWidth: 80
                                Layout.maximumWidth: 80
                                Layout.minimumHeight: 80
                                Layout.maximumHeight: 80
                                color: "transparent"
                                BusyIndicator {
                                    id: busy
                                    visible: false
                                    anchors.fill: parent
                                    Material.accent: Material.color(
                                                         root.secondaryColor)
                                }
                                SuccessIcon {
                                    id: sucIcon
                                    finalRadius: 40
                                    replayFactor: 2
                                    anchors.fill: parent
                                    circleColor: Material.color(Material.Green)
                                }
                                ErrorIcon {
                                    id: errIcon
                                    finalRadius: 40
                                    replayFactor: 2
                                    anchors.fill: parent
                                    circleColor: Material.color(Material.Red)
                                }
                            } /* Icon placeholder */
                            Rectangle {
                                Layout.fillHeight: true
                                Layout.fillWidth: true
                                color: "transparent"
                            }
                        } /* Column Layout Icon */
                    }

                    RowLayout {
                        Layout.leftMargin: 8
                        Layout.topMargin: 8
                        spacing: 0
                        Button {
                            text: "Zeige Ergebnisse"
                            Material.elevation: 0
                            Material.foreground: Material.color(
                                                     root.secondaryColor)
                        }
                    }
                } /* Column Layout */

                Component.onCompleted: {

                }
            }
        }
        RowLayout {
            Layout.fillHeight: true
            Layout.minimumWidth: col.width
            Layout.maximumWidth: col.width
            Layout.minimumHeight: 300
            spacing: 16
            Pane {
                id: runResultsTable
                Material.elevation: 6
                Layout.fillHeight: true
                Layout.fillWidth: true

                ScrollView {
                    clip: true
                    anchors.fill: parent
                    TextArea {
                        id: curResult
                        anchors.fill: parent
                        font.family: "Courier New"
                        font.pixelSize: 14
                        color: "#99000000"
                    }
                }
            }
            Pane {
                id: nonProcessParams
                Material.elevation: 6
                Layout.minimumWidth: 344
                Layout.fillHeight: true
                ParamsViewer {
                    id: tempParamsViewer
                    anchors.fill: parent
                    model: null /* set onTestRunenrChanged */
                }
            }
        }

        RowLayout {
            Layout.minimumHeight: 50
            Layout.maximumHeight: 50
            Layout.minimumWidth: col.width
            Layout.maximumWidth: col.width
            spacing: 16
            Rectangle {
                id: spacer
                color: "transparent"
                Layout.fillWidth: true
            }
            Text {
                Layout.maximumWidth: 120
                Layout.minimumWidth: 120
                font.family: "Roboto"
                font.pointSize: 10
                id: txtCancel
                visible: false
                text: qsTr("")
            }
            Button {
                Layout.maximumWidth: 180
                Layout.minimumWidth: 180
                id: manualStart
                text: qsTr("manueller Start")
                Material.accent: Material.color(root.secondaryColor)
                highlighted: true
                onClicked: {
                    if (testSuite.isRunning() === true) {
                        testSuite.abort()
                        txtCancel.visible = true
                    } else
                        testSuite.run()
                }
            }
        }
    } /* ColumnLayout */

    Timer {
        id: busyTxtTimer
        interval: 300
        running: true
        repeat: true
        onTriggered: {
            internal._curIdx = internal._curIdx + 1
            if (internal._curIdx > 3)
                internal._curIdx = 0

            var i = 0
            var txt = "Busy"
            if (testSuite.isRunning() === true) {
                busy.visible = true
                for (i = 0; i < internal._curIdx % 4; i++) {
                    txt = txt + "."
                }
                resultCaption.text = txt
            }

            var txtCancelContent = qsTr("Wird abgebrochen")
            if (testSuite.isRunning() === true) {
                for (i = 0; i < internal._curIdx % 4; i++) {
                    txtCancelContent = txtCancelContent + "."
                }
                txtCancel.text = txtCancelContent
            }
        }
    }
}
