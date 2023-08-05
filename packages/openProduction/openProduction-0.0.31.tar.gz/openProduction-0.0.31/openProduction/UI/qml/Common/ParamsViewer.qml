import QtQuick 2.9
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0
import QtQuick.Controls.Material 2.2
import QtQuick.Controls.Styles 1.4

Item {
    id: root
    property QtObject model: null

    Rectangle {
        id: content
        anchors.fill: parent
        color: "white"

        ListView {
            anchors.fill: parent
            model: root.model
            delegate: Item {
                function getSourceComponent(key, value, type) {

                    renderType.propKey = key
                    renderType.propHasChanges = false
                    renderType.propValueType = type;

                    if (type === "BOOL") {
                        renderType.sourceComponent = boolParam
                        renderType.propValueBool = value
                    } else if (type === "INT" || type === "FLOAT") {
                        renderType.sourceComponent = numberParam
                        renderType.propValueInt = value
                        renderType.propValueDouble = value
                    }
                }

                Component.onCompleted: {
                    getSourceComponent(key, value, type)
                }

                width: 180
                height: 40
                Loader {
                    id: renderType
                    property string propValueType
                    property string propValueString
                    property bool propValueBool
                    property int propValueInt
                    property double propValueDouble
                    property string propKey
                    property bool propHasChanges: false
                    property color backgroundColor: Material.color(
                                                        Material.Grey,
                                                        Material.Shade300)
                    property color styleColor: Material.color(Material.Orange)
                }
            }
        }

        Component {
            id: boolParam

            Rectangle {
                width: childrenRect.width
                height: childrenRect.height
                color: "white"
                CheckBox {
                    height: 40
                    id: checkBox
                    text: propKey
                    checked: propValueBool
                    onCheckedChanged: {
                        if (root.model !== null)
                            root.model.keyChangedFromUI(text, checked, "BOOL")
                    }

                    style: CheckBoxStyle {
                        indicator: Rectangle {
                            implicitWidth: 16
                            implicitHeight: 16
                            radius: 3
                            border.color: control.activeFocus ? "darkblue" : "gray"
                            border.width: 1
                            Rectangle {
                                visible: control.checked
                                color: "#555"
                                border.color: "#333"
                                radius: 1
                                anchors.margins: 4
                                anchors.fill: parent
                            }
                        }
                        label: Text {
                            text: propKey
                            font.family: "Roboto"
                            font.pixelSize: 12
                            color: "#de000000"
                        }
                    }
                }
            }
        }

        Component {
            id: numberParam

            Item {
                id: container
                height: 36
                width: 300
                y: 4
                x: 0

                Rectangle {
                    id: header
                    color: "white"

                    radius: 4
                    height: container.height - y
                    width: container.width
                    border.width: 2
                    border.color: Material.color(Material.Orange)
                    y: 8
                    x: 0
                    Rectangle {
                        color: "white"
                        y: -8
                        x: 7
                        Text {
                            id: helperText
                            text: "  " + propKey + "  "
                            font.family: "Roboto"
                            font.pointSize: 8
                            font.bold: true
                            color: Material.color(Material.Orange)
                        }

                        width: childrenRect.width
                        height: childrenRect.height
                    }

                    Rectangle {
                        color: "transparent"
                        radius: 0
                        height: container.height - helperText.height
                        width: container.width
                        y: helperText.height + helperText.y-10
                        x: 5

                        RowLayout {
                            anchors.fill: parent
                            Text {
                                Layout.preferredWidth: 10
                                Layout.maximumWidth: 10
                                Layout.minimumWidth: 10
                                text: (propHasChanges === true) ? "*" : ""
                                font.family: "Roboto"
                                font.pixelSize: 12
                                color: "#99000000"
                            }

                            DoubleValidator {
                                id: validatorDouble
                            }

                            IntValidator {
                                id: validatorInt
                            }

                            TextInput {
                                Layout.fillWidth: true
                                id: inputText
                                text: (propValueType==="FLOAT") ? propValueDouble : propValueInt;
                                font.family: "Roboto"
                                font.pixelSize: 12
                                color: "#de000000"
                                validator: (propValueType==="FLOAT") ? validatorDouble : validatorInt;
                                focus: true

                                onEditingFinished: {
                                    if (root.model !== null) {
                                        root.model.keyChangedFromUI(propKey,
                                                                    text, propValueType)
                                    }
                                    propHasChanges = false
                                }
                                onTextEdited: {
                                    propHasChanges = true
                                }
                            }
                        }
                    } /* rectangle */
                }
            }

        }
    }
}
