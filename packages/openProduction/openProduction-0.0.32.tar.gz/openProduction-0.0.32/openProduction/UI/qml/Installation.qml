import QtQuick 2.0

Item {

    property string primaryColor: Material.Red;
    property string secondaryColor: Material.Green;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);

    signal disableScreen(bool visible);
    signal toggleSideMenu;

    Rectangle {
        //anchors.centerIn: parent
        x:0
        y:0
        width: 200
        height: 200
        color:"yellow"

        Text {
            text: "Installation.qml"
        }
    }

}
