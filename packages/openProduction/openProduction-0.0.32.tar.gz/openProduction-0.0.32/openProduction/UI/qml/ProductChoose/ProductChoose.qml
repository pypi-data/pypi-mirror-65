import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4

Item {
    id: root
    visible: true
    width: 640
    height: 480

    property string primaryColor: Material.Blue;
    property string secondaryColor: Material.Orange;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);
    property string headerBackgroundColor: "#313443"
    property string headerFontColor: "white"
    property string overlayColor: "#aacfdbe7"

    signal errorOccured;
    signal productSelected(string productName, string productVersion, int productRevision);

    QtObject {
        id: internal
        property var changedProducts: []
    }

    function onPopupClosed(productName, discarded) {
        if (internal.changedProducts.length > 0)
        {
            var nextProduct = internal.changedProducts.pop();
            var rv = station.productGetBaseVersion(nextProduct);
            var productVersion = rv[0];
            var productRevision = rv[1];
            overlayPopup.open(nextProduct, productVersion, productRevision);
        }
    }

    function onProductSaveComplete(productName, success, revision) {
        var details;
        var message;
        if (success)
        {
            message = qsTr("Speichern erfolgreich")
            details = qsTr("Neue Revision " + revision)
        }
        else
        {
            message = qsTr("Fehler beim Speichern")
            details = qsTr("Siehe log Nachrichten")
        }

        busyIndicationPopup.item.close(message, details, success)
    }

    Component.onCompleted: {
        overlayPopup.closed.connect(root.onPopupClosed)
        station.productSaveComplete.connect(root.onProductSaveComplete)
    }

    Item {
        id: overlayPopup
        anchors.fill: parent
        z:100

        function open(productName, productVersion, productRevision) {
            overlay.visible = true
            popup.productName = productName;
            popup.productVersion = productVersion;
            popup.productRevision = productRevision;
            overlayFadeIn.start()
            popup.open()
        }

        function close() {
            overlayFadeOut.start()
            popup.close()
        }

        signal closed(string productName, bool discard)

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
            height: 182
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

            ColumnLayout {
                id: popupLayout
                x:0
                y:0
                width:parent.width
                height: parent.height
                Layout.margins: 0

                Rectangle {
                    Layout.leftMargin: 24
                    Layout.rightMargin: 24
                    Layout.preferredHeight: 40
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.fillWidth: true
                    color: "transparent"
                    Text {
                        anchors.fill: parent
                        text: qsTr("Produkt '" + popup.productName + "' hat lokale Änderungen")
                        font.pixelSize: 20
                        color: "#de000000"
                        font.family: "roboto"
                        font.bold: true
                        elide: Text.ElideRight
                        verticalAlignment: Text.AlignBottom
                    }
                }

                Rectangle {
                    Layout.leftMargin: 24
                    Layout.rightMargin: 24
                    Layout.topMargin: 20
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    color:"transparent"
                    Text {
                        anchors.fill: parent
                        text: qsTr("Als letzte gültige Basisversion wurde "+popup.productVersion+"."+popup.productRevision+" erkannt. Möchten Sie die lokalen Änderungen verwerfen oder übernehmen?")
                        font.pixelSize: 16
                        color: "#99000000"
                        font.family: "roboto"
                        Layout.bottomMargin: 28
                        maximumLineCount: 3
                        wrapMode: Text.WordWrap
                        elide: Text.ElideRight
                    }
                }


                Rectangle {
                    Layout.alignment: Qt.AlignBottom
                    color: "transparent"
                    Layout.minimumHeight: 52
                    Layout.maximumHeight: 52
                    Layout.minimumWidth: 560
                    Layout.maximumWidth: 560
                    RowLayout {
                        anchors.fill: parent
                        Layout.margins: 8
                        //Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                        Item {
                            // spacer item
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Rectangle { anchors.fill: parent; color: "transparent" } // to visualize the spacer
                        }
                        Button {
                            onClicked: {
                                overlayPopup.close();
                                overlayPopup.closed(popup.productName, true);
                                station.discardLocalChanges(popup.productName);
                            }
                            text: qsTr("verwerfen")
                            flat: true
                            Material.foreground: Material.color(root.primaryColor)
                        }
                        Button {
                            Layout.rightMargin: 8
                            onClicked: {
                                overlayPopup.close();
                                overlayPopup.closed(popup.productName, false);

                                //async call -> onProductSaved is called at termination
                                busyIndicationPopup.source = "../Common/BusyIndicationPopup.qml"
                                busyIndicationPopup.item.caption = "Speichere Änderungen"
                                busyIndicationPopup.item.open()
                                station.productSaveChangesAsync(popup.productName);
                            }
                            text: qsTr("übernehmen")
                            flat: true
                            Material.foreground: Material.color(root.primaryColor)
                        }
                    }
                }
            }
        } /* PopUp */
    }

    Item {
        id: busyPopup
        anchors.fill: parent
        z: 100

        Loader {
            anchors.fill: parent
            id: busyIndicationPopup
            // position the Loader in the center
            // of the parent
            source: ""
            onLoaded: {
                busyIndicationPopup.item.errorOccured.coonect(errorOccured)
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        RowLayout {
            id: listRow
            spacing: 10
            Layout.fillHeight: true
            Layout.leftMargin: 24
            Layout.rightMargin: 8

            Pane {
                id: productPane
                Layout.fillWidth: true
                Layout.minimumHeight: 356
                Layout.fillHeight: true

                Material.elevation: 6
                Material.background: "white"//"#313443"//Material.color(Material.Black, Material.Shade800)//Material.color(root.primaryColor, Material.Shade400);
                padding: 0

                ListView {

                    id: menuViewProduct
                    anchors.fill: parent

                    currentIndex: 0

                    onCurrentItemChanged:
                    {
                        console.log("productPane onCurrentItemChanged")
                        if (currentItem !== null)
                        {
                            var rv = station.getVersionModel(currentItem.text)
                            menuViewVersion.model = rv
                        }
                    }

                    model: station.getProductModel()
                    delegate: ToolButton{
                        property variant myData: model

                        id: controlProduct
                        property int indexOfThisDelegate: index
                        property string detailsOfThisDelegate: details
                        property string backgroundColor: "white"//"black"//Material.color(root.primaryColor, Material.Shade400)
                        property string backgroundColorHover: Material.color(Material.Grey, Material.Shade300)//"#474b57"//
                        property string backgroundColorActivated: Material.color(root.secondaryColor, Material.Shade200)
                        property bool isActivated: ListView.isCurrentItem
                        x: 0
                        width: parent.width
                        height:72
                        text: name
                        Material.background: ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.accent : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.primary : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        enabled: true
                        padding: 0

                        background: Rectangle {
                            function getBackgroundColor() {
                                var rv;
                                if (controlProduct.isActivated === true)
                                    rv = controlProduct.backgroundColorActivated
                                else if (controlProduct.hovered === true)
                                    rv = controlProduct.backgroundColorHover
                                else
                                    rv = controlProduct.backgroundColor
                                return rv;
                            }

                            implicitWidth: 100
                            implicitHeight: 40
                            opacity: enabled ? 1 : 0.3
                            color: getBackgroundColor()
                        }

                        onClicked: {
                            controlProduct.ListView.view.currentIndex = controlProduct.indexOfThisDelegate;
                        }

                        contentItem: Item {
                            RowLayout {
                                id: sideMenuDelegateRow
                                //anchors.horizontalCenter: parent.horizontalCenter
                                Rectangle {
                                    color:"transparent"
                                    Layout.minimumHeight: 72
                                    Layout.minimumWidth: 40
                                    Layout.maximumHeight: 72
                                    Layout.maximumWidth: 40
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignHCenter

                                    Image {
                                        x: 16
                                        id: imgProduct
                                        width: 24
                                        height: 24
                                        anchors.verticalCenter: parent.verticalCenter
                                        //anchors.centerIn: parent

                                        source: "../icons/tag.png"

                                        /*
                                        ColorOverlay {
                                            anchors.fill: parent
                                            source: imgProduct
                                            color: "grey"
                                        }
                                        */
                                    }
                                }


                                ColumnLayout {
                                    Layout.leftMargin: 32
                                    Text {

                                        height: controlProduct.height
                                        Layout.preferredWidth: controlProduct.width - imgProduct.width-imgProduct.x

                                        text: controlProduct.text
                                        horizontalAlignment: Text.AlignVCenter
                                        font.bold: false//controlProduct.isActivated ? true : false
                                        font.family: "Roboto"
                                        font.pixelSize: 16
                                        color: "#de000000"
                                        //anchors.verticalCenter: parent.verticalCenter
                                    }

                                    Text {
                                        height: controlProduct.height
                                        Layout.preferredWidth: controlProduct.width - imgProduct.width-imgProduct.x

                                        text: detailsOfThisDelegate
                                        horizontalAlignment: Text.AlignVCenter
                                        font.bold: false//controlProduct.isActivated ? true : false
                                        font.family: "Roboto"
                                        font.pixelSize: 14
                                        color: "#99000000"
                                        //anchors.verticalCenter: parent.verticalCenter
                                    }
                                }
                            }
                        }

                    }

                    headerPositioning: ListView.OverlayHeader
                    clip: true

                    header: Component {
                        Column {
                            z:100
                            Rectangle {
                                width:menuViewProduct.width
                                height:60
                                color: root.headerBackgroundColor
                                Text {
                                    anchors.fill: parent
                                    //anchors.horizontalCenter:  parent.left
                                    text: "Product"
                                    font.family: "Concert One"
                                    font.weight: Font.Light
                                    font.letterSpacing: -1.5
                                    font.pointSize: 16
                                    color: root.headerFontColor//"white"//Material.color(Material.Grey, Material.Shade500);

                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter

                                }
                            }
                        }
                    } /* header */
                } /* ListView */
            } /* productPane */

            Pane {
                id: versionPane
                Layout.fillWidth: true
                Layout.minimumHeight: 356
                Layout.fillHeight: true

                Material.elevation: 6
                Material.background: "white"//"#313443"//Material.color(Material.Black, Material.Shade800)//Material.color(root.primaryColor, Material.Shade400);
                padding: 0

                ListView {
                    id: menuViewVersion
                    anchors.fill: parent

                    currentIndex: 0

                    onCurrentItemChanged:
                    {
                        if (menuViewProduct.currentItem !== null && currentItem !== null)
                        {
                            var productName = menuViewProduct.currentItem.text;
                            var productVersion = currentItem.text
                            console.log(productName, productVersion);
                            station.reloadRevisionModel(productName, productVersion)
                        }
                        /*
                        comboRevision.currentIndex = 0;
                        comboRevision.contentText = comboRevision.model.getName(comboRevision.currentIndex);
                        comboRevision.contentDate = comboRevision.model.getDate(comboRevision.currentIndex);
                        */
                    }

                    model: {}
                    delegate: ToolButton{
                        id: controlVersion
                        property int indexOfThisDelegate: index
                        property string backgroundColor: "white"//"black"//Material.color(root.primaryColor, Material.Shade400)
                        property string backgroundColorHover: Material.color(Material.Grey, Material.Shade300)//"#474b57"//
                        property string backgroundColorActivated: Material.color(root.secondaryColor, Material.Shade200)
                        property bool isActivated: ListView.isCurrentItem
                        property string imagePathOfThisDelegate: imageSource
                        property string commentOfThisDelegate: comment
                        x: 0
                        width: parent.width
                        height: 88
                        text: name
                        Material.background: ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.accent : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.primary : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        enabled: true
                        padding: 0

                        background: Rectangle {
                            function getBackgroundColor() {
                                var rv;
                                if (controlVersion.isActivated === true)
                                    rv = controlVersion.backgroundColorActivated
                                else if (controlVersion.hovered === true)
                                    rv = controlVersion.backgroundColorHover
                                else
                                    rv = controlVersion.backgroundColor
                                return rv;
                            }

                            implicitWidth: 100
                            implicitHeight: 40
                            opacity: enabled ? 1 : 0.3
                            color: getBackgroundColor()
                        }

                        onClicked: {
                            controlVersion.ListView.view.currentIndex = controlVersion.indexOfThisDelegate;
                        }

                        contentItem: Item {
                            RowLayout {
                                id: contentVersionListRow

                                Rectangle {
                                    id: contentVersionImage
                                    color: "transparent"
                                    Layout.topMargin: 16
                                    Layout.bottomMargin: 16
                                    Layout.minimumHeight: 56
                                    Layout.minimumWidth: 100
                                    Layout.maximumHeight: 56
                                    Layout.maximumWidth: 100
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignHCenter

                                    Image {
                                        x: 0
                                        id: img
                                        width: 56
                                        height: 56
                                        anchors.centerIn: parent
                                        //y:5
                                        source: imagePathOfThisDelegate
                                    }
                                }

                                ColumnLayout  {
                                    Layout.leftMargin: 16
                                    Text {
                                        id: versionHeading
                                        text: controlVersion.text
                                        font.bold: false //controlVersion.isActivated ? true : false
                                        font.family: "Roboto"
                                        font.pixelSize: 16
                                        color: "#de000000"
                                        height:30
                                        Layout.maximumWidth: controlVersion.width-contentVersionImage.width-56
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        id: commentText
                                        Layout.maximumWidth: controlVersion.width-contentVersionImage.width-56
                                        text: controlVersion.commentOfThisDelegate
                                        font.family: "Roboto"
                                        font.pixelSize: 12
                                        //wrapMode: Text.WordWrap
                                        wrapMode: Text.WordWrap
                                        horizontalAlignment: Text.AlignJustify
                                        maximumLineCount: 2
                                        elide: Text.ElideRight
                                        color: "#99000000"
                                        ToolTip.visible: hovered
                                        ToolTip.text: controlVersion.commentOfThisDelegate
                                    }
                                }
                            }
                        }

                    }

                    headerPositioning: ListView.OverlayHeader
                    clip: true

                    header: Component {
                        Column {
                            z:100
                            Rectangle {
                                width:menuViewVersion.width
                                height:60
                                color: root.headerBackgroundColor
                                Text {
                                    anchors.fill: parent
                                    text: "Version"
                                    font.family: "Concert One"
                                    font.weight: Font.Light
                                    font.letterSpacing: -1.5
                                    font.pointSize: 16
                                    color: root.headerFontColor

                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter

                                }
                            }
                        }
                    } /* header */
                } /* ListView */
            } /* versionPane */

            Pane {
                visible: true
                id: revisionPane
                Layout.fillWidth: true
                Layout.minimumHeight: 356
                Layout.fillHeight: true

                Material.elevation: 6
                Material.background: "white"//"#313443"//Material.color(Material.Black, Material.Shade800)//Material.color(root.primaryColor, Material.Shade400);
                padding: 0

                ListView {
                    id: menuViewRevision
                    anchors.fill: parent
                    currentIndex: 0
                    model: station.getRevisionModel()

                    delegate: ToolButton{
                        id: controlRevision
                        property int indexOfThisDelegate: index
                        property string dateOfThisDelegate: date
                        property string backgroundColor: "white"
                        property string backgroundColorHover: Material.color(Material.Grey, Material.Shade300)
                        property string backgroundColorHoverNested: Material.color(Material.Grey, Material.Shade400)
                        property string backgroundColorActivated: Material.color(root.secondaryColor, Material.Shade200)
                        property bool isActivated: ListView.isCurrentItem
                        x: 0
                        width: parent.width
                        height:72
                        text: name
                        Material.background: ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.accent : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        Material.primary : ListView.isCurrentItem ? Material.color(root.secondaryColor) : Material.color(root.primaryColor, Material.Shade400)
                        enabled: true
                        padding: 0

                        background: Rectangle {
                            function getBackgroundColor() {
                                var rv;
                                if (controlRevision.isActivated === true)
                                    rv = controlRevision.backgroundColorActivated
                                else if (controlRevision.hovered === true)
                                    rv = controlRevision.backgroundColorHover
                                else
                                    rv = controlRevision.backgroundColor
                                return rv;
                            }

                            implicitWidth: 100
                            implicitHeight: 40
                            opacity: enabled ? 1 : 0.3
                            color: getBackgroundColor()
                        }

                        onClicked: {
                            controlRevision.ListView.view.currentIndex = controlRevision.indexOfThisDelegate;
                        }

                        contentItem: Item {
                            RowLayout {
                                Rectangle {
                                    color:"transparent"
                                    Layout.minimumHeight: 72
                                    Layout.minimumWidth: 40
                                    Layout.maximumHeight: 72
                                    Layout.maximumWidth: 40
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignHCenter

                                    Image {
                                        x: 16
                                        id: imgRevision
                                        width: 24
                                        height: 24
                                        anchors.verticalCenter: parent.verticalCenter
                                        source: "../icons/git.png"
                                    }
                                }


                                ColumnLayout {
                                    Layout.leftMargin: 32
                                    Text {

                                        height: controlRevision.height
                                        Layout.preferredWidth: controlRevision.width - imgRevision.width-imgRevision.x - 40 - 32 - 10

                                        text: controlRevision.text
                                        horizontalAlignment: Text.AlignVCenter
                                        font.bold: false
                                        font.family: "Roboto"
                                        font.pixelSize: 16
                                        color: "#de000000"
                                    }

                                    Text {
                                        height: controlRevision.height
                                        Layout.preferredWidth: controlRevision.width - imgRevision.width-imgRevision.x - 40 - 32 - 10

                                        text: dateOfThisDelegate
                                        horizontalAlignment: Text.AlignVCenter
                                        font.bold: false
                                        font.family: "Roboto"
                                        font.pixelSize: 14
                                        color: "#99000000"
                                    }
                                }

                                Rectangle {
                                    color:"transparent"
                                    Layout.minimumHeight: 72
                                    Layout.minimumWidth: 40
                                    Layout.maximumHeight: 72
                                    Layout.maximumWidth: 40
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignHCenter

                                    Rectangle {
                                        id: imgRevisionDetailsHover
                                        width: 35
                                        height: 35
                                        radius: 35
                                        x:0
                                        anchors.verticalCenter: parent.verticalCenter
                                        color:"transparent"
                                        Image {
                                            id: imgRevisionDetails
                                            width: 24
                                            height: 24
                                            anchors.centerIn: parent
                                            source: "../icons/details.png"
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            onEntered: {imgRevisionDetailsHover.color = backgroundColorHoverNested}
                                            onExited: {imgRevisionDetailsHover.color = "transparent"}

                                        }

                                    }


                                }
                            }
                        }

                    }

                    headerPositioning: ListView.OverlayHeader
                    clip: true

                    header: Component {
                        Column {
                            z:100
                            Rectangle {
                                z:100
                                width:menuViewRevision.width
                                height:60
                                color: root.headerBackgroundColor
                                Text {
                                    anchors.fill: parent
                                    text: "Revision"
                                    font.family: "Concert One"
                                    font.weight: Font.Light
                                    font.letterSpacing: -1.5
                                    font.pointSize: 16
                                    color: root.headerFontColor
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }
                    } /* header */
                } /* ListView */
            } /* revisionPane */
        } /* RowLayout Lists */


        /*
        Rectangle {
            id:comboHeader
            Layout.leftMargin: 24//listRow.leftMargin
            Layout.preferredWidth: versionPane.width + revisionPane.width + listRow.spacing
            Layout.minimumWidth: versionPane.width + productPane.width + listRow.spacing
            Layout.maximumWidth: versionPane.width + productPane.width + listRow.spacing
            Layout.preferredHeight:60
            Layout.topMargin: 10
            color: Material.color(root.primaryColor, Material.Shade700)
            Text {
                anchors.fill: parent
                text: "Revision"
                font.family: "Concert One"
                font.weight: Font.Light
                font.letterSpacing: -1.5
                font.pointSize: 16
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }


        ComboBox {
            id: comboRevision
            property string contentText;
            property string contentDate;
            Layout.leftMargin: 24//listRow.leftMargin
            //Layout.minimumWidth: versionPane.width + revisionPane.width + productPane.width + listRow.spacing*2
            Layout.minimumWidth: comboHeader.width
            Layout.preferredWidth: comboHeader.width
            Layout.maximumWidth: comboHeader.width
            model: station.getRevisionModel()
            textRole: "name"

            onCurrentIndexChanged: {
                comboRevision.contentText = comboRevision.model.getName(comboRevision.currentIndex);
                comboRevision.contentDate = comboRevision.model.getDate(comboRevision.currentIndex);
            }

            //displayText: comboRevision.currentText + " ("  + comboRevision.indicator.indexOfThisDelegate + ")"
            contentItem: Text {
                RowLayout {
                    anchors.fill: parent
                    Text {
                        leftPadding: 16
                        Layout.fillHeight: true
                        Layout.minimumWidth: 40
                        text: comboRevision.contentText
                        font.family: "roboto"
                        font.pixelSize: 16
                        color: "#de000000"
                        verticalAlignment: Text.AlignVCenter
                    }
                    Text {
                        leftPadding: 16
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        text: comboRevision.contentDate;
                        font.family: "roboto"
                        font.pixelSize: 14
                        color: "#99000000"
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }

            delegate: Rectangle {
                property int indexOfThisDelegate: index;
                property string currentText: name;

                id: comboItem
                width: parent.width
                height: 22+8

                RowLayout {
                    anchors.fill: parent
                    Text {
                        leftPadding: 16
                        Layout.fillHeight: true
                        Layout.minimumWidth: 40
                        text: name
                        font.family: "roboto"
                        font.pixelSize: 16
                        color: comboRevision.currentIndex===index ? Material.color(root.primaryColor): "#de000000"
                        verticalAlignment: Text.AlignVCenter
                    }
                    Text {
                        leftPadding: 16
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        text: date
                        font.family: "roboto"
                        font.pixelSize: 14
                        color: comboRevision.currentIndex===index ? Material.color(root.primaryColor): "#99000000"
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: { comboItem.color = Material.color(Material.Grey, Material.Shade200)}
                    onExited: { comboItem.color = "white"}
                    onClicked: {comboRevision.currentIndex = indexOfThisDelegate; comboRevision.popup.close()}
                }
            }

        }
        */

        RowLayout {
            Layout.topMargin: 24
            Layout.leftMargin: 24//listRow.leftMargin
            Layout.rightMargin: 8//listRow.rightMargin
            Layout.minimumWidth: versionPane.width + productPane.width + revisionPane.width + listRow.spacing*2
            Layout.maximumWidth: versionPane.width + productPane.width + revisionPane.width + listRow.spacing*2
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: btnSelect.height
                color: "transparent"
            }
            Button {
                id: btnSelect
                Material.accent: Material.color(root.secondaryColor)
                highlighted: true
                text: qsTr("auswählen")
                onClicked: {
                    productSelected(menuViewProduct.currentItem.text, menuViewVersion.currentItem.text, menuViewRevision.currentItem.text);
                }
            }
        } /* RowLayout button */
    } /* ColumnLayout */


}
