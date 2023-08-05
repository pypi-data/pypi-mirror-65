import QtQuick 2.0

ListModel {
    ListElement {
        name: "Dashboard"
        iconName: "icons/dashboard.png"
        iconNameSelected: "icons/dashboard_white.png"
        menuTitle: "Dashboard"
        section: "Produktion"
        source: "Dashboard/Dashboard.qml"
        role: "PRODUCTION,MANAGER"
    }
    ListElement {
        name: "Rüsten"
        iconName: "icons/import.png"
        iconNameSelected: "icons/import_white.png"
        menuTitle: "Produkt rüsten"
        section: "Produktion"
        source: "ProductRun/ProductEquip.qml"
        role: "PRODUCTION"
    }
    ListElement {
        name: "Ändern"
        iconName: "icons/change.png"
        iconNameSelected: "icons/change_white.png"
        menuTitle: "Produkt ändern"
        section: "Produkt"
        source: "Dashboard/Dashboard.qml"
        role: "PRODUCTION"
    }
    ListElement {
        name: "Erstellen"
        iconName: "icons/create.png"
        iconNameSelected: "icons/create_white.png"
        menuTitle: "Produkt erstellen"
        section: "Produkt"
        source: "Dashboard/Dashboard.qml"
        role: "PRODUCTION"
    }
    ListElement {
        name: "Exportieren"
        iconName: "icons/export.png"
        iconNameSelected: "icons/export_white.png"
        menuTitle: "Daten exportieren"
        section: "Reports"
        source: "Dashboard/Dashboard.qml"
        role: "PRODUCTION,MANAGER"
    }
    ListElement {
        name: "Installation"
        iconName: "icons/install.png"
        iconNameSelected: "icons/install_white.png"
        menuTitle: "Installation"
        section: "Sonstiges"
        source: "Installation.qml"
        role: "PRODUCTION,MANAGER"
    }
}
