import { monthDataSeries1, chartDatas } from "@/core/data/chart-data"
var primary = localStorage.getItem("primary_color") || "#7A70BA";
var secondary = localStorage.getItem("secondary_color") || "#48A3D7";
var trigoStrength = 3;
var iteration = 11;

export const series = [
    {
        name: "Active",
        data: [18, 50, 65, 18, 28, 70, 15, 35],
    },
    {
        name: "Bounce",
        data: [35, 70, 30, 60, 25, 45, 50, 50],
    },
]
export const series1 = [78]
export const series2 = [70]
export const series3 = [50]
export const series4 = [80]
export const series5 = [
    {
        data: [70, 60, 82, 80, 60, 90, 70, 120, 50, 60, 0],
    },
]

export const series6 = [
    {
        name: "series1",
        data: [70, 60, 82, 80, 60, 90, 70, 120, 50, 60, 0],
    },
]

export const series7 = [
    {
        data: [70, 60, 82, 80, 60, 90, 70, 120, 50, 60, 0],
    },
]
export const series8 = [
    {
        name: "Profit",
        data: [100, 50, 25, 50, 30, 50, 70],
    },
    {
        name: "Revenue",
        data: [70, 20, 55, 45, 35, 110, 85],
    },
    {
        name: "Cash Flow",
        data: [85, 55, 100, 35, 90, 60, 80],
    },
]
export const series9 = [90, 63, 50]
export const series10 = [
    {
        name: "Process 1",
        data: [44],
    },
]

export const series11 = [
    {
        name: "Dispatched",
        data: [40],
    },
]

export const series12 = [
    {
        name: "Reach Station",
        data: [50],
    },
]

export const series13 = [
    {
        name: "Out for delivery",
        data: [60],
    },
]

export const series14 = [
    {
        name: "Process 1",
        data: [44],
    },
]
export const series15 = [
    {
        name: "TEAM A",
        data: [50, 120, 90, 100, 70, 95, 40, 55, 30, 0],
    },
    {
        name: "TEAM B",
        data: [35, 60, 40, 90, 70, 110, 90, 120, 60, 0],
    },
]
export const series16 = [
    {
        data: [70, 60, 82, 80, 60, 90, 70, 120, 50, 60, 0],
    },
]
export const series17 = [
    {
        data: [
            20, 120, 15, 100, 120, 60, 150, 70, 100, 80, 105, 20, 70, 60, 10, 12,
            10, 130, 60, 80, 40, 140, 110, 150, 30, 75, 20, 45, 15, 130, 10, 30,
            15, 110, 65, 130, 0,
        ],
    },
]

