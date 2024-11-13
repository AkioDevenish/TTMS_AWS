interface tick {
    title: string,
    number: string,
    progress: string
}
interface item {
    id: number,
    img: string,
    username: string,
    organization:string,
    lastlogin:string,
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
        username: "Elana White",
        organization: "National Oceanic and Atmospheric Administration (NOAA)",
        lastlogin: "2024-11-01",  // Example last login
        status: "Active"
    },
    {
        id: 2,
        img: "user/2.png",
        username: "Tiger Nixon",
        organization: "World Meteorological Organization (WMO)",
        lastlogin: "2024-10-28",
        status: "Inactive"
    },
    {
        id: 3,
        img: "user/3.jpg",
        username: "Genelia Winters",
        organization: "European Space Agency (ESA)",
        lastlogin: "2024-10-15",
        status: "Active"
    },
    {
        id: 4,
        img: "user/4.jpg",
        username: "Robbert Winters",
        organization: "UK Met Office",
        lastlogin: "2024-10-25",
        status: "Active"
    },
    {
        id: 5,
        img: "user/5.jpg",
        username: "Garrett Winters",
        organization: "National Weather Service (NWS)",
        lastlogin: "2024-10-18",
        status: "Inactive"
    },
    {
        id: 6,
        img: "user/6.jpg",
        username: "Ashton Cox",
        organization: "MeteoGroup",
        lastlogin: "2024-11-02",
        status: "Active"
    },
    {
        id: 7,
        img: "user/7.jpg",
        username: "Cedric Kelly",
        organization: "National Aeronautics and Space Administration (NASA)",
        lastlogin: "2024-10-20",
        status: "Active"
    },
    {
        id: 8,
        img: "user/8.jpg",
        username: "Helly Shah",
        organization: "CIMSS (Cooperative Institute for Meteorological Satellite Studies)",
        lastlogin: "2024-10-30",
        status: "Inactive"
    },
    {
        id: 9,
        img: "user/9.jpg",
        username: "Airi Satou",
        organization: "Japan Meteorological Agency (JMA)",
        lastlogin: "2024-10-29",
        status: "Active"
    },
    {
        id: 10,
        img: "user/10.jpg",
        username: "Hendri Feyol",
        organization: "Bureau of Meteorology (Australia)",
        lastlogin: "2024-09-25",
        status: "Inactive"
    },
    {
        id: 11,
        img: "user/1.jpg",
        username: "Herrod Chandler",
        organization: "India Meteorological Department (IMD)",
        lastlogin: "2024-11-01",
        status: "Active"
    },
    {
        id: 12,
        img: "user/5.jpg",
        username: "Rhona Davidson",
        organization: "Canadian Meteorological Centre (CMC)",
        lastlogin: "2024-10-18",
        status: "Active"
    },
    {
        id: 13,
        img: "user/1.jpg",
        username: "Colleen Hurst",
        organization: "National Center for Atmospheric Research (NCAR)",
        lastlogin: "2024-10-22",
        status: "Active"
    },
    {
        id: 14,
        img: "user/2.png",
        username: "Sonya Frost",
        organization: "Singapore Meteorological Service",
        lastlogin: "2024-10-10",
        status: "Inactive"
    },
    {
        id: 15,
        img: "user/3.png",
        username: "Jena Gaines",
        organization: "NOAA National Hurricane Center (NHC)",
        lastlogin: "2024-10-05",
        status: "Active"
    },
    {
        id: 16,
        img: "user/4.jpg",
        username: "Quinn Flynn",
        organization: "National Meteorological Service of Mexico (SMN)",
        lastlogin: "2024-09-30",
        status: "Inactive"
    },
    {
        id: 17,
        img: "user/5.jpg",
        username: "Charde Marshall",
        organization: "US Geological Survey (USGS)",
        lastlogin: "2024-10-12",
        status: "Active"
    },
    {
        id: 18,
        img: "user/6.jpg",
        username: "Haley Kennedy",
        organization: "Australian Bureau of Meteorology",
        lastlogin: "2024-11-05",
        status: "Active"
    },
    {
        id: 19,
        img: "user/7.jpg",
        username: "Tatyana Fitzpatrick",
        organization: "Swiss Meteorological Institute (MeteoSwiss)",
        lastlogin: "2024-09-15",
        status: "Inactive"
    },
    {
        id: 20,
        img: "user/8.jpg",
        username: "Michael Silva",
        organization: "Korean Meteorological Administration (KMA)",
        lastlogin: "2024-11-02",
        status: "Active"
    },
    {
        id: 21,
        img: "user/9.jpg",
        username: "Paul Byrd",
        organization: "South African Weather Service",
        lastlogin: "2024-10-01",
        status: "Inactive"
    },
    {
        id: 22,
        img: "user/10.jpg",
        username: "Gloria Little",
        organization: "Meteorological Service of New Zealand (MetService)",
        lastlogin: "2024-10-17",
        status: "Active"
    },
    {
        id: 23,
        img: "user/2.png",
        username: "Bradley Greer",
        organization: "AccuWeather",
        lastlogin: "2024-09-30",
        status: "Inactive"
    },
    {
        id: 24,
        img: "user/5.jpg",
        username: "Dai Rios",
        organization: "China Meteorological Administration (CMA)",
        lastlogin: "2024-10-12",
        status: "Active"
    },
    {
        id: 25,
        img: "user/1.jpg",
        username: "Jenette Caldwell",
        organization: "U.S. Forest Service (USFS)",
        lastlogin: "2024-10-28",
        status: "Inactive"
    },
    {
        id: 26,
        img: "user/2.png",
        username: "Yuri Berry",
        organization: "UK Met Office",
        lastlogin: "2024-10-25",
        status: "Active"
    },
    {
        id: 27,
        img: "user/3.jpg",
        username: "C. Vance",
        organization: "Météo-France",
        lastlogin: "2024-11-01",
        status: "Active"
    }
];
