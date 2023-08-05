import QtQuick 2.0

Item {
    id: root
    property int finalRadius: 50
    property real finalCrossRatio: 0.6
    property color circleColor: "red"
    property real replayFactor: 1

    function animate () {
        canvas.lineLength = 0;
        mainAnimation.start()
    }

    Rectangle {
        id: circle
        color:circleColor
        radius: 0
        width: radius*2
        height: radius*2
        x: 0
        y: 0

        property int dx: root.finalRadius
        property int dy: root.finalRadius

        onRadiusChanged: recalcXY()

        function recalcXY () {
            circle.x = dx - radius
            circle.y = dy - radius
        }


        Canvas {
            id: canvas
            anchors.fill: parent
            property real lineLength : 0;

            onLineLengthChanged: requestPaint()

            onPaint: {

                var ctx = getContext('2d')
                ctx.resetTransform()
                ctx.fillStyle = 'rgba(255, 255, 255, 0)'
                ctx.fillRect(0, 0, width, height)

                var vDelta = height / 6

                ctx.lineCap = "round"
                ctx.lineWidth = vDelta * 0.3


                ctx.strokeStyle = 'white'


                ctx.beginPath()
                var x = circle.x
                if (x < 0)
                    x = 0
                var y = circle.y
                if (y < 0)
                    y = 0
                var mx =  width/2
                var my =  height/2



                ctx.moveTo(mx, my)
                var angle = 45;
                var factor = Math.sin(Math.PI/180*angle)
                var ll = circle.radius * lineLength*factor
                if (ll < 0)
                    ll = 0
                ctx.lineTo(mx + ll, my + ll)
                ctx.moveTo(mx, my)
                ctx.lineTo(mx + ll, my - ll)
                ctx.moveTo(mx, my)
                ctx.lineTo(mx - ll, my - ll)
                ctx.moveTo(mx, my)
                ctx.lineTo(mx - ll, my + ll)
                ctx.stroke()
            }
        }

        ParallelAnimation {
            id: mainAnimation

            PropertyAnimation {
                target: circle
                id: circleAnimation
                property: "radius";
                easing.type: Easing.OutQuad;
                duration: 600/replayFactor;
                from:0;
                to: finalRadius;
            }

            SequentialAnimation {

                PauseAnimation { duration: 200/replayFactor }

                PropertyAnimation {
                    target: canvas
                    id: lineAnimation
                    property: "lineLength";
                    easing.type: Easing.OutQuart;
                    duration: 700/replayFactor;
                    from:0;
                    to: finalCrossRatio;
                }

            }

        }
    }



}