export const series18 = [
    {
        data: monthDataSeries1[0].prices,
    },
]
export const series19 = [
    {
        name: "line",
        type: "line",
        data: [
            {
                x: new Date(1538778600000),
                y: 6550,
            },
            {
                x: new Date(1538782200000),
                y: 6560,
            },
            {
                x: new Date(1538814600000),
                y: 6640,
            },
            {
                x: new Date(1538884800000),
                y: 6560,
            },
        ],
    },
    {
        name: "candle",
        type: "candlestick",
        data: chartDatas
    },
]
export const series20 = [
    {
        name: "Load Average",
        type: 'column',
        data: generateMinuteWiseTimeSeries(
            new Date("12/12/2016 00:20:00").getTime(),
            12,
            {
                min: 10,
                max: 110,
            }
        ),
    },
    {
        name: 'Social Media',
        type: 'line',
        data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16]
    }
]
export const series21 = [
    {
        name: "Running",
        data: generateMinuteWiseTimeSeries(
            new Date("12/12/2016 00:20:00").getTime(),
            12,
            {
                min: 30,
                max: 110,
            }
        ),
    },
    {
        name: "Waiting",
        data: generateMinuteWiseTimeSeries(
            new Date("12/12/2016 00:20:00").getTime(),
            12,
            {
                min: 30,
                max: 110,
            }
        ),
    },
]
export const series22 = [
    {
        name: "Series 1",
        data: [80, 50, 30, 40, 100, 20],
    },
    {
        name: "Series 2",
        data: [20, 30, 40, 80, 20, 80],
    },
]
export const series23 = [
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
export const chartOptions = {
    chart: {
        type: "bar",
        height: 220,
        toolbar: {
            show: false,
        },
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: "50%",
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        show: true,
        width: 6,
        colors: ["transparent"],
    },
    grid: {
        show: true,
        borderColor: "var(--chart-border)",
        xaxis: {
            lines: {
                show: true,
            },
        },
    },
    colors: ["#48A3D7", "var(--theme-deafult)"],
    xaxis: {
        categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon"],
        tickAmount: 4,
        tickPlacement: "between",
        labels: {
            style: {
                fontFamily: "Rubik, sans-serif",
            },
        },
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        min: 0,
        max: 100,
        tickAmount: 5,
        tickPlacement: "between",
        labels: {
            style: {
                fontFamily: "Rubik, sans-serif",
            },
        },
    },
    fill: {
        opacity: 1,
    },
    legend: {
        position: "top",
        horizontalAlign: "left",
        fontFamily: "Rubik, sans-serif",
        fontSize: "14px",
        fontWeight: 500,
        labels: {
            colors: "var(--chart-text-color)",
        },
        markers: {
            width: 6,
            height: 6,
            radius: 12,
        },
        itemMargin: {
            horizontal: 10,
        },
    },
    responsive: [
        {
            breakpoint: 1366,
            options: {
                plotOptions: {
                    bar: {
                        columnWidth: "80%",
                    },
                },
                grid: {
                    padding: {
                        right: 0,
                    },
                },
            },
        },
        {
            breakpoint: 1200,
            options: {
                plotOptions: {
                    bar: {
                        columnWidth: "50%",
                    },
                },
                grid: {
                    padding: {
                        right: 0,
                    },
                },
            },
        },
        {
            breakpoint: 576,
            options: {
                plotOptions: {
                    bar: {
                        columnWidth: "60%",
                    },
                },
                grid: {
                    padding: {
                        right: 5,
                    },
                },
            },
        },
    ],
}
export const chartOptions1 = {
    chart: {
        height: 110,
        type: "radialBar",
        dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 10,
            color: "var(--theme-deafult)",
            opacity: 0.35,
        },
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: "60%",
            },
            track: {
                strokeWidth: "60%",
                opacity: 1,
                margin: 5,
            },
            dataLabels: {
                showOn: "always",
                value: {
                    color: "var(--body-font-color)",
                    fontSize: "14px",
                    show: true,
                    offsetY: -10,
                },
            },
        },
    },
    colors: ["var(--theme-deafult)"],
    stroke: {
        lineCap: "round",
    },
    responsive: [
        {
            breakpoint: 1500,
            options: {
                chart: {
                    height: 130,
                },
            },
        },
    ],

}
export const chartOptions2 = {
    chart: {
        height: 110,
        type: "radialBar",
        dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 10,
            color: "#FFA941",
            opacity: 0.35,
        },
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: "60%",
            },
            track: {
                strokeWidth: "60%",
                opacity: 1,
                margin: 5,
            },
            dataLabels: {
                showOn: "always",
                value: {
                    color: "var(--body-font-color)",
                    fontSize: "14px",
                    show: true,
                    offsetY: -10,
                },
            },
        },
    },
    colors: ["#FFA941"],
    stroke: {
        lineCap: "round",
    },
    responsive: [
        {
            breakpoint: 1500,
            options: {
                chart: {
                    height: 130,
                },
            },
        },
    ],
}
export const chartOptions3 = {
    chart: {
        height: 110,
        type: "radialBar",
        dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 10,
            color: "#57B9F6",
            opacity: 0.35,
        },
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: "60%",
            },
            track: {
                strokeWidth: "60%",
                opacity: 1,
                margin: 5,
            },
            dataLabels: {
                showOn: "always",
                value: {
                    color: "var(--body-font-color)",
                    fontSize: "14px",
                    show: true,
                    offsetY: -10,
                },
            },
        },
    },
    colors: ["#57B9F6"],
    stroke: {
        lineCap: "round",
    },
    responsive: [
        {
            breakpoint: 1500,
            options: {
                chart: {
                    height: 130,
                },
            },
        },
    ],
}
export const chartOptions4 = {
    chart: {
        height: 110,
        type: "radialBar",
        dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 10,
            color: "#48A3D7",
            opacity: 0.35,
        },
    },
    plotOptions: {
        radialBar: {
            hollow: {
                size: "60%",
            },
            track: {
                strokeWidth: "60%",
                opacity: 1,
                margin: 5,
            },
            dataLabels: {
                showOn: "always",
                value: {
                    color: "var(--body-font-color)",
                    fontSize: "14px",
                    show: true,
                    offsetY: -10,
                },
            },
        },
    },
    colors: ["#48A3D7"],
    stroke: {
        lineCap: "round",
    },
    responsive: [
        {
            breakpoint: 1500,
            options: {
                chart: {
                    height: 130,
                },
            },
        },
    ],
}
export const chartOptions5 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 200,
        type: "area",
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    xaxis: {
        show: false,
        type: "datetime",
        categories: [
            "2018-09-19T00:00:00",
            "2018-09-19T01:30:00",
            "2018-09-19T02:30:00",
            "2018-09-19T03:30:00",
            "2018-09-19T04:30:00",
            "2018-09-19T05:30:00",
            "2018-09-19T06:30:00",
            "2018-09-19T07:30:00",
            "2018-09-19T08:30:00",
            "2018-09-19T09:30:00",
            "2018-09-19T10:30:00",
        ],
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        labels: {
            show: false,
        },
    },
    grid: {
        show: false,
        padding: {
            left: -10, top: -25, right: -60, bottom: -40,
        },
    },
    fill: {
        opacity: 0.2,
    },
    colors: [primary],
    tooltip: {
        x: {
            format: "dd/MM/yy HH:mm",
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 100,
                }
            }
        }
    ]
}

