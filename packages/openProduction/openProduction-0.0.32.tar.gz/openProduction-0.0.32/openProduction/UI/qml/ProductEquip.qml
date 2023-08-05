import QtQuick 2.0
import "ProductChoose"

Item {
    id: root
    anchors.fill: parent

    property string primaryColor: Material.Red;
    property string secondaryColor: Material.Green;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);

    QtObject {
        id: internal
        property bool _productLoaded: false;
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
        }
    }

    function onProductStationLoadCompleted () {
        productLoad.source = "TestRunnerSimple/TestRunnerSimple.qml"
    }

    Component.onDestruction: {
        if (internal._productLoaded)
        {
            productLoad.source = "TestRunnerSimple/TestRunnerSimple.qml"
            root.disableScreen(false);
        }
    }

    ProductChoose {
        id: productChoose
        anchors.fill: parent
        onProductSelected: {
            station.loadProduct(productName, productVersion, productRevision);
            station.productStationLoadCompleted.connect(root.onProductStationLoadCompleted)
        }
    }

    Loader {
        /* overlay for "loading" product (HW probing etc...) */
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
            root.disableScreen(true);
        }
    }

    Loader {
        /* overlay for "running" product (...) */
        id: productRun

        onLoaded: {

        }
    }
}
