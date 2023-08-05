import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2

Item {
    id: container
    height:100
    width:300
    y:0
    x:0
    property color backgroundColor: Material.color(Material.Grey, Material.Shade300);
    property color styleColor: Material.color(Material.Orange)
    property string text: ""
    property string caption: ""

    Rectangle {
        id: header
        color: container.backgroundColor
        radius: 4
        height:30
        width:container.width
        y:0
        x:0
        Text {
            y: 5
            x: 5

            text: container.caption
            font.family: "Roboto"
            font.pointSize: 8
            color: container.styleColor

        }
    }

    Rectangle {
        color: container.backgroundColor
        radius: 0
        height:container.height-header.height-10
        width:container.width
        y:header.height-10
        x:0

        ScrollView {
            clip: true
            anchors.fill: parent
            TextArea  {
                font.family: "Roboto"
                font.pointSize: 10
                x:5
                text: container.text
                wrapMode: TextArea.Wrap
                Material.accent: container.styleColor
                readOnly: true
                selectByMouse: true
            }

        }
    }
}