export const chartOptions6 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 200,
        type: "area",
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    xaxis: {
        show: false,
        type: "datetime",
        categories: [
            "2018-09-19T00:00:00",
            "2018-09-19T01:30:00",
            "2018-09-19T02:30:00",
            "2018-09-19T03:30:00",
            "2018-09-19T04:30:00",
            "2018-09-19T05:30:00",
            "2018-09-19T06:30:00",
            "2018-09-19T07:30:00",
            "2018-09-19T08:30:00",
            "2018-09-19T09:30:00",
            "2018-09-19T10:30:00",
        ],
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        show: false
    },
    grid: {
        show: false,
        padding: {
            left: -10, top: -25, right: -60, bottom: -40,
        },
    },
    fill: {
        opacity: 0.2,
    },
    colors: [secondary],

    tooltip: {
        x: {
            format: "dd/MM/yy HH:mm",
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 100,
                }
            }
        }
    ]
}

export const chartOptions7 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 200,
        type: "area",
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    xaxis: {
        show: false,
        type: "datetime",
        categories: [
            "2018-09-19T00:00:00",
            "2018-09-19T01:30:00",
            "2018-09-19T02:30:00",
            "2018-09-19T03:30:00",
            "2018-09-19T04:30:00",
            "2018-09-19T05:30:00",
            "2018-09-19T06:30:00",
            "2018-09-19T07:30:00",
            "2018-09-19T08:30:00",
            "2018-09-19T09:30:00",
            "2018-09-19T10:30:00",
        ],
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    yaxis: {
        show: false
    },
    grid: {
        show: false,
        padding: {
            left: -10,
            top: -25,
            right: -60,
            bottom: -40,
        },
    },
    fill: {
        opacity: 0.2,
    },
    colors: ["#51bb25"],
    tooltip: {
        x: {
            format: "dd/MM/yy HH:mm",
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 100,
                }
            }
        }
    ]
}
export const chartOptions8 = {
    chart: {
        type: "bar",
        height: 380,
        toolbar: {
            show: false,
        },
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: "30%",
            endingShape: "rounded",
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        show: true,
        width: 1,
        colors: ["transparent"],
        curve: "smooth",
        lineCap: "butt",
    },
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        floating: false,
        axisTicks: {
            show: false,
        },
        axisBorder: {
            color: "#C4C4C4",
        },
    },
    yaxis: {
        title: {
            text: "Dollars in thounand",
            style: {
                fontSize: "14px",
                fontFamily: "Outfit', sans-serif",
                fontWeight: 500,
            },
        },
    },
    colors: [secondary, "#51bb25", primary],
    fill: {
        type: "gradient",
        gradient: {
            shade: "light",
            type: "vertical",
            shadeIntensity: 0.1,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.9,
            stops: [0, 100],
        },
    },
    tooltip: {
        y: {
            formatter: function (val: string) {
                return "$ " + val + " thousands";
            },
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 200,
                },
            },
        },
    ],
}
export const chartOptions9 = {
    chart: {
        type: "radialBar",
        height: 375,
        offsetY: -30,
        offsetX: 20,
    },
    plotOptions: {
        radialBar: {
            size: undefined,
            inverseOrder: false,
            hollow: {
                margin: 10,
                size: "30%",
                background: "transparent",
            },
            track: {
                show: true,
                background: "#f2f2f2",
                strokeWidth: "10%",
                opacity: 1,
                margin: 3,
            },
        },
    },
    labels: ["Skill 01", "Skill 02", "Skill 03"],
    legend: {
        show: true,
        fontSize: "16px",
        fontFamily: "Roboto, sans-serif",
        fontWeight: 500,
        labels: {
            colors: "#2C323F",
        },
        markers: {
            width: 86,
            height: 18,
            radius: 3,
        },
    },
    colors: [secondary, primary, "#51bb25"],
    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions10 = {
    chart: {
        height: 70,
        type: "bar",
        stacked: true,
        sparkline: {
            enabled: true,
        },
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: "15%",
            colors: {
                backgroundBarColors: [primary],
                backgroundBarOpacity: 0.2,
            },
        },
    },
    colors: [primary],
    stroke: {
        width: 0,
    },
    fill: {
        colors: [primary],
        type: "gradient",
        opacity: 1,
        gradient: {
            gradientToColors: [primary],
        },
    },
    title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: "Packed",
        style: {
            fontSize: "18px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 500,
        },
    },
    subtitle: {
        floating: true,
        align: "right",
        offsetY: 0,
        text: "44%",
        style: {
            fontSize: "14px",
        },
    },
    tooltip: {
        enabled: false,
    },
    xaxis: {
        categories: ["Packed"],
    },
    yaxis: {
        max: 100,
    },

    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions11 = {
    chart: {
        height: 70,
        type: "bar",
        stacked: true,
        sparkline: {
            enabled: true,
        },
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: "15%",
            colors: {
                backgroundBarColors: [secondary],
                backgroundBarOpacity: 0.2,
                backgroundBarRadius: 10,
            },
        },
    },
    colors: [secondary],
    stroke: {
        width: 0,
    },
    title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: "Dispatched",
        style: {
            fontSize: "18px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 500,
        },
    },
    subtitle: {
        floating: true,
        align: "right",
        offsetY: 0,
        text: "44%",
        style: {
            fontSize: "14px",
        },
    },
    tooltip: {
        enabled: false,
    },
    xaxis: {
        categories: ["Process 2"],
    },
    yaxis: {
        max: 100,
    },
    fill: {
        colors: [secondary],
        type: "gradient",
        gradient: {
            inverseColors: false,
            gradientToColors: [secondary],
        },
    },
    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions12 = {
    chart: {
        height: 70,
        type: "bar",
        stacked: true,
        sparkline: {
            enabled: true,
        },
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: "15%",
            colors: {
                backgroundBarColors: ["#a927f9"],
                backgroundBarOpacity: 0.2,
                backgroundBarRadius: 10,
            },
        },
    },
    colors: ["#a927f9"],
    stroke: {
        width: 0,
    },
    fill: {
        colors: ["#a927f9"],
        type: "gradient",
        gradient: {
            gradientToColors: ["#a927f9"],
        },
    },
    title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: "Reach Station",
        style: {
            fontSize: "18px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 500,
        },
    },
    subtitle: {
        floating: true,
        align: "right",
        offsetY: 0,
        text: "50%",
        style: {
            fontSize: "14px",
        },
    },
    tooltip: {
        enabled: false,
    },
    xaxis: {
        categories: ["Reach Station"],
    },
    yaxis: {
        max: 100,
    },
    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions13 = {
    chart: {
        height: 70,
        type: "bar",
        stacked: true,
        sparkline: {
            enabled: true,
        },
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: "15%",
            colors: {
                backgroundBarColors: ["#F8D62B"],
                backgroundBarOpacity: 0.2,
                backgroundBarRadius: 10,
            },
        },
    },
    colors: ["#F8D62B"],
    stroke: {
        width: 0,
    },
    fill: {
        colors: ["#F8D62B"],
        type: "gradient",
        gradient: {
            gradientToColors: ["#F8D62B"],
        },
    },
    title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: "Out for delivery",
        style: {
            fontSize: "18px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 500,
        },
    },
    subtitle: {
        floating: true,
        align: "right",
        offsetY: 0,
        text: "60%",
        style: {
            fontSize: "14px",
        },
    },
    tooltip: {
        enabled: false,
    },
    xaxis: {
        categories: ["Out for delivery"],
    },
    yaxis: {
        max: 100,
    },
    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions14 = {
    chart: {
        height: 70,
        type: "bar",
        stacked: true,
        sparkline: {
            enabled: true,
        },
    },
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: "15%",
            colors: {
                backgroundBarColors: ["#51BB25"],
                backgroundBarOpacity: 0.2,
                backgroundBarRadius: 10,
            },
        },
    },
    colors: ["#51BB25"],
    stroke: {
        width: 0,
    },
    series: [
        {
            name: "Delivered",
            data: [74],
        },
    ],
    fill: {
        colors: ["#51BB25"],
        type: "gradient",
        gradient: {
            gradientToColors: ["#51BB25"],
        },
    },
    title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: "Delivered",
        style: {
            fontSize: "18px",
            fontFamily: "Roboto, sans-serif",
            fontWeight: 500,
        },
    },
    subtitle: {
        floating: true,
        align: "right",
        offsetY: 0,
        text: "74%",
        style: {
            fontSize: "14px",
        },
    },
    tooltip: {
        enabled: false,
    },
    xaxis: {
        categories: ["Delivered"],
    },
    yaxis: {
        max: 100,
    },
    responsive: [{
        breakpoint: 767,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions15 = {
    chart: {
        height: 320,
        type: "area",
        toolbar: {
            show: false,
        },
    },
    stroke: {
        curve: "smooth",
        width: 0,
    },
    fill: {
        colors: [primary, secondary],
        type: "gradient",
        gradient: {
            shade: "light", type: "vertical",
            shadeIntensity: 0.4, inverseColors: false, opacityFrom: 0.9, opacityTo: 0.8,
            stops: [0, 100],
        },
    },
    dataLabels: {
        enabled: false,
    },
    grid: {
        borderColor: "rgba(196,196,196, 0.3)",
        padding: {
            top: 0, right: -120, bottom: 10,
        },
    },
    colors: [primary, secondary],
    labels: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
    ],
    markers: {
        size: 0,
    },
    xaxis: {
        axisTicks: {
            show: false,
        },
        axisBorder: {
            color: "rgba(196,196,196, 0.3)",
        },
    },
    yaxis: [
        {
            title: {
                text: "Dollars in thounand",

            },
        },
    ],
    tooltip: {
        shared: true,
        intersect: false,
        y: {
            formatter: function (y: number) {
                if (typeof y !== "undefined") {
                    return y.toFixed(0) + " points";
                }
                return y;
            },
        },
    },
}
export const chartOptions16 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 300,
        type: "area",
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    xaxis: {
        categories: [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
        ],
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
    },
    grid: {
        borderColor: "rgba(196,196,196, 0.3)",
        padding: {
            top: -20,
            right: -55,
            bottom: 0,
        },
    },
    fill: {
        opacity: 0.2,
    },
    colors: [primary],
    tooltip: {
        x: {
            format: "dd/MM/yy HH:mm",
        },
    },
}
export const chartOptions17 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 400,
        type: "area",
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    xaxis: {
        categories: [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Jan", "Feb", "Mar", "Apr", "May",
        ],
        tickAmount: 5,
        tickPlacement: "between",
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
        tooltip: {
            enabled: false,
        },
    },
    grid: {
        borderColor: "rgba(196,196,196, 0.3)",
        padding: {
            top: -20,
            right: -16,
            bottom: 0,
        },
    },
    fill: {
        opacity: 0.2,
    },
    colors: [primary],
    tooltip: {
        x: {
            format: "dd/MM/yy HH:mm",
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 200,
                }
            }
        }
    ]
}

