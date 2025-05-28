import { series17, series18, series19, series20, chartOptions17, chartOptions18, chartOptions19, chartOptions20 } from "@/core/data/chart"

export const atmosoverview = [
    {
        bg: "bg-primary",
        title: "Rainfall",
        number: "10mm",
    },
    {
        bg: "bg-secondary",
        title: "Humidity",
        number: "89.2%"
    },
    {
        bg: "bg-warning",
        title: "Wind Speed",
        number: "30m/s"
       
      
    },
    {
        bg: "bg-tertiary",
        title: "Wind Direction",
        number: "90º"
    }
]
export const baranioverview = [
    {
        bg: "bg-primary",
        title: "Rainfall",
        number: "15mm",
    },
    {
        bg: "bg-secondary",
        title: "Humidity",
        number: "63.2%"
    },
    {
        bg: "bg-warning",
        title: "Dewpoint",
        number: "18°C"
    },
    {
        bg: "bg-tertiary",
        title: "Irradiation",
        number: "1300W/m2"
    }
]
export const pawsoverview = [
    {
        bg: "bg-primary",
        title: "Rainfall",
        number: "8mm",
    },
    {
        bg: "bg-secondary",
        title: "Humidity",
        number: "71.8%"
    },
    {
        bg: "bg-warning",
        title: "Wind Speed",
        number: "18m/s"
    },
    {
        bg: "bg-tertiary",
        title: "Wind Direction",
        number: "108º"
    }
]
export const paws2overview = [
    {
        bg: "bg-primary",
        title: "Rainfall",
        number: "1mm",
    },
    {
        bg: "bg-secondary",
        title: "Humidity",
        number: "65.5%"
    },
    {
        bg: "bg-warning",
        title: "Wind Speed",
        number: "30m/s"
    },
    {
        bg: "bg-tertiary",
        title: "Wind Direction",
        number: "138º"
    }
]

