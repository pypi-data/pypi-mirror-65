import QtQuick 2.0

Item {
    anchors.fill: parent
    id: root

    property color titleBarColor: "blue"
    property string title: "MyApp"

    // Declare properties that will store the position of the mouse cursor
    property int previousX
    property int previousY

    Rectangle {
        id: titleBar
        width:parent.width
        height:15
        x:0
        y:0
        color: root.titleBarColor

        Text {
            id: titleText
            text: root.title
            //font.family: "Roboto"
            font.pointSize: 8
            y:0
            x:5
            color:"white"
        }
    }

    Rectangle {
        id:minimize
        color:"green"
        x:parent.width-5-width-15*2
        y:0
        width:15
        height:15

        MouseArea {
            anchors.fill: parent
            onClicked: {
                mainWindow.visibility = "Minimized"
            }
        }
    }

    Rectangle {
        id:maximize
        color:"yellow"
        x:parent.width-5-width-15
        y:0
        width:15
        height:15

        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (mainWindow.visibility === 4)
                    mainWindow.visibility = "Windowed"
                else
                    mainWindow.visibility = "Maximized"
            }
        }
    }

    Rectangle {
        id:close
        color:"red"
        x:parent.width-5-width
        y:0
        width:15
        height:15

        MouseArea {
            anchors.fill: parent
            onClicked: {
                mainWindow.close()
            }
        }
    }

    MouseArea {
        id: topLeftArea
        height: 5
        x:0
        y:0
        width: 5


        // We set the shape of the cursor so that it is clear that this resizing
        cursorShape: Qt.SizeFDiagCursor

        onPressed: {
            // We memorize the position along the Y axis
            previousX = mouseX
            previousY = mouseY
        }

        // When changing a position, we recalculate the position of the window, and its height
        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setY(mainWindow.y + dy)
            mainWindow.setHeight(mainWindow.height - dy)
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setX(mainWindow.x + dx)
            mainWindow.setWidth(mainWindow.width - dx)
        }
    }

    MouseArea {
        id: topArea
        height: 5
        x:5
        y:0
        width: parent.width-10


        // We set the shape of the cursor so that it is clear that this resizing
        cursorShape: Qt.SizeVerCursor

        onPressed: {
            // We memorize the position along the Y axis
            previousY = mouseY
        }

        // When changing a position, we recalculate the position of the window, and its height
        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setY(mainWindow.y + dy)
            mainWindow.setHeight(mainWindow.height - dy)
        }
    }

    MouseArea {
        id: topRightArea
        height: 5
        x:parent.width-5
        y:0
        width: 5


        // We set the shape of the cursor so that it is clear that this resizing
        cursorShape: Qt.SizeBDiagCursor

        onPressed: {
            // We memorize the position along the Y axis
            previousX = mouseX
            previousY = mouseY
        }

        // When changing a position, we recalculate the position of the window, and its height
        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setY(mainWindow.y + dy)
            mainWindow.setHeight(mainWindow.height - dy)
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setWidth(mainWindow.width + dx)
        }

    }


    // Similar calculations for the remaining three areas of resize
    MouseArea {
        id: bottomArea
        height: 5
        x:5
        y: parent.height-5
        width: parent.width-10

        cursorShape: Qt.SizeVerCursor

        onPressed: {
            previousY = mouseY
        }

        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setHeight(mainWindow.height + dy)
        }
    }

    MouseArea {
        id: bottomLeftArea
        height: 5
        x:0
        y:parent.height-5
        width: 5


        // We set the shape of the cursor so that it is clear that this resizing
        cursorShape: Qt.SizeBDiagCursor

        onPressed: {
            // We memorize the position along the Y axis
            previousX = mouseX
            previousY = mouseY
        }

        // When changing a position, we recalculate the position of the window, and its height
        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setHeight(mainWindow.height + dy)
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setX(mainWindow.x + dx)
            mainWindow.setWidth(mainWindow.width - dx)
        }
    }

    MouseArea {
        id: leftArea
        width: 5
        height: parent.height-10
        y:5
        x:0

        cursorShape: Qt.SizeHorCursor

        onPressed: {
            previousX = mouseX
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setX(mainWindow.x + dx)
            mainWindow.setWidth(mainWindow.width - dx)
        }
    }

    MouseArea {
        id: bottomRightArea
        height: 5
        x:parent.width-5
        y:parent.height-5
        width: 5


        // We set the shape of the cursor so that it is clear that this resizing
        cursorShape: Qt.SizeFDiagCursor

        onPressed: {
            // We memorize the position along the Y axis
            previousX = mouseX
            previousY = mouseY
        }

        // When changing a position, we recalculate the position of the window, and its height
        onMouseYChanged: {
            var dy = mouseY - previousY
            mainWindow.setHeight(mainWindow.height + dy)
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setWidth(mainWindow.width + dx)
        }
    }

    MouseArea {
        id: rightArea
        width: 5
        height: parent.height-10
        x:parent.width-5
        y:5

        cursorShape:  Qt.SizeHorCursor

        onPressed: {
            previousX = mouseX
        }

        onMouseXChanged: {
            var dx = mouseX - previousX
            mainWindow.setWidth(mainWindow.width + dx)
        }
    }



    // The central area for moving the application window
    // Here you already need to use the position both along the X axis and the Y axis
    MouseArea {
        x:5
        width: parent.width-10-15*3
        y:5
        height:15
        property bool preventWinChange
        property int debounce : 0

        onPressed: {
            preventWinChange = false
            previousX = mouseX
            previousY = mouseY
        }

        onMouseXChanged: {
            if (preventWinChange === false) {
                var dx = mouseX - previousX
                mainWindow.setX(mainWindow.x + dx)
                //preventWinChange = true;
            }
        }

        onMouseYChanged: {
            if (preventWinChange === false) {
                var dy = mouseY - previousY
                mainWindow.setY(mainWindow.y + dy)
            }
        }

        onDoubleClicked: {
            preventWinChange = true
            if (mainWindow.visibility === 4)
                mainWindow.visibility = "Windowed"
            else
                mainWindow.visibility = "Maximized"
        }
    }
}
