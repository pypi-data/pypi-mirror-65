import QtQuick 2.0

Item {
    id: root
    property int finalRadius: 50
    property color circleColor: "green"
    property real replayFactor: 1

    function animate () {
        canvas.progress = 0;
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
            property real progress : 0;

            onProgressChanged: requestPaint()

            //renderTarget: Canvas.FramebufferObject
            //renderStrategy: Canvas.Cooperative

            onPaint: {

                var ctx = getContext('2d')
                ctx.resetTransform()
                ctx.fillStyle = 'rgba(255, 255, 255, 0)'
                ctx.fillRect(0, 0, width, height)

                var left = width * 0.25
                var right = width * 0.75
                var vCenter = height * 0.5
                var vDelta = height / 6

                ctx.lineCap = "round"
                ctx.lineWidth = vDelta * 0.3
                ctx.strokeStyle = 'white'


                ctx.beginPath()

                var x = circle.x
                if (x < 0)
                    x = 0
                var y = circle.x
                if (y < 0)
                    y = 0
                var mx =  width/2
                var my =  height/2

                var points = [[mx-circle.radius/2, my],
                              [mx-circle.radius/10,my + circle.radius/3],
                              [mx+(circle.radius/2),my - (circle.radius/3)]
                              ];


                var completeLength = 0;
                var i;
                var dx = 0;
                var dy = 0;

                for (i = 0; i < points.length-1; i++) {
                    dy = points[i+1][1] - points[i][1];
                    dx = points[i+1][0] - points[i][0];
                    var len = Math.sqrt(Math.pow(dx,2)+Math.pow(dy,2))
                    completeLength+=len;


                }

                completeLength = canvas.progress*completeLength;

                var drawedLength = 0;
                for (i = 0; i < points.length-1; i++) {
                    //console.log("idx=",i, "start from=", points[i][0], points[i][1])

                    ctx.moveTo(points[i][0], points[i][1]);
                    dy = points[i+1][1] - points[i][1];
                    dx = points[i+1][0] - points[i][0];
                    var angle  = Math.atan2(dy,dx)
                    var length = Math.sqrt(Math.pow(dx,2)+Math.pow(dy,2))
                    if ((length + drawedLength) > completeLength)
                        length = completeLength-drawedLength;

                    dx = Math.cos(angle)*length;
                    dy = Math.sin(angle)*length;

                    //console.log("paint to=", points[i][0]+dx, points[i][1]+dy, angle, length, dx, dy, drawedLength)

                    ctx.lineTo(points[i][0]+dx, points[i][1]+dy);

                    drawedLength+=length;

                    if (drawedLength >= completeLength)
                        break
                }

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
                    property: "progress";
                    easing.type: Easing.OutQuart;
                    duration: 700/replayFactor;
                    from:0;
                    to: 1;
                }

            }

        }
    }



}
