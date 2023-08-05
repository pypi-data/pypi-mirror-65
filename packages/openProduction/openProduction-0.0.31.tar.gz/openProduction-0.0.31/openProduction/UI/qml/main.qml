import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import "TestRunnerSimple"

Window {
    id: mainWindow
    visible: true
    width: 640
    height: 480
    title: qsTr("openProduction")
    property string primaryColor: Material.Blue;
    property string secondaryColor: Material.Orange;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);
    property string surfaceColor: "white";
    property bool invalidStation: true

    property string stationName: openProduction.getStationName()
    property string workspace: openProduction.getWorkspace()
    property string programVersion: openProduction.getVersion()

    property string role: "Production"

    visibility: "Maximized"

    flags: Qt.Window | Qt.FramelessWindowHint // Disable window frame

    signal contentAreaLoad(string source)

    function onDisableScreen(visible) {
        disableScreen.visible = visible;
    }

    function toggleSideMenu()
    {
        menuIcon.backgroundColor=Material.color(mainWindow.primaryColor)
        surround.color= Material.color(mainWindow.primaryColor)
        menuIcon.toggle()
        if (sideMenu.state === "hidden") {
            sideMenu.state = "shown"
        }
        else {
            sideMenu.state = "hidden"
        }
    }

    function onErrorOccured()
    {
        disableScreen.visible=false;
        menuView.currentIndex = mainWindow.invalidStation? sideMenu.installIdx:0;
    }


    Rectangle {
        objectName: "disableOverlay"
        id: disableScreen
        anchors.fill: parent
        color: "#aacfdbe7"
        z:5
        MouseArea {
            anchors.fill: parent
        }
    }

    TestRunnerSimple {
        id: loadingScreen
        objectName: "loadingScreen"
        runner: station.loadStationAsync(mainWindow.workspace, mainWindow.stationName)
        primaryColor: mainWindow.primaryColor
        secondaryColor: mainWindow.secondaryColor
        backgroundColor: mainWindow.backgroundColor
        footerText: ""
        title: qsTr("Lade " + mainWindow.stationName)

        onTerminate: {
            if (loadingScreen.state === "success")
            {
                mainWindow.invalidStation = false;
            }
            else
            {
                mainWindow.invalidStation = true;
                mainWindow.stationName = "<no station loaded>"
            }

            disableScreen.visible=false;
        }
    }


    Pane {
        id: mainContentArea
        x:sideMenu.x + sideMenu.width
        y:header.height
        height: mainWindow.height - y- footer.height
        width: mainWindow.width - (x)
        Material.background: mainWindow.backgroundColor

        Loader {
            id: contentLoader
            anchors.fill: parent
            source: menuView.currentItem.sourceOfThisDelegate

            onSourceChanged: {
                mainWindow.contentAreaLoad(source)
                console.log(source)
            }

            onLoaded: {
                contentLoader.item.primaryColor    = mainWindow.primaryColor;
                contentLoader.item.secondaryColor  = mainWindow.secondaryColor;
                contentLoader.item.backgroundColor = mainWindow.backgroundColor;
                contentLoader.item.disableScreen.connect(onDisableScreen)
                contentLoader.item.toggleSideMenu.connect(toggleSideMenu)
            }

            onStatusChanged: {contentLoader.item.opacity=0; if (contentLoader.status === Loader.Ready) {opacityLoader.start();}}
        }

        OpacityAnimator {
            id: opacityLoader
            target: contentLoader.item;
            from: 0;
            to: 1;
            duration: 300
            running: false
        }
    }

    Rectangle {
            id: header
            x:sideMenu.width+sideMenu.x
            y:0
            height: 80
            width: mainWindow.width
            color: Material.color(mainWindow.primaryColor)
            property string title: menuView.currentItem.titleOfThisDelegate

            Material.foreground: "white"

            Row {
                spacing: 20
                anchors.fill: parent

                Rectangle {
                    width:5
                    color: "transparent"
                    height: 50
                }

                Rectangle {
                    id: surround
                    y:15
                    width: 50
                    height: 50
                    radius: 50
                    x: 0
                    color: header.color

                    MenuAnim {
                        id: menuIcon
                        x:2
                        y:1
                        width:48
                        height:48

                        backgroundColor: "transparent"
                        arrowFormState: false

                        MouseArea {
                            anchors.fill: parent

                            onClicked: {
                                mainWindow.toggleSideMenu()
                            }
                            hoverEnabled: true

                            onEntered: {
                                surround.color= Material.color(mainWindow.primaryColor, Material.Shade700)
                                menuIcon.backgroundColor= Material.color(mainWindow.primaryColor, Material.Shade700)
                                menuIcon.requestPaint()
                            }
                            onExited: {
                                surround.color=Material.color(mainWindow.primaryColor)
                                menuIcon.backgroundColor=Material.color(mainWindow.primaryColor)
                                menuIcon.requestPaint()
                            }
                        }
                    }
                }

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    text: header.title
                    //font.pointSize: 14
                    //font.family: "Roboto"

                    font.family: "Concert One"
                    font.weight: Font.Light
                    font.letterSpacing: -1.5
                    font.pointSize: 16
                    color: header.Material.foreground
                }
            }


        } /* header */

        Rectangle {
            id: footer
            x:sideMenu.width+sideMenu.x
            y:mainWindow.height - height
            height: header.height/2
            width: mainWindow.width
            color: Material.color(mainWindow.primaryColor)
            RowLayout {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                Layout.topMargin: 10
                spacing: 0
                Text {
                    Layout.fillHeight: true
                    Layout.leftMargin: 40
                    text: mainWindow.stationName + " (workspace " + mainWindow.workspace + " "
                    font.pointSize: 8
                    font.family: "Roboto"
                    color: "white"
                    Layout.alignment: Qt.AlignVCenter
                    verticalAlignment: Text.AlignVCenter
                }
                TabButton {
                    Material.accent: Material.color(mainWindow.secondaryColor);
                    icon.source: "icons/open-folder.png"
                    icon.width:16
                    icon.height:16
                    Layout.maximumHeight: 16
                    Layout.minimumHeight: 16
                    Layout.alignment: Qt.AlignVCenter
                    padding: 0
                    spacing: 0
                    onClicked: {helper.openExplorer(mainWindow.workspace);}

                }
                Text {
                    Layout.fillHeight: true
                    text: " )"
                    font.pointSize: 8
                    font.family: "Roboto"
                    color: "white"
                    Layout.alignment: Qt.AlignVCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

        Pane {

            id:sideMenu
            width: 200
            height: mainWindow.height-y
            x:0
            y:0
            property int installIdx: 5
            Material.elevation: 10
            Material.background: "white"
            padding: 0

            ListView {
                id: menuView
                anchors.fill: parent

                currentIndex: mainWindow.invalidStation? sideMenu.installIdx:0

                model: SideMenuModel {}
                delegate: ToolButton{
                    id: control
                    property int indexOfThisDelegate: index
                    property string backgroundColor: sideMenu.Material.background//"black"//Material.color(mainWindow.primaryColor, Material.Shade400)
                    property string backgroundColorHover: Material.color(Material.Grey, Material.Shade300)//"#474b57"//
                    property string backgroundColorActivated: Material.color(mainWindow.secondaryColor)
                    property bool isActivated: ListView.isCurrentItem
                    property string titleOfThisDelegate: menuTitle
                    property string sourceOfThisDelegate: source
                    x: 0
                    width: sideMenu.width-1
                    text: name
                    property string iconPath: ListView.isCurrentItem ? iconNameSelected : iconName
                    Material.background: ListView.isCurrentItem ? Material.color(mainWindow.secondaryColor) : Material.color(mainWindow.primaryColor, Material.Shade400)
                    Material.accent : ListView.isCurrentItem ? Material.color(mainWindow.secondaryColor) : Material.color(mainWindow.primaryColor, Material.Shade400)
                    Material.primary : ListView.isCurrentItem ? Material.color(mainWindow.secondaryColor) : Material.color(mainWindow.primaryColor, Material.Shade400)
                    enabled: (mainWindow.invalidStation&&index!=sideMenu.installIdx)?false:true

                    background: Rectangle {
                            function getBackgroundColor() {
                                var rv;
                                if (control.isActivated === true)
                                    rv = control.backgroundColorActivated
                                else if (control.hovered === true)
                                    rv = control.backgroundColorHover
                                else
                                    rv = control.backgroundColor
                                return rv;
                            }

                            implicitWidth: 100
                            implicitHeight: 40
                            opacity: enabled ? 1 : 0.3
                            Material.background: getBackgroundColor()
                            color: getBackgroundColor()
                            Material.elevation: control.isActivated ? 6:0
                        }

                    onClicked: {
                        control.ListView.view.currentIndex = control.indexOfThisDelegate;
                    }

                    contentItem: Item {
                                Row {
                                    id: sideMenuDelegateRow
                                    //anchors.horizontalCenter: parent.horizontalCenter
                                    spacing: 5
                                    Rectangle {
                                        width: 20
                                        height: 20
                                         color: "transparent"

                                    }

                                    function getItemColor() {
                                        var rv;
                                        if (control.enabled === false)
                                            rv = "grey"
                                        else if (control.ListView.isCurrentItem)
                                            rv = "white"
                                        else
                                            rv = "black"
                                        return rv
                                    }



                                    Image {
                                        id: imgMenu
                                        source: control.iconPath
                                        width: 20
                                        height: 20

                                        /*
                                        ColorOverlay {
                                            anchors.fill: imgMenu
                                            source: imgMenu
                                            //color: "#ff0000"  // make image like it lays under red glass
                                            color: sideMenuDelegateRow.getItemColor()//control.ListView.isCurrentItem ? "white" : "black"
                                        }
                                        */


                                    }


                                    Text {
                                        text: control.text
                                        font.bold: control.isActivated ? true : false
                                        font.family: "Roboto"
                                        font.pointSize: 10
                                        color: sideMenuDelegateRow.getItemColor()//control.ListView.isCurrentItem ? "white" : "black"
                                        anchors.verticalCenter: parent.verticalCenter
                                    }
                                }
                        }

                }

                header: Component {
                    Column {
                        Rectangle {
                            width:sideMenu.width
                            height:80
                            color: "#313443"//Material.color(mainWindow.secondaryColor )
                            Row {
                                x:10
                                y:10
                                spacing:10
                                Rectangle {
                                    id: listLogo
                                    height:60
                                    width:60

                                    radius: 60

                                    color: backgroundColor;

                                    Image {
                                        anchors.horizontalCenter:  parent.horizontalCenter
                                        anchors.verticalCenter: parent.verticalCenter
                                        width: listLogo.width-20
                                        height: listLogo.height-20
                                        source: "icons/img2.png"
                                    }
                                }

                                Column
                                {
                                    spacing:10
                                    Text {
                                        id: logoText

                                        text: "openProduction"
                                        font.family: "Concert One"
                                        font.weight: Font.Light
                                        font.pointSize: 10
                                        color: "white"
                                    }
                                    Text {
                                        width:parent.width
                                        //anchors.horizontalCenter:  parent.left
                                        text: mainWindow.programVersion
                                        font.family: "Roboto"
                                        font.pointSize: 8
                                        font.bold: true
                                        //color: "white"
                                        color: Material.color(Material.Grey, Material.Shade500);
                                        horizontalAlignment: Text.AlignRight

                                    }
                                }
                            }
                        }

                        /*
                        Rectangle {
                            width:sideMenu.width
                            height:20
                            color: "#313443"
                        }
                        */
                    }
                } /* header */

                // The delegate for each section header
                   Component {
                       id: sectionHeading
                       Rectangle {
                           y:40
                           width: sideMenu.width
                           height: childrenRect.height +60
                           color: sideMenu.Material.background

                           Text {
                               x: 25
                               y: 40
                               text: section
                               font.family: "Roboto"
                               font.pointSize: 10
                               color: Material.color(Material.Grey)
                           }
                       }
                   }

                section.property: "section"
                section.criteria: ViewSection.FullString
                section.delegate: sectionHeading

            } /* ListView */

            states: [
                    State {
                        name: "shown"
                    },
                State {
                    name: "hidden"
                }
                ]

            transitions: [
                Transition {
                    to: "hidden"
                    NumberAnimation { target:sideMenu; properties: "x"; easing.type: Easing.InOutQuad; from: 0; to: -sideMenu.width; duration: 300 }
                },
                Transition {
                    to: "shown"
                    NumberAnimation { target:sideMenu; properties: "x"; easing.type: Easing.InOutQuad; from: -sideMenu.width; to: 0; duration: 300 }
                }
            ]
        } /* sideMenu */

    TitleBar {
        id: titleBar
        title:""
        titleBarColor: "transparent"
    }
}
