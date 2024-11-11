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
                path: "/dashboards/dashboard_education",
                title: "Atmos",
                type: "link"
            },
            {
                path: "/dashboards/dashboard_project",
                title: "Barani",
                type: "link"
            },
            {
                path: "/dashboards/dashboard_ecommerce",
                title: "3D-Paws",
                type: "link"
            },
            {
                path: "/dashboards/dashboard_education",
                title: "Sutron",
                type: "link"
            },
            {
                path: "/dashboards/dashboard_education",
                title: "OTT Hydromet",
                type: "link"
            }
  
        ]
    },

    {
        headTitle1: "API Management",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },




    {
        headTitle1: "Miscellaneous",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },


    {
        path: "/pages/faq",
        title: "FAQ",
        icon: "stroke-faq",
        icon1: "fill-faq",
        isPinned: false,
        type: "link"
    },

    {
        path: "/knowledgebase/knowledgebase",
        title: "Knowledgebase",
        type: "link",
        isPinned: false,
        icon: "stroke-knowledgebase",
        icon1: "fill-knowledgebase"
    },
    {
        path: "/pages/support",
        title: "Support Ticket",
        isPinned: false,
        icon: "stroke-support-tickets",
        icon1: "fill-support-tickets",
        type: "link"
    }
]