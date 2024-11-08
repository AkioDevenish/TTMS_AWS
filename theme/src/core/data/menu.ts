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
        headTitle2: "Dashboards,Widgets & Layout.",
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
                path: "/dashboards/dashboard_default",
                title: "Homepage",
                type: "link"
            },
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
        title: "Widgets",
        icon: "stroke-widget",
        icon1: "fill-widget",
        type: "sub",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/widgets/general",
                title: "General",
                type: "link"
            },
            {
                path: "/widgets/Chart",
                title: "Charts",
                type: "link"
            }
        ]
    },

    {
        headTitle1: "Applications",
        headTitle2: "Ready to use apps",
        type: "headtitle"
    },
    {
        title: "project",
        icon: "stroke-project",
        icon1: "fill-project",
        type: "sub",
        badgeType: "light-info",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/project/project_list",
                title: "Project List",
                type: "link"
            },
            {
                path: "/project/project_create",
                title: "Create new",
                type: "link"
            }
        ]
    },
    {
        path: "/app/file_manager",
        title: "File Manager",
        icon: "stroke-file",
        icon1: "fill-file",
        type: "link",
        isPinned: false,
        active: false
    },
    {
        path: "/app/kanban_board",
        title: "Kanban Board",
        icon: "stroke-board",
        icon1: "fill-board",
        type: "link",
        badgeType: "light-danger",
        isPinned: false,
        active: false
    },
    {
        title: "Ecommerce",
        icon: "stroke-ecommerce",
        icon1: "fill-ecommerce",
        type: "sub",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/ecommerce/add_product",
                title: "Add Product",
                type: "link"
            },
            {
                path: "/ecommerce/product",
                title: "Product",
                type: "link"
            },
            {
                path: "/ecommerce/details/1",
                title: "Product Page",
                type: "link"
            },

            {
                path: "/ecommerce/product_list",
                title: "Product List",
                type: "link"
            },
            {
                path: "/ecommerce/payment_details",
                title: "Payment Details",
                type: "link"
            },
            {
                path: "/ecommerce/order_history",
                title: "Order History",
                type: "link"
            },
            {
                title: "Invoices",
                type: "sub",
                children: [
                    {
                        path: "/ecommerce/invoice_1",
                        title: "Invoice-1",
                        type: "link",
                    },
                    {
                        path: "/ecommerce/invoice_2",
                        title: "Invoice-2",
                        type: "link",
                    },
                    {
                        path: "/ecommerce/invoice_3",
                        title: "Invoice-3",
                        type: "link",
                    },
                    {
                        path: "/ecommerce/invoice_4",
                        title: "Invoice-4",
                        type: "link",
                    },
                    {
                        path: "/ecommerce/invoice_5",
                        title: "Invoice-5",
                        type: "link",
                    },
                    {
                        path: "/ecommerce/invoice_6",
                        title: "Invoice-6",
                        type: "link",
                    }
                ]
            },
            {
                path: "/ecommerce/cart",
                title: "Cart",
                type: "link"
            },
            {
                path: "/ecommerce/wishlist",
                title: "Wishlist",
                type: "link"
            },
            {
                path: "/ecommerce/checkout",
                title: "Checkout",
                type: "link"
            },
            {
                path: "/ecommerce/pricing",
                title: "Pricing",
                type: "link"
            }
        ]
    },
    {
        path: "/app/letter_box",
        icon: "stroke-email",
        icon1: "fill-email",
        title: "Letter Box",
        isPinned: false,
        type: "link"
    },
    {
        title: "Chat",
        icon: "stroke-chat",
        icon1: "fill-chat",
        type: "sub",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/app/private_chat",
                title: "Private Chat",
                type: "link"
            },
            {
                path: "/app/group_chat",
                title: "Group Chat",
                type: "link"
            }
        ]
    },
    {
        title: "Users",
        icon: "stroke-user",
        icon1: "fill-user",
        type: "sub",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/users/profile",
                title: "Users Profile",
                type: "link"
            },
            {
                path: "/users/edit",
                title: "Users Edit",
                type: "link"
            },
            {
                path: "/users/cards",
                title: "Users Cards",
                type: "link"
            }
        ]
    },
    {
        path: "/app/bookmark",
        title: "Bookmark",
        icon: "stroke-bookmark",
        icon1: "fill-bookmark",
        type: "link",
        isPinned: false,
        bookmark: true
    },
    {
        path: "/app/contact",
        title: "Contacts",
        icon: "stroke-contact",
        icon1: "fill-contact",
        type: "link",
        isPinned: false,
        bookmark: true
    },
    {
        path: "/app/task",
        title: "Tasks",
        icon: "stroke-task",
        icon1: "fill-task",
        isPinned: false,
        type: "link"
    },
    {
        path: "/app/calendar",
        title: "Calendar",
        icon: "stroke-calendar",
        icon1: "fill-calender",
        type: "link",
        isPinned: false,
        bookmark: true
    },
    {
        path: "/pages/social_app",
        title: "Social App",
        icon: "stroke-social",
        icon1: "fill-social",
        isPinned: false,
        type: "link"
    },
    {
        path: "/app/todo",
        title: "Todo",
        icon: "stroke-to-do",
        icon1: "fill-to-do",
        isPinned: false,
        type: "link"
    },

    {
        path: "/pages/search",
        title: "Search Results",
        icon: "stroke-search",
        icon1: "fill-search",
        isPinned: false,
        type: "link"
    },

    {
        headTitle1: "Forms & Table",
        headTitle2: "Ready to use froms & tables ",
        type: "headtitle"
    },
    {
        title: "Forms",
        icon: "stroke-form",
        icon1: "fill-form",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                title: "Form Controls",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/form/validation",
                        title: "Form Validation",
                        type: "link"
                    },
                    {
                        path: "/form/base_inputs",
                        title: "Base Inputs",
                        type: "link"
                    },
                    {
                        path: "/form/checkbox_radio",
                        title: "Checkbox & Radio",
                        type: "link"
                    },
                    {
                        path: "/form/input_groups",
                        title: "Input Groups",
                        type: "link"
                    },
                    {
                        path: "/form/input_mask",
                        title: "Input Mask",
                        type: "link"
                    },
                    {
                        path: "/form/mega_options",
                        title: "Mega Options",
                        type: "link"
                    }
                ]
            },
            {
                title: "Form Widgets",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/form/datepicker",
                        title: "Datepicker",
                        type: "link"
                    },
                    {
                        path: "/form/touchspin",
                        title: "Touchspin",
                        type: "link"
                    },
                    {
                        path: "/form/select2",
                        title: "Select2",
                        type: "link"
                    },
                    {
                        path: "/form/switch",
                        title: "Switch",
                        type: "link"
                    },

                    {
                        path: "/form/typeahead",
                        title: "Typeahead",
                        type: "link"
                    },
                    {
                        path: "/form/clipboard",
                        title: "Clipboard",
                        type: "link"
                    }
                ]
            },
            {
                title: "Form Layout",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/form/form_wizard",
                        title: "Form Wizard 1",
                        icon: "file-text",
                        type: "link"
                    },
                    {
                        path: "/form/form_wizard_two",
                        title: "Form Wizard 2",
                        icon: "file-text",
                        type: "link"
                    },
                    {
                        path: "/form/two_actor",
                        title: "Two Factor",
                        icon: "file-text",
                        type: "link"
                    }
                ]
            }
        ]
    },
    {
        title: "Tables",
        icon: "stroke-table",
        icon1: "fill-table",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                title: "Bootstrap Tables",
                path: "/table/basic",
                type: "link",
                active: false
            },
            {
                path: "/table/table_components",
                title: "Table Components",
                type: "link"
            },
            {
                path: "/table/datatable_basic",
                title: "Basic Init",
                type: "link"
            }
        ]
    },
    {
        headTitle1: "Components",
        headTitle2: "UI Components & Elements",
        type: "headtitle"
    },
    {
        title: "UI Kits",
        icon: "stroke-ui-kits",
        icon1: "fill-ui-kits",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/uikits/typography",
                title: "Typography",
                type: "link"
            },
            {
                path: "/uikits/avatars",
                title: "Avatars",
                type: "link"
            },
            {
                path: "/uikits/helper_classes",
                title: "Helper Classes",
                type: "link"
            },
            {
                path: "/uikits/grid",
                title: "Grid",
                type: "link"
            },
            {
                path: "/uikits/tag_pills",
                title: "Tag & Pills",
                type: "link"
            },
            {
                path: "/uikits/progress_bar",
                title: "Progress",
                type: "link"
            },
            {
                path: "/uikits/modal",
                title: "Modal",
                type: "link"
            },
            {
                path: "/uikits/alert",
                title: "Alert",
                type: "link"
            },
            {
                path: "/uikits/popover",
                title: "Popover",
                type: "link"
            },
            {
                path: "/uikits/tooltip",
                title: "Tooltip",
                type: "link"
            },
            {
                path: "/uikits/dropdown",
                title: "Dropdown",
                type: "link"
            },
            {
                path: "/uikits/accordion",
                title: "Accordian",
                type: "link"
            },
            {
                title: "Tabs",
                type: "link",
                path: "/uikits/tabs",
                active: false
            },
            {
                path: "/uikits/lists",
                title: "Lists",
                type: "link"
            }

        ]
    },
    {
        title: "Bonus UI",
        icon: "stroke-bonus-kit",
        icon1: "fill-bonus-kit",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/advance/scrollable",
                title: "Scrollable",
                type: "link"
            },
            {
                path: "/advance/tree",
                title: "Tree View",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/toasts",
                title: "Toasts",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/rating",
                title: "Rating",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/dropzone",
                title: "Dropzone",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/tour",
                title: "Tour",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/sweetalert",
                title: "SweetAlert2",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/animated_modal",
                title: "Animated Modal",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/owl_carousel",
                title: "Owl Carousel",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/ribbons",
                title: "Ribbons",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/pagination",
                title: "Pagination",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/breadcrumb",
                title: "Breadcrumb",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/range_slider",
                title: "Range Slider",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/image_cropper",
                title: "Image Cropper",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/basic_card",
                title: "Basic Card",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/creative_card",
                title: "Creative Card",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/draggable_card",
                title: "Draggable Card",
                icon: "folder-plus",
                type: "link"
            },
            {
                path: "/advance/timeline",
                title: "Timeline",
                icon: "folder-plus",
                type: "link"
            }
        ]
    },
    {
        title: "Animation",
        icon: "stroke-animation",
        icon1: "fill-animation",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/animation/animate",
                title: "Animate",
                type: "link"
            },
            {
                path: "/animation/aos_animation",
                title: "AOS Animation",
                type: "link"
            }
        ]
    },
    {
        title: "Icons",
        icon: "stroke-icons",
        icon1: "fill-icons",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/icons/flag",
                title: "Flag Icon",
                type: "link"
            },
            {
                path: "/icons/fontawesome",
                title: "Fontawesome Icon",
                type: "link"
            },
            {
                path: "/icons/ico",
                title: "Ico Icon",
                type: "link"
            },
            {
                path: "/icons/themify",
                title: "Themify Icon",
                type: "link"
            },
            {
                path: "/icons/feather_icon",
                title: "Feather Icon",
                type: "link"
            },
            {
                path: "/icons/whether",
                title: "Whether Icon",
                type: "link"
            }
        ]
    },

    {
        title: "Buttons",
        icon: "stroke-button",
        icon1: "fill-button",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/buttons/default_button",
                title: "Default Style",
                type: "link"
            },
            {
                path: "/buttons/flat",
                title: "Flat Style",
                type: "link"
            },
            {
                path: "/buttons/edge",
                title: "Edge Style",
                type: "link"
            },
            {
                path: "/buttons/raised",
                title: "Raised Style",
                type: "link"
            },
            {
                path: "/buttons/group",
                title: "Button Group",
                type: "link"
            }
        ]
    },
    {
        title: "Charts",
        icon: "stroke-charts",
        icon1: "fill-charts",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/chart/apexChart",
                title: "ApexChart",
                type: "link"
            },
            {
                path: "/chart/google",
                title: "Google Chart",
                type: "link"
            },
            {
                path: "/chart/chartist",
                title: "Chartist",
                type: "link"
            }
        ]
    },
    {
        headTitle1: "Pages",
        headTitle2: "All Neccesory Pages Added",
        type: "headtitle"
    },
    {
        path: "/pages/sample_page",
        title: "Sample page",
        icon: "stroke-sample-page",
        isPinned: false,
        icon1: "fill-sample-page",
        type: "link"
    },
    {
        path: "/pages/internationalization",
        title: "Internationalization",
        icon: "stroke-internationalization",
        icon1: "fill-internationalization",
        isPinned: false,
        type: "link"
    },
    {
        title: "Others",
        icon: "stroke-others",
        icon1: "fill-others",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                title: "Error Page",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/error_page1",
                        title: "Error 400",
                        type: "link"
                    },
                    {
                        path: "/error_page2",
                        title: "Error 401",
                        type: "link"
                    },
                    {
                        path: "/error_page3",
                        title: "Error 403",
                        type: "link"
                    },
                    {
                        path: "/error_page4",
                        title: "Error 404",
                        type: "link"
                    },
                    {
                        path: "/error_page5",
                        title: "Error 500",
                        type: "link"
                    },
                    {
                        path: "/error_page6",
                        title: "Error 503",
                        type: "link"
                    }
                ]
            },
            {
                title: "Authentication",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/auth/login",
                        title: "Login Simple",
                        type: "link",
                        active: false
                    },
                    {
                        path: "/authentication/login/one",
                        title: "Login with Image",
                        type: "link"
                    },
                    {
                        path: "/authentication/login/two",
                        title: "Login with Image Two",
                        type: "link"
                    },
                    {
                        path: "/authentication/login/validate",
                        title: "Login with validation",
                        type: "link"
                    },
                    {
                        path: "/authentication/login/tooltip",
                        title: "Login with tooltip",
                        type: "link"
                    },
                    {
                        path: "/authentication/login/sweetalert",
                        title: "Login with sweetalert",
                        type: "link"
                    },
                    {
                        path: "/auth/register",
                        title: "Register Simple",
                        type: "link"
                    },
                    {
                        path: "/authentication/register/one",
                        title: "Register with Image",
                        type: "link"
                    },
                    {
                        path: "/authentication/register/two",
                        title: "Register With Image Two",
                        type: "link"
                    },
                    {
                        path: "/authentication/unlock_user",
                        title: "Unlock User",
                        type: "link"
                    },
                    {
                        path: "/authentication/forget_password",
                        title: "Forget Password",
                        type: "link"
                    },
                    {
                        path: "/authentication/reset_password",
                        title: "Reset Password",
                        type: "link"
                    },
                    {
                        path: "/authentication/maintenance",
                        title: "Maintenance",
                        type: "link"
                    }
                ]
            },
            {
                title: "Coming Soon",
                icon: "bx:briefcase-alt",
                type: "sub",
                active: false,
                children: [
                    {
                        path: "/comingsoon/comingsoon_simple",
                        title: "Coming Simple",
                        type: "link"
                    },
                    {
                        path: "/comingsoon/comingsoon_image",
                        title: "Coming with Bg Image",
                        type: "link"
                    },
                    {
                        path: "/comingsoon/comingsoon_video",
                        title: "Coming with Bg video",
                        type: "link"
                    }
                ]
            }
        ]
    },
    {
        headTitle1: "Miscellaneous",
        headTitle2: "Bouns pages & apps",
        type: "headtitle"
    },
    {
        title: "Gallery",
        icon: "stroke-gallery",
        icon1: "fill-gallery",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/gallery/grid_gallery",
                title: "Grid Gallery",
                type: "link"
            },
            {
                path: "/gallery/gallery_desc",
                title: "Grid Gallery With Desc",
                type: "link"
            },
            {
                path: "/gallery/gallery_masonary",
                title: "Masonary Gallery",
                type: "link"
            },
            {
                path: "/gallery/gallery_masonary_desc",
                title: "Masonary Gallery Desc",
                type: "link"
            },
            {
                path: "/gallery/hover_effect",
                title: "Hover Effect",
                type: "link"
            }
        ]
    },

    {
        title: "Blog",
        icon: "stroke-blog",
        icon1: "fill-blog",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/blog/details",
                title: "Blog Details",
                type: "link"
            },
            {
                path: "/blog/single",
                title: "Blog Single",
                type: "link"
            },
            {
                path: "/blog/add_post",
                title: "Add Post",
                type: "link"
            }
        ]
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
        title: "Job Search",
        icon: "stroke-job-search",
        icon1: "fill-job-search",
        type: "sub",
        active: false,
        isPinned: false,
        children: [
            {
                path: "/job/card",
                title: "Card View",
                icon: "package",
                type: "link"
            },
            {
                path: "/job/list",
                title: "List View",
                icon: "package",
                type: "link"
            },
            {
                path: "/job/details/1",
                title: "Job Details",
                icon: "package",
                type: "link"
            },
            {
                path: "/job/apply/1",
                title: "Apply",
                icon: "package",
                type: "link"
            }
        ]
    },
    {
        title: "Learning",
        icon: "stroke-learning",
        icon1: "fill-learning",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/learning/list",
                title: "Learning List",
                type: "link"
            },
            {
                path: "/learning/details/1",
                title: "Detailed Course",
                type: "link"
            }
        ]
    },

    {
        title: "Maps",
        icon: "stroke-maps",
        icon1: "fill-maps",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/maps/vue_google_maps",
                title: "Google Maps",
                type: "link"
            },
            {
                path: "/maps/vue_leaflet_maps",
                title: "Vue Leaflet",
                type: "link"
            }
        ]
    },
    {
        title: "editor",
        icon: "stroke-editors",
        icon1: "fill-editors",
        type: "sub",
        isPinned: false,
        active: false,
        children: [
            {
                path: "/editor/ck_editor",
                title: "Ck Editor",
                type: "link"
            },
            {
                path: "/editor/simple_editor",
                title: "Simple Editor",
                type: "link"
            }
        ]
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