import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import "../ProductChoose"

Item {
    id: root
    anchors.fill: parent

    property string primaryColor: Material.Red;
    property string secondaryColor: Material.Green;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);

    QtObject {
        id: internal
        property bool _productLoaded: false;
        property string productName;
        property string productVersion;
        property string productRevision;
    }

    signal disableScreen(bool visible);
    signal toggleSideMenu;

    function onProductLoadComplete(success) {
        root.disableScreen(false);


        productLoad.source = "";

        if (success && internal._productLoaded===false)
        {
            productChoose.visible = false;
            internal._productLoaded = true;
            toggleSideMenu();
            productRun.source = "ProductRun.qml"
        }
    }

    function onProductStationLoadCompleted () {
        if (station.getLoadedProduct() === null)
            console.log("product is null")
        else
        {
            productLoad.source = "../TestRunnerSimple/TestRunnerSimple.qml"
        }
    }

    Component.onDestruction: {
        if (internal._productLoaded)
        {
            productLoad.source = "../TestRunnerSimple/TestRunnerSimple.qml"
            root.disableScreen(false);
        }
    }

    ProductChoose {
        id: productChoose
        anchors.fill: parent
        onProductSelected: {
            internal.productName = productName;
            internal.productVersion = productVersion;
            internal.productRevision = productRevision;
            station.loadProduct(productName, productVersion, productRevision);
            station.productStationLoadCompleted.connect(root.onProductStationLoadCompleted)
        }
    }


    Loader {
        // overlay for "loading" product (HW probing etc...)
        id: productLoad

        onLoaded: {
            productLoad.item.testRunnerFinished.connect(onProductLoadComplete)
            if (internal._productLoaded)
                productLoad.item.runnerType = "unload"
            else
                productLoad.item.runnerType = "load"
            productLoad.item.runner = station.getLoadedProduct()
            productLoad.item.primaryColor = root.primaryColor;
            productLoad.item.secondaryColor = root.secondaryColor;
            productLoad.item.backgroundColor = root.backgroundColor;
            productLoad.item.footerText = internal.productName + " - " + internal.productVersion + " - Revision " + internal.productRevision
            productLoad.item.title = qsTr("Produkt rüsten");
            root.disableScreen(true);
        }
    }


    Loader {
        /* overlay for "running" product (...) */
        id: productRun
        anchors.fill: parent
        onStatusChanged: {contentLoader.item.opacity=0; if (contentLoader.status === Loader.Ready) {opacityLoader.start();}}

        onLoaded: {
            productRun.item.primaryColor = root.primaryColor;
            productRun.item.secondaryColor = root.secondaryColor;
            productRun.item.backgroundColor = root.backgroundColor;
            productRun.item.testSuite = station.getLoadedProduct();
            if (productRun.item.testSuite !== null)
                productRun.item.testSuite.enaCliRunner();
        }
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