export const notificationbox = [
    {
        bgclass: "bg-light-primary",
        img: "dashboard/icon/wallet.png",
        title: "New daily offer added",
        desc: "New user-only offer added",
        date: "10 Sep,2024"
    },
    {
        bgclass: "bg-light-info",
        img: "dashboard/icon/shield-dne.png",
        title: "Product Evaluation",
        desc: "Changed to a new workflow",
        date: "12 Oct,2024"
    },
    {
        bgclass: "bg-light-warning",
        img: "dashboard/icon/graph.png",
        title: "Return of a Product",
        desc: "452 items were returned",
        date: "15 Mar,2024"
    },
    {
        bgclass: "bg-light-tertiary",
        img: "dashboard/icon/ticket-star.png",
        title: "Recently Paid",
        desc: "Mastercard payment of $343",
        date: "20 Jun,2024"
    }
]
export const upcoming = [
    {
        name: "John Elliot",
        img: "dashboard/user/05.png",
        date: "21 Oct 2024",
        time: "15:55 AM"
    },
    {
        name: "Ashley Hart",
        img: "dashboard/user/06.png",
        date: "12 Oct 2024",
        time: "10:20 AM"
    },
    {
        name: "Anna lverson",
        img: "dashboard/user/07.png",
        date: "05 Oct 2024",
        time: "14:30 AM"
    },
    {
        name: "Dana Lemon",
        img: "dashboard/user/08.png",
        date: "01 Oct 2024",
        time: "18:45 AM"
    }
]
export const membersbox = [
    {
        img: "dashboard/user/01.jpg",
        name: "Joshua Woo",
        desc: "Climate Data Scientist",
        status: "Pending",
        statusclass: "background-light-primary b-light-primary font-primary"
    },
    {
        img: "dashboard/user/02.jpg",
        name: "Ashley Hart",
        desc: "Meteorological Analyst",
        status: "Pending",
        statusclass: "background-light-primary b-light-primary font-primary"
    },
    {
        img: "dashboard/user/03.jpg",
        name: "Anna lverson",
        desc: "Atmospheric Researcher",
        status: "Approved",
        statusclass: "background-light-secondary b-light-secondary font-secondary"
    },
    {
        img: "dashboard/user/04.jpg",
        name: "Ron Dayley",
        desc: "Weather Systems Engineer",
        status: "Approved",
        statusclass: "background-light-secondary b-light-secondary font-secondary"
    },
    {
        img: "dashboard/user/02.jpg",
        name: "Sarah Chen",
        desc: "Climate Data Modeler",
        status: "Pending",
        statusclass: "background-light-primary b-light-primary font-primary"
    },
    {
        img: "dashboard/user/03.jpg",
        name: "Marcus Thompson",
        desc: "Precipitation Analyst",
        status: "Approved",
        statusclass: "background-light-secondary b-light-secondary font-secondary"
    },

]
export const sale = [
    {
        img: "dashboard/icon/customers.png",
        title: "Customers",
        num: "1.736",
        fontclass: "font-success",
        total: "+3,7%"
    },
    {
        img: "dashboard/icon/revenue.png",
        title: "Revenue",
        num: "$9.247 ",
        fontclass: "font-danger",
        total: "-0,10%"
    },
    {
        img: "dashboard/icon/profit.png",
        title: "Profit",
        num: "80%",
        fontclass: "font-success",
        total: "+11,6%"
    }
]
export const saleproduct = [
    {
   
        name: "ATMOS - z6-26732",
        time: "0:28",
        progressclass: "progress-striped-secondary",
        width: "40%"
    },
    {

        name: "BARANI - 2101LH028",
        time: "0:40",
        progressclass: "progress-striped-warning",
        width: "60%"
    },
    {
   
        name: "3D PAWS - T01 Rawin",
        time: "0:56",
        progressclass: "progress-striped-tertiary",
        width: "80%"
    },
    {
        name: "3D PAWS - T14 UTT",
        time: "0:35",
        progressclass: "progress-striped-primary",
        width: "50%"
    },
    {
        name: "3D PAWS - T01 Rawinsonde",
        time: "0:35",
        progressclass: "progress-striped-info",
        width: "90%"
    }
]
export const project = [
        {
            title: "T01 Rawinsonde",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "13 Aug 2024",
            unit: "ºC",
            type: "Temperature",
            value: "30.0"
        },
        {
            title: "T10 Paramin",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "06 Jan 2024",
            unit: "m/s",
            type: "Wind Speed",
            value: "4.2"
        },
        {
            title: "T03 Centeno",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "27 Jun 2024",
            unit: "mm",
            type: "Rainfall",
            value: "2.5"
        },
        {
            title: "T04 Mayaro",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "28 Jul 2024",
            unit: "%",
            type: "Humidity",
            value: "78.3"
        },
        {
            title: "T06 Moruga",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "10 Mar 2024",
            unit: "m/s",
            type: "Wind Speed",
            value: "3.8"
        },
        {
            title: "T08 Penal",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "21 Feb 2024",
            unit: "mm",
            type: "Rainfall",
            value: "1.8"
        },
        {
            title: "T07 Wild Fowl Trust",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "22 Feb 2024",
            unit: "ºC",
            type: "Temperature",
            value: "29.5"
        },
        {
            title: "T11 UWI",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "02 Apr 2024",
            unit: "m/s",
            type: "Wind Speed",
            value: "5.1"
        },
        {
            title: "T09 Brigand Hill",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "04 May 2024",
            unit: "mm",
            type: "Rainfall",
            value: "3.2"
        },
        {
            title: "T12 Caroni",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "24 Oct 2024",
            value: "75.6",
            unit: "%",
            type: "Humidity"
       
        },
        {
            title: "T15 ASJA",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "01 1Nov 2024",
            value: "31.2",
            unit: "ºC",
            type: "Temperature"
        
        },
        {
            title: "T13 Matelot",
            bgclass: "bg-primary",
            file: "3D-Paws",
            date: "02 May 2024",
            value: "4.1",
            unit: "mm",
            type: "Rainfall"
         
        }
]
export const projectstatus = [
    {
        btnclass: "btn-light1-primary",
        iconclass: "bg-primary",
        img: "dashboard-2/svg-icon/calendar.png",
        title: "Upcomings",
        desc: "5 Projects"
    },
    {
        btnclass: "btn-light1-secondary",
        iconclass: "bg-secondary",
        img: "dashboard-2/svg-icon/check.png",
        title: "Completed",
        desc: "27 Projects"
    },
    {
        upcoming: "mb-0",
        btnclass: "btn-light1-warning",
        iconclass: "bg-warning",
        img: "dashboard-2/svg-icon/processing.png",
        title: "In Progress",
        desc: "13 Projects"
    },
    {
        upcoming: "mb-0",
        btnclass: "btn-light1-tertiary",
        iconclass: "bg-tertiary",
        img: "dashboard-2/svg-icon/total.png",
        title: "Total",
        desc: "47 Projects"
    }
]
export const recentdata = [
    {
        name: "Behance Post",
        children: [
            {
                img: "dashboard-2/user/1.png",
            },
            {
                img: "dashboard-2/user/2.png",
            }
        ],
        start: "05Jan23",
        finish: "12Jan23",
        more: true,
        series: series17,
        chart: chartOptions17
    },
    {
        name: "Figma Design",
        children: [
            {
                img: "dashboard-2/user/4.png",
            },
            {
                img: "dashboard-2/user/6.png",
            },
            {
                img: "dashboard-2/user/5.png",
            }
        ],
        start: "11Feb23",
        finish: "24Feb23",
        more: false,
        series: series18,
        chart: chartOptions18
    },
    {
        name: "Web Page",
        children: [
            {
                img: "dashboard-2/user/7.png",
            },
            {
                img: "dashboard-2/user/8.png",
            }
        ],
        start: "17Mar23",
        finish: "08Mar23",
        more: true,
        series: series19,
        chart: chartOptions19
    },
    {
        name: "CRM Admin",
        children: [
            {
                img: "dashboard-2/user/12.png",
            },
            {
                img: "dashboard-2/user/11.png",
            },
            {
                img: "dashboard-2/user/12.png",
            }
        ],
        start: "05Sep23",
        finish: "13Sep23",
        more: false,
        series: series20,
        chart: chartOptions20
    }
]
export const totalproject = [
    {
        bgclass: "bg-primary",
        title: "Active"
    },
    {
        bgclass: "bg-secondary",
        title: "Inactive"
    },
 
]
export const projectdata = [
    {
        col: "col-xl-3 col-xl-50 col-md-6 proorder-md-7",
        title: "Website Design",
        img: "dashboard-2/user/16.png",
        name: "Square Dashboard",
        email: "karson123@gmail.com",
        class1: "bg-light-primary font-primary",
        design1: "UX Design",
        class2: "bg-light-secondary font-secondary",
        design2: "3D Deisgn",
        ratting: [
            {
                rating: "12",
                name: "Issues"
            },
            {
                rating: "5",
                name: "Resolved "
            },
            {
                rating: "7",
                name: "Comment"
            }
        ],
        task: "6/10",
        progressclass: "progress-striped-primary",
        width: "50%"
    },
    {
        col: "col-xl-3 col-xl-50 col-md-6 proorder-md-8",
        title: "Social Post Design",
        img: "dashboard-2/user/18.png",
        name: "Cronin Lewis",
        email: "cronin324@gmail.com",
        class1: "bg-light-primary font-primary",
        design1: "Illustration",
        class2: "bg-light-warning font-warning",
        design2: "Video Editing",
        ratting: [
            {
                rating: "10",
                name: "Issues"
            },
            {
                rating: "9 ",
                name: "Resolved"
            },
            {
                rating: "5",
                name: "Comment"
            }
        ],
        task: "4/10",
        progressclass: "progress-striped-secondary",
        width: "40%"
    },
    {
        col: "col-xl-3 col-xl-50 col-md-6 proorder-md-9",
        title: "Podcast Web design",
        img: "dashboard-2/user/17.png",
        name: "Rau Foster",
        email: "raufoster23@gmail.com",
        class1: "bg-light-tertiary font-tertiary",
        design1: "2D Design",
        class2: "bg-light-secondary font-secondary",
        design2: "Dribbble Post",
        ratting: [
            {
                rating: "16",
                name: "Issues"
            },
            {
                rating: "10",
                name: "Resolved"
            },
            {
                rating: "7",
                name: "Comment"
            }
        ],
        task: " 8/10",
        progressclass: "progress-striped-warning",
        width: "80%"
    },
    {
        col: "col-xl-3 col-xl-50 col-md-6 proorder-md-10",
        title: "Crypto Dashboard",
        img: "dashboard-2/user/19.png",
        name: "Volkman Melisa",
        email: "volkman839@gmail.com",
        class1: "bg-light-primary font-primary",
        design1: "Design System",
        class2: "bg-light-secondary font-secondary",
        design2: "Branding",
        ratting: [
            {
                rating: "04",
                name: "Issues"
            },
            {
                rating: "5",
                name: "Resolved"
            },
            {
                rating: "7 ",
                name: "Comment"
            }
        ],
        task: "2/10",
        progressclass: "progress-striped-tertiary",
        width: "20%"
    }
]
export const task = [
    {
        class: "font-primary",
        title: "NFT illustrarion Package",
        img: "dashboard-2/user/17.png",
        desc: "Hackett Yessenia ",

    },
    {
        class: "font-secondary",
        title: "Podcast landing Page",
        img: "dashboard-2/user/13.png",
        image: true,
        img2: "dashboard-2/user/14.png",
        desc: "schneider.."
    },
    {
        class: "font-warning",
        title: "Delivery Food Ap",
        img: "dashboard-2/user/15.png",
        desc: "Mahdi Gholizadeh",

    }
]
export const event = [
    {
        img: "dashboard-2/user/1.png"
    },
    {
        img: "dashboard-2/user/2.png"
    },
    {
        img: "dashboard-2/user/3.png"
    }
]
export const recentproject = [
    {
        name: "",
        images: [
            {
                img: ""
            },
            {
                img: ""
            }
        ],
        start: "",
        finish: "",

    }
]
export const client = [
    {
        img: "dashboard-2/svg-icon/1.png",
        name: 'Redesign Layout',
        by: 'Anna Catmire',
        time: 'Sep 20 - Oct 26',
        social: [
            'dashboard-2/user/1.png',
            'dashboard-2/user/12.png',
            'dashboard-2/user/3.png'
        ],
        more: true,
        type: 'UI/UX Design',
        progress: "width: 40%",
        color: 'primary'
    },
    {
        img: "dashboard-2/svg-icon/2.png",
        name: 'Login & Sign Up Ui',
        by: 'John Elliot',
        time: 'Mar 16 - Apr 10',
        social: [
            'dashboard-2/user/4.png',
            'dashboard-2/user/5.png',
            'dashboard-2/user/6.png'
        ],
        more: false,
        type: 'Designer',
        progress: "width: 70%",
        color: 'secondary'
    },
    {
        img: "dashboard-2/svg-icon/3.png",
        name: 'Redesign CRM',
        by: 'Ashley Hart',
        time: 'May 09 - Jun 02',
        social: [
            'dashboard-2/user/7.png',
            'dashboard-2/user/8.png',
            'dashboard-2/user/9.png'
        ],
        more: true,
        type: 'UI/UX Design',
        progress: "width: 50%",
        color: 'warning'
    },
    {
        img: "dashboard-2/svg-icon/4.png",
        name: 'Front-End Website',
        by: 'Dana Lemon',
        time: 'Jul 12 - Aug 20',
        social: [
            'dashboard-2/user/10.png',
            'dashboard-2/user/11.png',
            'dashboard-2/user/12.png'
        ],
        more: true,
        type: 'Developer',
        progress: "width: 50%",
        color: 'tertiary'
    },
    {
        img: "dashboard-2/svg-icon/1.png",
        name: 'Redesign Layout',
        by: 'Anna Catmire',
        time: 'Sep 20 - Oct 26',
        social: [
            'dashboard-2/user/1.png',
            'dashboard-2/user/12.png',
            'dashboard-2/user/3.png'
        ],
        more: true,
        type: 'UI/UX Design',
        progress: "width: 40%",
        color: 'primary'
    },
    {
        img: "dashboard-2/svg-icon/2.png",
        name: 'Login & Sign Up Ui',
        by: 'John Elliot',
        time: 'Mar 16 - Apr 10',
        social: [
            'dashboard-2/user/4.png',
            'dashboard-2/user/5.png',
            'dashboard-2/user/6.png'
        ],
        more: false,
        type: 'Designer',
        progress: "width: 70%",
        color: 'secondary'
    },
    {
        img: "dashboard-2/svg-icon/3.png",
        name: 'Redesign CRM',
        by: 'Ashley Hart',
        time: 'May 09 - Jun 02',
        social: [
            'dashboard-2/user/7.png',
            'dashboard-2/user/8.png',
            'dashboard-2/user/9.png'
        ],
        more: true,
        type: 'UI/UX Design',
        progress: "width: 50%",
        color: 'warning'
    },
    {
        img: "dashboard-2/svg-icon/4.png",
        name: 'Front-End Website',
        by: 'Dana Lemon',
        time: 'Jul 12 - Aug 20',
        social: [
            'dashboard-2/user/10.png',
            'dashboard-2/user/11.png',
            'dashboard-2/user/12.png'
        ],
        more: true,
        type: 'Developer',
        progress: "width: 50%",
        color: 'tertiary'
    },
    {
        img: "dashboard-2/svg-icon/3.png",
        name: 'Redesign CRM',
        by: 'Ashley Hart',
        time: 'May 09 - Jun 02',
        social: [
            'dashboard-2/user/7.png',
            'dashboard-2/user/8.png',
            'dashboard-2/user/9.png'
        ],
        more: true,
        type: 'UI/UX Design',
        progress: "width: 50%",
        color: 'warning'
    },
    {
        img: "dashboard-2/svg-icon/4.png",
        name: 'Front-End Website',
        by: 'Dana Lemon',
        time: 'Jul 12 - Aug 20',
        social: [
            'dashboard-2/user/10.png',
            'dashboard-2/user/11.png',
            'dashboard-2/user/12.png'
        ],
        more: true,
        type: 'Developer',
        progress: "width: 50%",
        color: 'tertiary'
    }

]
export const order = [
    {
        img: "dashboard-3/1.png",
        order: "Decorative Plants",
        date: "20 Sep - 03.00AM",
        qty: "QTY:12",
        imgs: "dashboard-3/user/6.png",
        customer: "Leonie Green ",
        price: "637.30",
        statusclass: "background-light-success font-success",
        status: "Succeed"
    },
    {
        img: "dashboard-3/2.png",
        order: "Sticky Calender",
        date: "12 Mar - 08.12AM",
        qty: "QTY:14",
        imgs: "dashboard-3/user/8.png",
        customer: "Peter White",
        price: "637.30",
        statusclass: "background-light-warning font-warning",
        status: "Waiting"
    },
    {
        img: "dashboard-3/3.png",
        order: "Crystal Mug",
        date: "Feb 15 - 10.00AM",
        qty: "QTY:19",
        imgs: "dashboard-3/user/7.png",
        customer: "Ruby Yang",
        price: "637.30",
        statusclass: "background-light-success font-success",
        status: "Succeed"
    },
    {
        img: "dashboard-3/4.png",
        order: "Motion Table Lamp",
        date: "Jun 10 - 12.30AM",
        qty: "QTY:17",
        imgs: "dashboard-3/user/8.png",
        customer: "Visha Long",
        price: "637.30",
        statusclass: "background-light-danger font-danger",
        status: "Canceled"
    },
    {
        img: "dashboard-3/2.png",
        order: "Sticky Calender",
        date: "12 Mar - 08.12AM",
        qty: "QTY:14",
        imgs: "dashboard-3/user/8.png",
        customer: "Peter White",
        price: "637.30",
        statusclass: "background-light-warning font-warning",
        status: "Waiting"
    },
    {
        img: "dashboard-3/3.png",
        order: "Crystal Mug",
        date: "Feb 15 - 10.00AM",
        qty: "QTY:19",
        imgs: "dashboard-3/user/7.png",
        customer: "Ruby Yang",
        price: "637.30",
        statusclass: "background-light-success font-success",
        status: "Succeed"
    },
    {
        img: "dashboard-3/4.png",
        order: "Motion Table Lamp",
        date: "Jun 10 - 12.30AM",
        qty: "QTY:17",
        imgs: "dashboard-3/user/8.png",
        customer: "Visha Long",
        price: "637.30",
        statusclass: "background-light-danger font-danger",
        status: "Canceled"
    }
]
export const customers = [
    {
        img: "dashboard-3/user/1.png",
        name: "Junsung Park",
        ids: "ID #32449",
        textclass: "text-success",
        text: "Paid",
        price: "8282.13",
        min: "50 min ago"
    },
    {
        img: "dashboard-3/user/2.png",
        name: "Yongjae Choi",
        ids: "ID #95460",
        textclass: "text-danger",
        text: "Pending",
        price: "9546.84",
        min: "34 min ago"
    },
    {
        img: "dashboard-3/user/3.png",
        name: "Seonil Jang",
        ids: "ID #95468",
        textclass: "text-success",
        text: "Paid",
        price: "2354.16",
        min: "30 min ago"
    },
    {
        img: "dashboard-3/user/4.png",
        name: "Joohee Min",
        ids: "ID #95462",
        textclass: "text-danger",
        text: "Pending",
        price: "3254.35",
        min: "25 min ago"
    },
    {
        img: "dashboard-3/user/5.png",
        name: "Soojung Kin",
        ids: "ID #34586",
        textclass: "text-success",
        text: "Paid",
        price: "3654.32",
        min: "23 min ago"
    }
]
export const progresuser = [
    {
        class: "bg-primary",
        width: "25%"
    },
    {
        class: "bg-secondary",
        width: "25%"
    },
    {
        class: "bg-warning",
        width: "25%"
    },
    {
        class: "bg-tertiary",
        width: "25%"
    }
]
export const mapitems = [
    {
        class: "bg-primary",
        title: "Keyboard",
        number: "651"
    },
    {
        class: "bg-secondary",
        title: "Laptops",
        number: "345"
    },
    {
        class: "bg-warning",
        title: "Desktop",
        number: "654"
    },
    {
        class: "bg-tertiary",
        title: "Mouse",
        number: "954"
    }
]
export const contries = [
    {
        class: "fill-primary",
        icon: "map-loaction",
        title: "United States",
        total: "53.23"
    },
    {
        class: "fill-secondary",
        icon: "map-loaction",
        title: "Romania",
        total: "31.85"
    },
    {
        class: "fill-warning",
        icon: "map-loaction",
        title: "Austalia",
        total: "12.98"
    },
    {
        class: "fill-tertiary",
        icon: "map-loaction",
        title: "Germany",
        total: "45.23"
    },
    {
        class: "fill-success",
        icon: "map-loaction",
        title: "Africa",
        total: "23.15"
    },
    {
        class: "fill-danger",
        icon: "map-loaction",
        title: "Europe",
        total: "95.75"
    }
]
export const slide = [
    {
        img: "dashboard-3/slider/1.png"
    },
    {
        img: "dashboard-3/slider/2.png"
    },
    {
        img: "dashboard-3/slider/3.png"
    }
]
export const proslide = [
    {
        img: "dashboard-3/slider/4.png"
    },
    {
        img: "dashboard-3/slider/5.png"
    },
    {
        img: "dashboard-3/slider/6.png"
    }
]
export const seller = [
    {
        img: "dashboard-3/user/9.png",
        name: "Gary Waters",
        brand: "Adidas",
        product: "Clothes",
        sold: "650",
        price: "37.50",
        earning: "24375"
    },
    {
        img: "dashboard-3/user/10.png",
        name: "Edwin Hogan",
        brand: "Nike",
        product: "Shoes",
        sold: "956",
        price: "24.75",
        earning: "23661"
    },
    {
        img: "dashboard-3/user/11.png",
        name: "Aaron Hogan",
        brand: "Sony",
        product: "Electronics",
        sold: "348",
        price: "184.50",
        earning: "64206"
    },
    {
        img: "dashboard-3/user/12.png",
        name: "Ralph Waters",
        brand: "i Phone",
        product: "Mobile",
        sold: "100",
        price: "150.25",
        earning: "15025"
    }
]

