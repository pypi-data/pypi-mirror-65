import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4
import QtCharts 2.3

Item {
    id: root

    property string primaryColor: Material.Red;
    property string secondaryColor: Material.Green;
    property string backgroundColor: Material.color(Material.Grey, Material.Shade50);

    signal disableScreen(bool visible);
    signal toggleSideMenu;

    Pane {
        id: productionSpeed
        Material.background: "white"
        Material.elevation: 6
        width: root.width/2
        height: root.height

        padding: 0

        ChartView {
            title: "Produktionszeiten über Revision"
            titleFont.family: "roboto"
            titleFont.pointSize: 16
            legend.font.family: "roboto"
            legend.font.pointSize: 10
            anchors.fill: parent
            antialiasing: true
            animationOptions: ChartView.AllAnimations
            LineSeries {
                axisX: ValueAxis {
                    min: 0
                    max: 6
                    tickCount: 7
                    labelFormat : "Rev: %d"
                }
                axisY: ValueAxis {
                    min: 0
                    max: 30
                }

                name: "Peco Rear"
                pointsVisible: true
                XYPoint { x: 0; y: 10 }
                XYPoint { x: 1; y: 10.1 }
                XYPoint { x: 2; y: 10.2 }
                XYPoint { x: 3; y: 10.0 }
                XYPoint { x: 4; y: 10.3 }
                XYPoint { x: 5; y: 15 }
                XYPoint { x: 6; y: 10.1 }
            }

            LineSeries {
                name: "Peco Stair"
                pointsVisible: true
                XYPoint { x: 0; y: 21 }
                XYPoint { x: 1; y: 20 }
                XYPoint { x: 2; y: 22 }
                XYPoint { x: 3; y: 21 }
                XYPoint { x: 4; y: 22 }
                XYPoint { x: 5; y: 21 }
                XYPoint { x: 6; y: 22 }
            }
        }
    }

    Pane {
        id: topProducts
        Material.background: "white"
        Material.elevation: 6
        width: root.width - productionSpeed.width - 20
        height: productionSpeed.height/2
        y:0
        x:productionSpeed.width+10
        padding: 0

        ChartView {
            id: chart
            title: "Top-5 Produkte"
            titleFont.family: "roboto"
            titleFont.pointSize: 16
            legend.font.family: "roboto"
            legend.font.pointSize: 10
            anchors.fill: parent
            legend.alignment: Qt.AlignBottom
            antialiasing: true
            animationOptions: ChartView.AllAnimations


            PieSeries {
                id: pieSeries
                PieSlice { label: "Bauernstolz"; value: 13.5 }
                PieSlice { label: "Peco Rear"; value: 10.9 }
                PieSlice { label: "Peco Stair"; value: 8.6 }
                PieSlice { label: "DTAGD"; value: 8.2 }
                PieSlice { label: "Peco Rear"; value: 6.8 }
            }

        }

    }

    Pane {
        id: productionErrors
        Material.background: "white"
        Material.elevation: 6
        width: root.width - productionSpeed.width - 20
        height: productionSpeed.height/2-10
        y:productionSpeed.height/2+10
        x:productionSpeed.width+10
        padding: 0

        ChartView {
            title: "Produktionsausfälle"
            anchors.fill: parent
            legend.alignment: Qt.AlignBottom
            antialiasing: true
            titleFont.family: "roboto"
            titleFont.pointSize: 16
            legend.font.family: "roboto"
            legend.font.pointSize: 10
            animationOptions: ChartView.AllAnimations

            BarSeries {
                id: mySeries
                axisX: BarCategoryAxis { categories: ["Peco Rear", "Peco Stair", "Bauernstolz", "DTAGD"]}
                BarSet { label: "Gut"; values: [150, 170, 120, 130]; color: "green" }
                BarSet { label: "Schlecht"; values: [15, 13, 10, 11]; color: "red" }
            }
        }
    }

}
