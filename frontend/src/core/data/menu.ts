export interface MenuItem {
  headTitle1?: string;
  headTitle2?: string;
  title?: string;
  icon?: string;
  icon1?: string;
  type: string;
  badgeType?: string;
  badgeValue?: string | number;
  active?: boolean;
  isPinned?: boolean;
  path?: string;
  children?: MenuItem[];
  bookmark?: boolean;
  requireRole?: string;
  admin?: number;
}

export const menu: MenuItem[] = [
  // {
  //   headTitle1: "General",
  //   headTitle2: "Dashboards, AWS Creation",
  //   type: "headtitle"
  // },
  // {
  //   title: "Dashboards",
  //   icon: "stroke-home",
  //   icon1: "fill-home",
  //   type: "sub",
  //   badgeType: "light-primary",
  //   active: false,
  //   isPinned: false,
  //   children: [
  //     {
  //       path: "/dashboards/Main_Dashboard",
  //       title: "Main Dashboard",
  //       type: "link"
  //     },


  //   ]
  // },

  // api key navigation block
  {
    headTitle1: "General",
    headTitle2: "",
    type: "headtitle"
  },
  {
    path: "/dashboard",
    title: "Dashboard",
    isPinned: false,
    icon: "stroke-home",
    icon1: "fill-home",
    type: "link"
  },

  // aws stations block
  {
    headTitle1: "Stations",
    headTitle2: "Ready to use apps",
    type: "headtitle"
  },
  {
    title: "Weather Stations",
    icon: "stroke-charts",
    icon1: "fill-charts",
    type: "sub",
    badgeType: "light-info",
    isPinned: false,
    active: false,
    children: [
      {
        path: "/stations/AWS_OTT_Hyrdomet",
        title: "OTT-Hydromet",
        type: "link"
      },

      {
        path: "/stations/AWS_Barani",
        title: "Barani",
        type: "link"
      },
      {
        path: "/stations/AWS_Zentra",
        title: "Zentra",
        type: "link"
      },
      {
        path: "/stations/AWS_3D_Paws",
        title: "3D-Paws",
        type: "link"
      },
  
   

    ]
  },
  {
    path: "/stations/create",
    title: "Create New AWS",
    icon: "stroke-form",
    icon1: "fill-form",
    type: "link",
    admin: 1
  },

  // api key navigation block
  {
    headTitle1: "API Management",
    headTitle2: "Ready to use apps",
    type: "headtitle",
    admin: 1
  },
  {
    path: "/pages/api",
    title: "API Key",
    isPinned: false,
    icon: "stroke-others",
    icon1: "fill-others",
    type: "link",
    admin: 1
  },

  // miscellaneous block
  {
    headTitle1: "Miscellaneous",
    headTitle2: "Miscellaneous",
    type: "headtitle"
  },
  {
    path: "/app/private_chat",
    title: "Chat",
    isPinned: false,
    icon: "stroke-chat",
    icon1: "fill-chat",
    type: "link"
  },
  {
    path: "/pages/knowledgebase",
    title: "Documentation",
    isPinned: false,
    icon: "stroke-to-do",
    icon1: "fill-to-do",
    type: "link"
  },

  // system management block
  {
    headTitle1: "System Management",
    headTitle2: "System Management",
    type: "headtitle"
  },
  {
    path: "/pages/users_management",
    title: "User Management",
    isPinned: false,
    icon: "stroke-user",
    icon1: "fill-user",
    type: "link",
    admin: 1
  }
]