export const chartOptions18 = {
    chart: {
        height: 400,
        type: "line",
        toolbar: {
            show: false,
        },
    },
    annotations: {
        yaxis: [
            {
                y: 8200,
                y2: 8400,
                borderColor: "#f8d62b", fillColor: "#f8d62b", opacity: 0.1,
                label: {
                    borderColor: "#f8d62b",
                    offsetX: -30,
                    style: {
                        fontSize: "10px", color: "#fff", background: "#f8d62b",
                    },
                    text: "Y-axis range",
                },
            },
        ],
        xaxis: [
            {
                x: new Date("15 Nov 2017").getTime(),
                strokeDashArray: 0,
                borderColor: primary,
                label: {
                    borderColor: primary, offsetY: 20,
                    style: {
                        color: "#fff", background: primary,
                    },
                    text: "Anno Test",
                },
            },
            {
                x: new Date("17 Nov 2017").getTime(),
                x2: new Date("18 Nov 2017").getTime(),
                fillColor: "#63d5be",
                opacity: 0.1,
                label: {
                    borderColor: "##63d5be",
                    style: {
                        fontSize: "10px", color: "#fff", background: "#63d5be",
                    },
                    offsetY: 20, text: "X-axis range",
                },
            },
        ],
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 3,
        curve: "smooth",
    },
    grid: {
        padding: {
            right: 30,
            left: 20,
        },
    },
    title: {
        text: "Line with Annotations",
        align: "left",
        style: {
            fontSize: "18px", fontFamily: "Nunito, sans-serif", fontWeight: 500,
        },
    },
    colors: [secondary],
    labels: monthDataSeries1[0].dates,
    xaxis: {
        type: "datetime",
    },
    responsive: [{
        breakpoint: 576,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }]
}
export const chartOptions19 = {
    plotOptions: {
        candlestick: {
            colors: {
                upward: '#7A70BA',
                downward: '#48A3D7'
            }
        }
    },
    legend: {
        show: false,
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'dark',
            type: 'vertical',
            shadeIntensity: 0.2,
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100],
        }
    },
    chart: {
        height: 450,
        type: "line",
        toolbar: {
            show: false,
        },
    },
    stroke: {
        curve: 'smooth',
        width: [1, 1],
    },

    xaxis: {
        type: "datetime",
        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false
        }
    },
    grid: {
        strokeDashArray: 3,
        position: 'back',
        row: {
            opacity: 0.5
        },
        column: {
            opacity: 0.5
        },
    },
    responsive: [
        {
            breakpoint: 576,
            options: {
                chart: {
                    height: 250,
                }
            }
        }
    ]
}
export const chartOptions20 = {
    chart: {
        height: 350,
        type: 'line',

        toolbar: {
            show: false,
        },
        zoom: {
            enabled: false,
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        width: 0,
    },
    title: {
        text: "Average",
        align: "left",
        style: {
            fontSize: "12px",
        },
    },
    subtitle: {
        text: "17%",
        floating: true,
        align: "right",
        offsetY: 0,
        style: {
            fontSize: "20px",
            fontWeight: 500,
        },
    },
    fill: {
        colors: [primary],
        type: "gradient",
        gradient: {
            shade: "light",
            type: "vertical",
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.8,
            stops: [0, 100],
        },
    },
    xaxis: {
        type: "datetime",
        range: 2700000,
    },
    yaxis: {
        decimalsInFloat: 1,
    },
    legend: {
        show: false,
    },
    responsive: [
        {
            breakpoint: 1366,
            options: {
                subtitle: {
                    style: {
                        fontSize: "18px",
                    },
                },
            },
        },
        {
            breakpoint: 992,
            options: {
                subtitle: {
                    style: {
                        fontSize: "16px",
                    },
                },
            },
        },
    ],
}
export const chartOptions21 = {
    chart: {
        height: 350,
        type: "line",
        stacked: true,
        animations: {
            enabled: true,
            easing: "linear",
            dynamicAnimation: {
                speed: 1000,
            },
        },
        events: {
            animationEnd: function (chartCtx: any) {
                const newData1 = chartCtx.w.config.series[0].data.slice();
                newData1.shift();
                const newData2 = chartCtx.w.config.series[1].data.slice();
                newData2.shift();
                window.setTimeout(function () {
                    chartCtx.updateOptions(
                        {
                            series: [
                                {
                                    data: newData1,
                                },
                                {
                                    data: newData2,
                                },
                            ],
                            subtitle: {

                            },
                        },
                        false,
                        false
                    );
                }, 300);
            },
        },
        toolbar: {
            show: false,
        },
        zoom: {
            enabled: false,
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        curve: "straight",
        width: 5,
    },
    grid: {
        padding: {
            left: 0,
            right: 0,
        },
    },
    fill: {
        opacity: 0.9,
    },
    colors: [primary, secondary],
    markers: {
        size: 0,
        hover: {
            size: 0,
        },
    },
    xaxis: {
        type: "datetime",
        range: 2700000,
    },
    yaxis: {
        decimalsInFloat: 1,
    },
    title: {
        text: "Processes",
        align: "left",
        style: {
            fontSize: "12px",
        },
    },
    legend: {
        show: true,
        floating: true,
        horizontalAlign: "right",
        onItemClick: {
            toggleDataSeries: false,
        },
        position: "top",
        offsetY: -33,
        offsetX: 60,
    },
    responsive: [{
        breakpoint: 1366,
        options: {
            title: {
                style: {
                    fontSize: "18px",
                },
            },
        },
    },
    {
        breakpoint: 992,
        options: {
            title: {
                style: {
                    fontSize: "16px",
                },
            },
        },
    }
    ]
}
export const chartOptions22 = {
    fill: {
        type: "gradient",
        gradient: {
            shade: "dark",
            type: "Reflected",
            shadeIntensity: 0.1,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.8,
            stops: [0, 100],
        },
    },
    colors: [primary, secondary],
    chart: {
        height: 300,
        type: "radar",
        dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1,
        },
    },
    title: {
        text: "Radar Chart - Multi Series",
    },
    stroke: {
        width: 0,
    },
    markers: {
        size: 0,
    },
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
}
export const chartOptions23 = {
    chart: {
        toolbar: {
            show: false,
        },
        height: 320,
        type: "bubble",
    },
    dataLabels: {
        enabled: false,
    },
    fill: {
        type: "gradient",
        gradient: {
            shade: "dark", type: "horizontal", shadeIntensity: 0.4, inverseColors: false, opacityFrom: 1, opacityTo: 0.7, stops: [0, 100],
        },
    },
    colors: [primary, secondary, "#51bb25",
        "#544fff",],
    title: {
        text: "Simple Bubble Chart",
    },
    xaxis: {
        tickAmount: 12,
        type: "category",
    },
    yaxis: {
        max: 70,
    },
}


export function generateData(baseval: number, count: number, yrange: any) {
    var i = 0;
    var series = [];
    while (i < count) {
        var x = Math.floor(Math.random() * (750 - 1 + 1)) + 1;
        var y =
            Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
        var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;

        series.push([x, y, z]);
        baseval += 86400000;
        i++;
    }
    return series;
}

export function getRandom() {
    var i = iteration;
    return (
        (Math.sin(i / trigoStrength) * (i / trigoStrength) +
            i / trigoStrength +
            1) *
        (trigoStrength * 2)
    );
}

export function generateMinuteWiseTimeSeries(baseval: number, count: number, yrange: any) {
    var i = 0;
    var series = [];
    while (i < count) {
        var x = baseval;
        var y =
            (Math.sin(i / trigoStrength) * (i / trigoStrength) +
                i / trigoStrength +
                1) *
            (trigoStrength * 2);

        series.push([x, y]);
        baseval += 300000;
        i++;
    }
    return series;
}