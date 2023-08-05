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
    property string text: "hello world, test 123"
    property string caption: ""

    Rectangle {
        id: header
        color: container.backgroundColor
        radius: 4
        height:30+20
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
        height:container.height-header.height+20
        width:container.width
        y:header.height+header.y-20
        x:0

        ScrollView {
            clip: true
            anchors.fill: parent

            TextArea  {
                id: textInput
                font.family: "Roboto"
                font.pointSize: 10
                x:5
                text: container.text
                wrapMode: TextArea.Wrap
                Material.accent: container.styleColor
                readOnly: true
                selectByMouse: true

                MouseArea {
                        property int selectStart;
                        property int selectEnd;
                        property int curPos;

                        anchors.fill: parent
                        acceptedButtons: Qt.RightButton
                        hoverEnabled: true
                        onClicked: {
                            selectStart = textInput.selectionStart;
                            selectEnd = textInput.selectionEnd;
                            curPos = textInput.cursorPosition;
                            contextMenu.x = mouse.x;
                            contextMenu.y = mouse.y;
                            contextMenu.open();
                            textInput.cursorPosition = curPos;
                            textInput.select(selectStart,selectEnd);
                        }
                        onPressAndHold: {
                            if (mouse.source === Qt.MouseEventNotSynthesized) {
                                selectStart = textInput.selectionStart;
                                selectEnd = textInput.selectionEnd;
                                curPos = textInput.cursorPosition;
                                contextMenu.x = mouse.x;
                                contextMenu.y = mouse.y;
                                contextMenu.open();
                                textInput.cursorPosition = curPos;
                                textInput.select(selectStart,selectEnd);
                            }
                        }

                        Menu {
                            id: contextMenu
                            MenuItem {
                                text: "Select all"
                                onTriggered: {
                                    textInput.selectAll()
                                }
                            }
                            MenuItem {
                                text: "Copy"
                                onTriggered: {
                                    textInput.copy()
                                }
                            }
                        }
                    }
            }

        }
    }
}