// Barani data remains the same as it already had battery info
export const baranidata = [
    {
        number: "24.5 °C",
        text: "Air Temperature",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/student.png",
        cardclass: "student",
        fontclass: "font-danger",
        total: "- 0.8",
        month: "24:00PM"
    },
    {
        number: "0.5 mm",
        text: "Rainfall",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/teacher.png",
        cardclass: "student-2",
        fontclass: "font-success",
        total: "+0.5",
        month: "24:00PM"
    },
    {
        number: "65.8 %",
        text: "Humidity",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 3.2",
        month: "24:00PM"
    },
    {
        number: "3.2 m/s",
        text: "Wind Speed",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.5",
        month: "24:00PM"
    },
    {
        number: "245.0 °",
        text: "Wind Direction",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 15.0",
        month: "24:00PM"
    },
    {
        number: "1013.2 hPa",
        text: "Atmospheric Pressure",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.3",
        month: "24:00PM"
    },
    {
        number: "85.2 %",
        text: "Battery Percent",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "- 0.1",
        month: "24:00PM"
    },
    {
        number: "12.8 V",
        text: "Battery Voltage",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.2",
        month: "24:00PM"
    }
]

export const ott_hydromet_data = [
    {
        number: "24.8 °C",
        text: "Air Temperature",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/student.png",
        cardclass: "student",
        fontclass: "font-danger",
        total: "- 0.6",
        month: "24:00PM"
    },
    {
        number: "0.6 mm",
        text: "Rainfall",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/teacher.png",
        cardclass: "student-2",
        fontclass: "font-success",
        total: "+0.6",
        month: "24:00PM"
    },
    {
        number: "66.2 %",
        text: "Humidity",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 2.8",
        month: "24:00PM"
    },
    {
        number: "3.8 m/s",
        text: "Wind Speed",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.4",
        month: "24:00PM"
    },
    {
        number: "242.5 °",
        text: "Wind Direction",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 12.5",
        month: "24:00PM"
    },
    {
        number: "1013.0 hPa",
        text: "Atmospheric Pressure",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.2",
        month: "24:00PM"
    },
    {
        number: "88.5 %",
        text: "Battery Percent",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "- 0.1",
        month: "24:00PM"
    },
    {
        number: "13.1 V",
        text: "Battery Voltage",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.1",
        month: "24:00PM"
    }
]

