interface tick {
    title: string,
    number: string,
    progress: string
}
interface item {
    id: number,
    img: string,
    name: string,
    key:string,
    first_used:string,
    last_used:string,
    status:string,
}
export const ticket: tick[] = [
    {
        title: "Order",
        number: "2563",
        progress: "bg-primary"
    },
    {
        title: "Pending",
        number: "8943",
        progress: "bg-secondary"
    },
    {
        title: "Running",
        number: "2500",
        progress: "bg-warning"
    },
    {
        title: "Smooth",
        number: "2060",
        progress: "bg-info"
    },
    {
        title: "Done",
        number: "5600",
        progress: "bg-success"
    },
    {
        title: "Cancle",
        number: "2560",
        progress: "bg-danger"
    }
]
export const items: item[] = [
        {
            id: 1,
            img: "user/1.jpg",
            name: "Elana White",
            key: "****-****-****-4321",
            first_used: "2023-03-01",
            last_used: "2023-10-12",
            status: "Active"
        },
        {
            id: 2,
            img: "user/2.png",
            name: "Tiger Nixon",
            key: "****-****-****-4121",
            first_used: "2023-05-07",
            last_used: "2023-09-28",
            status: "Inactive"
        },
        {
            id: 3,
            img: "user/3.jpg",
            name: "Genelia Winters",
            key: "****-****-****-8422",
            first_used: "2023-01-15",
            last_used: "2023-11-01",
            status: "Active"
        },
        {
            id: 4,
            img: "user/4.jpg",
            name: "Robbert Winters",
            key: "****-****-****-6522",
            first_used: "2022-12-20",
            last_used: "2023-09-15",
            status: "Suspended"
        },
        {
            id: 5,
            img: "user/5.jpg",
            name: "Garrett Winters",
            key: "****-****-****-1422",
            first_used: "2023-03-11",
            last_used: "2023-10-10",
            status: "Active"
        },
        {
            id: 6,
            img: "user/6.jpg",
            name: "Ashton Cox",
            key: "****-****-****-1952",
            first_used: "2023-02-10",
            last_used: "2023-08-14",
            status: "Inactive"
        },
        {
            id: 7,
            img: "user/7.jpg",
            name: "Cedric Kelly",
            key: "****-****-****-6224",
            first_used: "2023-06-01",
            last_used: "2023-10-05",
            status: "Active"
        },
        {
            id: 8,
            img: "user/8.jpg",
            name: "Helly Shah",
            key: "****-****-****-5678",
            first_used: "2023-01-20",
            last_used: "2023-10-31",
            status: "Active"
        },
        {
            id: 9,
            img: "user/9.jpg",
            name: "Airi Satou",
            key: "****-****-****-4789",
            first_used: "2023-04-02",
            last_used: "2023-09-12",
            status: "Suspended"
        },
        {
            id: 10,
            img: "user/10.jpg",
            name: "Hendri Feyol",
            key: "****-****-****-3804",
            first_used: "2023-05-15",
            last_used: "2023-09-01",
            status: "Active"
        },
        {
            id: 11,
            img: "user/1.jpg",
            name: "Herrod Chandler",
            key: "****-****-****-9608",
            first_used: "2023-06-10",
            last_used: "2023-10-21",
            status: "Inactive"
        },
        {
            id: 12,
            img: "user/5.jpg",
            name: "Rhona Davidson",
            key: "****-****-****-6200",
            first_used: "2023-02-28",
            last_used: "2023-08-25",
            status: "Suspended"
        },
        {
            id: 13,
            img: "user/1.jpg",
            name: "Colleen Hurst",
            key: "****-****-****-2360",
            first_used: "2023-03-19",
            last_used: "2023-10-08",
            status: "Active"
        },
        {
            id: 14,
            img: "user/2.png",
            name: "Sonya Frost",
            key: "****-****-****-1667",
            first_used: "2023-05-01",
            last_used: "2023-08-14",
            status: "Inactive"
        },
        {
            id: 15,
            img: "user/3.png",
            name: "Jena Gaines",
            key: "****-****-****-3814",
            first_used: "2023-07-10",
            last_used: "2023-10-05",
            status: "Active"
        },
        {
            id: 16,
            img: "user/4.jpg",
            name: "Quinn Flynn",
            key: "****-****-****-9497",
            first_used: "2023-04-16",
            last_used: "2023-10-02",
            status: "Suspended"
        },
        {
            id: 17,
            img: "user/5.jpg",
            name: "Charde Marshall",
            key: "****-****-****-6741",
            first_used: "2023-06-21",
            last_used: "2023-09-30",
            status: "Active"
        },
        {
            id: 18,
            img: "user/6.jpg",
            name: "Haley Kennedy",
            key: "****-****-****-3597",
            first_used: "2023-08-01",
            last_used: "2023-10-20",
            status: "Inactive"
        },
        {
            id: 19,
            img: "user/7.jpg",
            name: "Tatyana Fitzpatrick",
            key: "****-****-****-1965",
            first_used: "2023-07-07",
            last_used: "2023-09-18",
            status: "Active"
        },
        {
            id: 20,
            img: "user/8.jpg",
            name: "Michael Silva",
            key: "****-****-****-1581",
            first_used: "2023-01-30",
            last_used: "2023-10-10",
            status: "Suspended"
        },
        {
            id: 21,
            img: "user/9.jpg",
            name: "Paul Byrd",
            key: "****-****-****-3059",
            first_used: "2023-03-22",
            last_used: "2023-09-10",
            status: "Active"
        },
        {
            id: 22,
            img: "user/10.jpg",
            name: "Gloria Little",
            key: "****-****-****-1721",
            first_used: "2023-04-05",
            last_used: "2023-10-12",
            status: "Active"
        },
        {
            id: 23,
            img: "user/2.png",
            name: "Bradley Greer",
            key: "****-****-****-2558",
            first_used: "2023-06-03",
            last_used: "2023-08-19",
            status: "Inactive"
        },
        {
            id: 24,
            img: "user/5.jpg",
            name: "Dai Rios",
            key: "****-****-****-2290",
            first_used: "2023-05-12",
            last_used: "2023-10-03",
            status: "Active"
        },
        {
            id: 25,
            img: "user/1.jpg",
            name: "Jenette Caldwell",
            key: "****-****-****-1937",
            first_used: "2023-02-05",
            last_used: "2023-10-22",
            status: "Suspended"
        },
        {
            id: 26,
            img: "user/2.png",
            name: "Yuri Berry",
            key: "****-****-****-6154",
            first_used: "2023-04-21",
            last_used: "2023-10-11",
            status: "Active"
        },
        {
            id: 27,
            img: "user/3.jpg",
            name: "C. Vance",
            key: "****-****-****-8330",
            first_used: "2023-07-09",
            last_used: "2023-09-27",
            status: "Inactive"
        }
    ];
    