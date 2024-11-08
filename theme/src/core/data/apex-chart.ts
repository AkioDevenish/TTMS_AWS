import { monthDataSeries, chartDatas } from "@/core/data/chart-data"
var secondary = localStorage.getItem('secondary_color') || "#48A3D7";
var primary = localStorage.getItem('primary_color') || "#7A70BA";

export const series = [
    {
        name: "STOCK ABC",
        data: monthDataSeries[0].prices,
    },
]
export const series1 = [
    {
        name: 'series1',
        data: [31, 40, 28, 51, 42, 109, 100]
    }, {
        name: 'series2',
        data: [11, 32, 45, 32, 34, 52, 41]
    }
]
export const series2 = [
    {
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }
]
export const series3 = [
    {
        name: 'Net Profit',
        data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
    }, {
        name: 'Revenue',
        data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
    }, {
        name: 'Free Cash Flow',
        data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
    }
]
export const series4 = [
    {
        name: "Bubble1",
        data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
            min: 10,
            max: 60,
        }),
    },
    {
        name: "Bubble2",
        data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
            min: 10,
            max: 60,
        }),
    },
    {
        name: "Bubble3",
        data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
            min: 10,
            max: 60,
        }),
    },
    {
        name: "Bubble4",
        data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
            min: 10,
            max: 60,
        }),
    },
]
export const series5 = [
    {
        data: [34, 44, 54, 21, 12, 43, 33, 23, 66, 66, 58],
    },
]
export const series7 = [
    {
        name: "STOCK ABC",
        data: monthDataSeries[0].prices,
    },
]
export const series6 = [
    44, 55, 13, 43, 22
]
export const series8 = [44, 55, 41, 17, 15]
export const series9 = [
    {
        name: "Column",
        type: "column",
        data: [23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30],
    },
    {
        name: "Area",
        type: "area",
        data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43],
    },
    {
        name: "Line",
        type: "line",
        data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39],
    },
]
export const series10 = [{
    data: chartDatas
}
]
export const series11 = [
    {
        name: 'Series 1',
        data: [20, 100, 40, 30, 50, 80, 33],
    },
]
export const series12 = [44, 55, 67, 83]

