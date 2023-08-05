import QtQuick 2.0
Canvas {
    id: canvas
    width: 48
    height: 48
    x:0
    y:0

    property color backgroundColor: "yellow"
    property color color: "white"

    property int animationDuration: 300
    property bool arrowFormState: true
    function toggle() { arrowFormState = !arrowFormState }

    property real angle: 180
    property real morphProgress: 1
    states: State {
        when: arrowFormState
        PropertyChanges { angle: 0; target: canvas }
        PropertyChanges { morphProgress: 0; target: canvas }
    }
    transitions: Transition {
        RotationAnimation {
            property: "angle"
            direction: RotationAnimation.Clockwise
            easing.type: Easing.InOutCubic
            duration: canvas.animationDuration
        }
        NumberAnimation {
            property: "morphProgress"
            easing.type: Easing.InOutCubic
            duration: canvas.animationDuration
        }
    }

    onAngleChanged: requestPaint()
    onMorphProgressChanged: requestPaint()

    //renderTarget: Canvas.FramebufferObject
    renderStrategy: Canvas.Cooperative

    onPaint: {
        var ctx = getContext('2d')
        // The context keeps its state between paint calls, reset the transform
        ctx.resetTransform()

        //ctx.fillStyle = canvas.backgroundColor
        ctx.clearRect(0, 0, width, height)

        // Rotate from the center
        ctx.translate(width / 2, height / 2)
        ctx.rotate(angle * Math.PI / 180)
        ctx.translate(-width / 2, -height / 2)

        var left = width * 0.25
        var right = width * 0.75
        var vCenter = height * 0.5
        var vDelta = height / 6

        // Use our cubic-interpolated morphProgress to extract
        // other animation parameter values
        function interpolate(first, second, ratio) {
            return first + (second - first) * ratio;
        };
        var vArrowEndDelta = interpolate(vDelta, vDelta * 1.25, morphProgress)
        var vArrowTipDelta = interpolate(vDelta, 0, morphProgress)
        var arrowEndX = interpolate(left, right - vArrowEndDelta, morphProgress)

        ctx.lineCap = "square"
        ctx.lineWidth = vDelta * 0.4
        ctx.strokeStyle = canvas.color
        var lineCapAdjustment = interpolate(0, ctx.lineWidth / 2, morphProgress)

        ctx.beginPath()
        ctx.moveTo(arrowEndX, vCenter - vArrowEndDelta)
        ctx.lineTo(right, vCenter - vArrowTipDelta)
        ctx.moveTo(left + lineCapAdjustment, vCenter)
        ctx.lineTo(right - lineCapAdjustment, vCenter)
        ctx.moveTo(arrowEndX, vCenter + vArrowEndDelta)
        ctx.lineTo(right, vCenter + vArrowTipDelta)
        ctx.stroke()
    }
}