export const paws_data = [
    {
        number: "25.0 °C",
        text: "Air Temperature",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/student.png",
        cardclass: "student",
        fontclass: "font-danger",
        total: "- 0.7",
        month: "24:00PM"
    },
    {
        number: "0.4 mm",
        text: "Rainfall",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/teacher.png",
        cardclass: "student-2",
        fontclass: "font-success",
        total: "+0.4",
        month: "24:00PM"
    },
    {
        number: "65.5 %",
        text: "Humidity",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 2.6",
        month: "24:00PM"
    },
    {
        number: "3.4 m/s",
        text: "Wind Speed",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.6",
        month: "24:00PM"
    },
    {
        number: "243.5 °",
        text: "Wind Direction",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 13.5",
        month: "24:00PM"
    },
    {
        number: "1013.5 hPa",
        text: "Atmospheric Pressure",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.5",
        month: "24:00PM"
    },
    {
        number: "86.8 %",
        text: "Battery Percent",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "- 0.2",
        month: "24:00PM"
    },
    {
        number: "12.9 V",
        text: "Battery Voltage",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.1",
        month: "24:00PM"
    }
]

export const zentradata = [
    {
        number: "24.6 °C",
        text: "Air Temperature",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/student.png",
        cardclass: "student",
        fontclass: "font-danger",
        total: "- 0.9",
        month: "24:00PM"
    },
    {
        number: "0.7 mm",
        text: "Rainfall",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/teacher.png",
        cardclass: "student-2",
        fontclass: "font-success",
        total: "+0.7",
        month: "24:00PM"
    },
    {
        number: "65.0 %",
        text: "Humidity",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "+ 2.7",
        month: "24:00PM"
    },
    {
        number: "3.6 m/s",
        text: "Wind Speed",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.4",
        month: "24:00PM"
    },
    {
        number: "244.0 °",
        text: "Wind Direction",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.4",
        month: "24:00PM"
    },
    {
        number: "1032.2 hPa",
        text: "Atmospheric Pressure",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.3",
        month: "24:00PM"
    },
    {
        number: "65.2 %",
        text: "Battery Percent",
        iconclass: "bg-light-success",
        icon: "icon-arrow-up font-success",
        img: "dashboard-4/icon/calendar.png",
        cardclass: "student-3",
        fontclass: "font-success",
        total: "- 0.1",
        month: "24:00PM"
    },
    {
        number: "12.9 V",
        text: "Battery Voltage",
        iconclass: "bg-light-danger",
        icon: "icon-arrow-down font-danger",
        img: "dashboard-4/icon/invoice.png",
        cardclass: "student-4",
        fontclass: "font-danger",
        total: "- 0.2",
        month: "24:00PM"
    }
]
export const assignments = [
    {
        name: "Atmos",
        bgclass: "bg-primary",
        type:"Z6-26732",
        date: "12 May 2024",
        time:"0:25",
        progressclass: "progress-border-primary",
        width: "80%"
    },
]
export const ott_hydromet_monitor = [
    {
        name: "Hydromet",
        bgclass: "bg-primary",
        id:"323-238-H",
        date: "12 Nov 2024",
        time:"9:10 AM",
        status:"Sucessful"
    },
]
export const paws_monitor = [
    {
        name: "3D_Paws",
        bgclass: "bg-primary",
        id:"T01 Rawin",
        date: "12 Nov 2024",
        time:"9:10 AM",
        status:"Sucessful"
    },
]
export const zentramonitor = [
    {
        name: "Atmos",
        bgclass: "bg-primary",
        id:"Z6-26732",
        date: "12 Nov 2024",
        time:"9:10 AM",
        status:"Sucessful"
    },
]
export const sutronmonitor = [
    {
        name: "Sutron",
        bgclass: "bg-primary",
        id:"323-238-H",
        date: "12 Nov 2024",
        time:"9:10 AM",
        status:"Sucessful"
    },
]
export const baranimonitor = [
    {
        name: "Barani",
        bgclass: "bg-primary",
        id:"2101LH028",
        date: "12 Nov 2024",
        time:"9:10 AM",
        status:"Sucessful"
    }, 
]