export const chartOptions = {
    chart: {
        height: 350,
        type: "area",
        zoom: {
            enabled: false,
        },
        toolbar: {
            show: false,
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        curve: "straight",
    },
    title: {
        text: "Fundamental Analysis of Stocks",
        align: "left",
    },
    subtitle: {
        text: "Price Movements",
        align: "left",
    },
    labels: monthDataSeries[0].dates,
    xaxis: {
        type: "datetime",
    },
    yaxis: {
        opposite: true,
    },
    legend: {
        horizontalAlign: "left",
    },
    colors: [primary],
}
export const chartOptions1 = {
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    xaxis: {
        type: 'datetime',
        categories: ["2018-09-19T00:00:00", "2018-09-19T01:30:00", "2018-09-19T02:30:00", "2018-09-19T03:30:00", "2018-09-19T04:30:00", "2018-09-19T05:30:00", "2018-09-19T06:30:00"],
    },
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
    colors: [primary, secondary]
}
export const chartOptions2 = {
    chart: {
        height: 350,
        type: 'bar',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    series: [{
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }],
    xaxis: {
        categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan', 'United States', 'China', 'Germany'],
    },
    colors: [primary]
}
export const chartOptions3 = {
    chart: {
        height: 350,
        type: 'bar',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            endingShape: 'rounded',
            columnWidth: '55%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
    },
    yaxis: {
        title: {
            text: '$ (thousands)'
        }
    },
    fill: {
        opacity: 1

    },
    tooltip: {
        y: {
            formatter: function (val: number) {
                return "$ " + val + " thousands"
            }
        }
    },
    colors: [primary, secondary, '#51bb25']
}
export const chartOptions4 = {
    chart: {
        height: 350,
        type: "bubble",
        toolbar: {
            show: false,
        },
    },
    dataLabels: {
        enabled: false,
    },

    fill: {
        type: "gradient",
    },
    title: {
        text: "3D Bubble Chart",
    },
    xaxis: {
        tickAmount: 12,
        type: "datetime",

        labels: {
            rotate: 0,
        },
    },
    yaxis: {
        max: 70,
    },
    theme: {
        palette: "palette2",
    },
    stroke: {
        width: 0,
    },
    colors: [
        primary,
        secondary,
        "#51bb25",
        "#f8d62b",
    ],
}
export const chartOptions5 = {
    chart: {
        type: "line",
        height: 350,
        toolbar: {
            show: false,
        },
    },
    stroke: {
        curve: "stepline",
    },
    dataLabels: {
        enabled: false,
    },
    title: {
        text: "Stepline Chart",
        align: "left",
    },
    markers: {
        hover: {
            sizeOffset: 4,
        },
    },
    colors: [primary],
}
export const chartOptions7 = {
    annotations: {
        yaxis: [
            {
                y: 8200,
                borderColor: "#00E396",
                label: {
                    borderColor: "#00E396",
                    style: {
                        color: "#fff",
                        background: "#00E396",
                    },
                    text: "Support",
                },
            },
            {
                y: 8600, y2: 9000,
                borderColor: "#000", fillColor: "#FEB019",
                opacity: 0.2,
                label: {
                    borderColor: "#333",
                    style: {
                        fontSize: "10px",
                        color: "#333",
                        background: "#FEB019",
                    },
                    text: "Y-axis range",
                },
            },
        ],
        xaxis: [
            {
                x: new Date("23 Nov 2017").getTime(),
                strokeDashArray: 0,
                borderColor: "#775DD0",
                label: {
                    borderColor: "#775DD0",
                    style: {
                        color: "#fff", background: "#775DD0",
                    },
                    text: "Anno Test",
                },
            },
            {
                x: new Date("26 Nov 2017").getTime(),
                x2: new Date("28 Nov 2017").getTime(),
                fillColor: "#B3F7CA",
                opacity: 0.4,
                label: {
                    borderColor: "#B3F7CA",
                    style: {
                        fontSize: "10px",
                        color: "#fff", background: "#00E396",
                    },
                    offsetY: -10, text: "X-axis range",
                },
            },
        ],
        points: [
            {
                x: new Date("01 Dec 2017").getTime(),
                y: 8607.55,
                marker: {
                    size: 8,
                    fillColor: "#fff",
                    strokeColor: "red",
                    radius: 2, cssClass: "apexcharts-custom-class",
                },
                label: {
                    borderColor: "#FF4560",
                    offsetY: 0,
                    style: {
                        color: "#fff", background: "#FF4560",
                    },
                    text: "Point Annotation",
                },
            },
        ],
    },
    chart: {
        height: 350,
        type: "line",
        id: "areachart-2",
        toolbar: {
            show: false,
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        curve: "straight",
    },
    grid: {
        padding: {
            right: 30,
            left: 20,
        },
    },
    labels: monthDataSeries[0].dates,
    title: {
        text: "Line with Annotations",
        align: "left",
    },
    xaxis: {
        type: "datetime",
    },
    colors: [primary],
}
export const chartOptions6 = {
    chart: {
        width: 380,

        type: "pie",
    },
    labels: ["Team A", "Team B", "Team C", "Team D", "Team E"],

    colors: [
        primary,
        secondary,
        "#51bb25",
        "#a927f9",
        "#f8d62b",
    ],
}
export const chartOptions8 = {
    chart: {
        width: 380,
        type: 'donut',
    },

    colors: ['#dc3545', '#f8d62b', primary, '#51bb25', '#a927f9']
}
export const chartOptions9 = {
    chart: {
        height: 350,
        type: "line",
        stacked: false,
        toolbar: {
            show: false,
        },
    },
    stroke: {
        width: [0, 2, 5],
        curve: "smooth",
    },
    plotOptions: {
        bar: {
            columnWidth: "50%",
        },
    },
    fill: {
        opacity: [0.85, 0.25, 1],
        gradient: {
            inverseColors: false,
            shade: "light",
            type: "vertical",
            opacityFrom: 0.85,
            opacityTo: 0.55,
            stops: [0, 100, 100, 100],
        },
    },
    labels: [
        "01/01/2003",
        "02/01/2003",
        "03/01/2003",
        "04/01/2003",
        "05/01/2003",
        "06/01/2003",
        "07/01/2003",
        "08/01/2003",
        "09/01/2003",
        "10/01/2003",
        "11/01/2003",
    ],
    markers: {
        size: 0,
    },
    xaxis: {
        type: "datetime",
    },
    yaxis: {
        min: 0,
    },
    tooltip: {
        shared: true,
        intersect: false,
        y: {
            formatter: function (y: number) {
                if (typeof y !== "undefined") {
                    return y.toFixed(0) + " views";
                }
                return y;
            },
        },
    },
    legend: {
        labels: {
            useSeriesColors: true,
        },
    },
    colors: [secondary, "#51bb25", primary],
}
export const chartOptions10 = {
    chart: {
        height: 350,
        type: 'candlestick',
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        candlestick: {
            colors: {
                upward: primary,
                downward: secondary
            }
        }
    },
    title: {
        text: 'CandleStick Chart',
        align: 'left'
    },
    xaxis: {
        type: 'datetime'
    },
    yaxis: {
        tooltip: {
            enabled: true
        }
    },
    colors: ['#000000']
}
export const chartOptions11 = {
    chart: {
        height: 350,
        type: 'radar',
        toolbar: {
            show: false
        }
    },
    labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    plotOptions: {
        radar: {
            size: 140,
            polygons: {
                strokeColor: '#e9e9e9',
                fill: {
                    colors: ['#f8f8f8', '#fff']
                }
            }
        }
    },
    title: {
        text: 'Radar with Polygon Fill'
    },
    colors: ['#FF4560'],
    markers: {
        size: 4,
        colors: ['#fff'],
        strokeColor: '#FF4560',
        strokeWidth: 2,
    },
    tooltip: {
        y: {
            formatter: function (val: number) {
                return val;
            },
        },
    },
    yaxis: {
        tickAmount: 7,
        labels: {
            formatter: function (val: number, i: number) {
                if (i % 2 === 0) {
                    return val;
                } else {
                    return "";
                }
            },
        },
    },
}
export const chartOptions12 = {
    chart: {
        height: 350,
        type: 'radialBar',
    },
    plotOptions: {
        radialBar: {
            dataLabels: {
                name: {
                    fontSize: '22px',
                },
                value: {
                    fontSize: '16px',
                },
                total: {
                    show: true,
                    label: 'Total',
                    formatter: function () {
                        return 249
                    }
                }
            }
        }
    },
    labels: ['Apples', 'Oranges', 'Bananas', 'Berries'],

    colors: [secondary, '#51bb25', '#f8d62b', primary]

}



export function generateData(baseval: number, count: number, yrange: any) {
    var i = 0;
    var series = [];
    while (i < count) {
        var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
        var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;
        series.push([baseval, y, z]);
        baseval += 86400000;
        i++;
    }
    return series;
}