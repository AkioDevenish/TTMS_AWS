interface MenuItem {
    headTitle1?: string;
    headTitle2?: string;
    title?: string;
    icon?: string;
    icon1?: string;
    type: string;
    badgeType?: string;
    active?: boolean;
    isPinned?: boolean;
    path?: string;
    children?: MenuItem[];
    bookmark?: boolean;
}

export const menu: MenuItem[] = [
    {
        headTitle1: "General",
        headTitle2: "Dashboards, AWS Creation",
        type: "headtitle"
    },
    {
        title: "Dashboards",
        icon: "stroke-home",
        icon1: "fill-home",
        type: "sub",
        badgeType: "light-primary",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/dashboards/Main_Dashboard",
                title: "Main Dashboard",
                type: "link"
            },

            {
                path: "/dashboards/Create_New_AWS",
                title: "Create New AWS",
                type: "link"
            },
        ]
    },
  
    {
        headTitle1: "Stations",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },
    {
        title: "Weather Stations",
        icon: "stroke-project",
        icon1: "fill-project",
        type: "sub",
        badgeType: "light-info",
        isPinned: false,
        active: false,
        children: [
      
            {
                path: "/stations/AWS_Barani",
                title: "Barani",
                type: "link"
            },
            {
                path: "/stations/AWS_3D_Paws",
                title: "3D-Paws",
                type: "link"
            },
            {
                path: "/stations/AWS_Sutron",
                title: "Sutron",
                type: "link"
            },
            {
                path: "/stations/AWS_OTT_Hyrdomet",
                title: "OTT-Hydromet",
                type: "link"
            },
            {
                path: "/stations/AWS_Zentra",
                title: "Zentra",
                type: "link"
            },
  
        ]
    },

    {
        headTitle1: "API Management",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },
    {
        path: "/pages/api",
        title: "API Key",
        isPinned: false,
        icon: "stroke-support-tickets",
        icon1: "fill-support-tickets",
        type: "link"
    },
    
    {
        headTitle1: "User Management",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },

    {
        path: "/pages/users_management",
        title: "User Management",
        isPinned: false,
        icon: "stroke-support-tickets",
        icon1: "fill-support-tickets",
        type: "link"
    }
]