export const meting = [
    {
        img: "dashboard-4/metting/chart.png"
    },
    {
        img: "dashboard-4/metting/message.png"
    },
    {
        img: "dashboard-4/metting/1.png"
    },
    {
        img: "dashboard-4/metting/2.png"
    },
    {
        img: "dashboard-4/metting/3.png"
    },
    {
        img: "dashboard-4/metting/4.png"
    },
    {
        img: "dashboard-4/metting/5.png"
    },
    {
        img: "dashboard-4/metting/6.png"
    },
    {
        img: "dashboard-4/metting/7.png"
    },
    {
        img: "dashboard-4/metting/8.png"
    },
    {
        img: "dashboard-4/metting/9.png"
    },
    {
        img: "dashboard-4/metting/10.png"
    }
]
export const enrolled = [
    {
        class: "b-primary bg-primary",
        title: "After Effects CC Masterclass",
        time: "10:20 -11:30"
    },
    {
        class: "b-secondary bg-secondary",
        title: "Design from A to Z",
        time: "09:00 -10:30"
    },
    {
        class: "b-warning bg-warning",
        title: "Graphic Design Bootcamp",
        time: "15:00 -16:00"
    },
    {
        class: "b-tertiary bg-tertiary",
        title: "The Ultimate Guide to Usabillity",
        time: "13:25 -14:30"
    },
    {
        class: "b-success bg-success",
        title: "After Effects CC Masterclass",
        time: "12:45 -14:20"
    }
]
export const featured = [
    {
        img: "dashboard-4/featured/1.png",
        name: "Mobile UX",
        subname: "Erin Mooney",
        start: "Feb 15",
        rate: "4.8",
        type: "UX/UI Design",
        icon: "bookmark",
        isActive: false
    },
    {
        img: "dashboard-4/featured/2.png",
        name: "Illustration",
        subname: "Elsie Lemon",
        start: "Mar 22",
        rate: "2.3",
        type: "Web Designer",
        icon: "bookmark",
        isActive: false
    },
    {
        img: "dashboard-4/featured/3.png",
        name: "Design System",
        subname: "Anna Green",
        start: "Jun 28",
        rate: "1.5",
        type: "Developer",
        icon: "bookmark",
        isActive: false
    },
    {
        img: "dashboard-4/featured/4.png",
        name: "Leadership",
        subname: "John  Elliot",
        start: "Apr 04",
        rate: "2.4",
        type: "UX/UI Design",
        icon: "bookmark",
        isActive: false
    },
    {
        img: "dashboard-4/featured/5.png",
        name: "Latest Figma",
        subname: "Dylan Field",
        start: "jun 01",
        rate: "5.4",
        type: "Graphic Designer",
        icon: "bookmark",
        isActive: false
    }
]
export const website = [
    {
        number: "1",
        title: "Offline"
    },
    {
        number: "1",
        title: "Resolved"
    },
    {
        number: "2",
        title: "Disabled"
    },

]
