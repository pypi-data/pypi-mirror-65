import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import "../Common"

Window {
    id: root
    visible: true
    width: 640
    height: 480+50
    title: qsTr("Produkt rüsten")
    property string primaryColor: Material.Indigo;
    property string secondaryColor: Material.Orange;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);
    property string surfaceColor: "white";
    property string footerText: "Bauernstolz - AA - Revision 3"
    property bool closeAccepted: false
    property alias state: busyArea.state
    property string runnerType: "regular"
    signal terminate;

    property QtObject runner: null;

    flags: Qt.FramelessWindowHint
    modality: Qt.ApplicationModal

    color: backgroundColor

    signal testRunnerFinished(bool success)

    onClosing: {
        if (root.closeAccepted === false)
            close.accepted = false
        else
            terminate();
    }

    Component.onCompleted: {
        root.requestActivate()
    }

    function onErrorButtonClosed() {
        testRunnerFinished(false);
        root.closeAccepted = true
        root.close();
    }

    function init() {
        path.curIdx = 0;
        runner.setStepType(runnerType)
        runner.stepStart.connect(onStepStart)
        runner.stepComplete.connect(onStepComplete)
        busyArea.errorBtnPressed.connect(onErrorButtonClosed);
        if (runnerType.toLowerCase() === "unload")
            runner.unloadSuite()
        else
            runner.loadSuite()
    }

    onRunnerChanged: {
        if (runner !== null)
            init()
    }

    function onStepStart(testCaseDoc, idx, numCases) {
        busyArea.caption = testCaseDoc;
        path.curIdx = idx;
    }

    function onSequenceComplete(testCaseDoc, idx, numCases) {
        busyArea.caption = testCaseDoc;
        path.curIdx = idx;
    }

    function onStepComplete(suiteState, stepResult, stepMsg, stepCompleteName, idx, numCases) {
        if (stepResult !== 0 && stepResult !== 4)
        {
            busyArea.state = "error"
            if (stepResult === 1)
                busyArea.details = "FAIL: " + stepCompleteName;
            else if (stepResult === 2)
                busyArea.details = "ERROR: " + stepCompleteName;
            busyArea.errorDetails = stepMsg
        }
        else
        {
            if (idx+1 === numCases)
            {
                busyArea.state = "success"
                delay2(1000, function(){root.closeAccepted = true; root.testRunnerFinished(true); root.close(); })
            }
        }
    }

    Timer {
        id: timer
    }

    Timer {
        id: timer2
    }

    ParallelAnimation {
        id: closingAnimation
        PropertyAnimation {
            target: root;
            property: "width";
            to: 10;
            duration: 100 }
        PropertyAnimation {
            target: root;
            property: "height";
            to: 10;
            duration: 100 }
        PropertyAnimation {
            target: root;
            property: "x";
            to: root.x+root.width/2;
            duration: 100 }
        PropertyAnimation {
            target: root;
            property: "y";
            to: root.y+root.height/2;
            duration: 100 }
    }

    function delay(delayTime, cb) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }

    function delay2(delayTime, cb) {
        timer2.interval = delayTime;
        timer2.repeat = false;
        timer2.triggered.connect(cb);
        timer2.start();
    }

    Rectangle {
        id: header
        x:0
        y:0
        height: 70
        width: root.width
        color: Material.color(root.primaryColor, Material.Shade700)
        Text {
            x: 40
            y: 20
            text: root.title
            font.pointSize: 14
            font.family: "Roboto"
            color: "white"
        }
    }

    Rectangle {
        id: footer
        x:0
        y:root.height - height
        height: header.height/2
        width: root.width
        color: Material.color(root.primaryColor, Material.Shade700)
        Text {
            x: 40
            y: 10
            text: root.footerText
            font.pointSize: 8
            font.family: "Roboto"
            color: "white"
        }
    }

    Row {
        id: path
        property int curIdx: 0
        y: header.height + 10
        x: 10
        width: root.width-x*2

        Repeater {
            id: repeat
            model: runner.getTestCases()//["Produkt rüsten", "oranges", "pears"]

                Column{
                    id: column
                    height:100
                    width: parent.width/repeat.count
                    Row {
                        function getCircleColor()
                        {
                            if (column.Positioner.index < path.curIdx)
                            {
                                return Material.color(root.primaryColor, Material.Shade200)
                            }
                            else if (column.Positioner.index === path.curIdx)
                            {
                                return Material.color(root.primaryColor, Material.Shade700)
                            }
                            else
                            {
                                return Material.color(root.primaryColor, Material.Shade50)
                            }
                        }

                        function getFirstPathColor()
                        {
                            if (column.Positioner.isFirstItem)
                            {
                                return root.backgroundColor
                            }
                            else if (column.Positioner.index <= path.curIdx)
                            {
                                return Material.color(root.primaryColor, Material.Shade200)
                            }
                            else
                            {
                                return Material.color(root.primaryColor, Material.Shade50)
                            }
                        }
                        function getLastPathColor()
                        {
                            if (column.Positioner.isLastItem)
                            {
                                return root.backgroundColor
                            }
                            else if (column.Positioner.index < path.curIdx)
                            {
                                return Material.color(root.primaryColor, Material.Shade200)
                            }
                            else
                            {
                                return Material.color(root.primaryColor, Material.Shade50)
                            }
                        }

                        height:parent.height/2
                        width: parent.width
                        Rectangle {
                            y:25
                            width:column.width/2-circle.width/2+5
                            height:10
                            z:0
                            color: parent.getFirstPathColor()
                        }
                        Rectangle {
                            id: circle
                            y:20
                            width:20
                            height:20
                            radius:20
                            color:parent.getCircleColor()
                            z:1
                        }
                        Rectangle {
                            y:25
                            width:column.width/2-circle.width/2+5
                            height:10
                            z:0
                            color: parent.getLastPathColor()
                        }
                        spacing: -5
                    }

                    Text {
                        horizontalAlignment: Text.AlignHCenter
                        text: modelData
                        height:parent.height/2
                        width: parent.width
                        color: (column.Positioner.index === path.curIdx) ?  Material.color(root.primaryColor, Material.Shade700) : "black"
                        font.bold: (column.Positioner.index === path.curIdx) ? true : false
                        font.family: "Roboto"
                        font.pointSize: 8
                    }
                }
        }
    }

    BusyIndication {
        secondaryColor: Material.color(root.secondaryColor)
        id:busyArea
        x: 40
        y: header.height + 100
        width: root.width-x*2
        height: footer.y - (path.y + path.height)
    }

}
