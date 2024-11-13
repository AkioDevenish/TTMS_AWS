import { ref } from "vue"
interface tree {
    id: number;
    label: string;
    nodes?: Node[];
}
interface Node {
    id: number;
    label: string;
    nodes?: Node[];
}
export let menu = ref<tree[]>([
    {
        id: 1,
        label: "Applications",
        nodes: [
            {
                id: 1,
                label: "Ecommerce",
                nodes: [
                    {
                        id: 1,
                        label: "Product"
                    },
                    {
                        id: 2,
                        label: "Cart"
                    },
                    {
                        id: 3,
                        label: "Invoice"
                    }
                ],
            },
            {
                id: 2,
                label: "Default",
                nodes: [
                    {
                        id: 1,
                        label: "Users-profile",
                    },
                    {
                        id: 2,
                        label: "Users-edit",
                    },
                    {
                        id: 3,
                        label: "Users-cards",
                    },
                ],
            },
            {
                id: 3,
                label: "Default",
                nodes: [
                    {
                        id: 1,
                        label: "Chat-app",
                    },
                    {
                        id: 2,
                        label: "Video-chat",
                    }
                ],
            },
        ],
    },
    {
        id: 2,
        label: "Components",
        nodes: [
            {
                id: 1,
                label: "UI-Kits",
                nodes: [
                    {
                        id: 1,
                        label: "Typography"
                    },
                    {
                        id: 2,
                        label: "Avatars"
                    },
                    {
                        id: 3,
                        label: "Grid"
                    }
                ],
            },
            {
                id: 2,
                label: "Bonus-UI",
                nodes: [
                    {
                        id: 1,
                        label: "Toasts",
                    },
                    {
                        id: 2,
                        label: "Rating",
                    },
                    {
                        id: 3,
                        label: "Pagination",
                    },
                ],
            },
            {
                id: 3,
                label: "Charts",
                nodes: [
                    {
                        id: 1,
                        label: "Apex-chart",
                    },
                    {
                        id: 2,
                        label: "Google-chart",
                    },
                    {
                        id: 3,
                        label: "Echarts",
                    }
                ],
            },
        ],
    },
    {
        id: 3,
        label: "Miscellaneous",
        nodes: [
            {
                id: 1,
                label: "Gallery",
                nodes: [
                    {
                        id: 1,
                        label: "Gallery-grid"
                    },
                    {
                        id: 2,
                        label: "Gallery-grid-desc"
                    },
                    {
                        id: 3,
                        label: "Masonry-gallery"
                    }
                ],
            },
            {
                id: 2,
                label: "Blog",
                nodes: [
                    {
                        id: 1,
                        label: "Blog-details",
                    },
                    {
                        id: 2,
                        label: "Blog-single",
                    },
                    {
                        id: 3,
                        label: "Add-post",
                    },
                ],
            },
            {
                id: 3,
                label: "Editors",
                nodes: [
                    {
                        id: 1,
                        label: "Summer-note",
                    },
                    {
                        id: 2,
                        label: "CK-editor",
                    },
                    {
                        id: 3,
                        label: "MDE-editor",
                    }
                ],
            },
        ],
    }
])

export let tree = ref<tree[]>([
    {
        id: 1,
        label: "Applications",
        nodes: [
            {
                id: 1,
                label: "Ecommerce",
                nodes: [
                    {
                        id: 1,
                        label: "Product"
                    },
                    {
                        id: 2,
                        label: "Cart"
                    },
                    {
                        id: 3,
                        label: "Invoice"
                    }
                ],
            },
            {
                id: 2,
                label: "Default",
                nodes: [
                    {
                        id: 1,
                        label: "Users-profile",
                    },
                    {
                        id: 2,
                        label: "Users-edit",
                    },
                    {
                        id: 3,
                        label: "Users-cards",
                    },
                ],
            },
            {
                id: 3,
                label: "Default",
                nodes: [
                    {
                        id: 1,
                        label: "Chat-app",
                    },
                    {
                        id: 2,
                        label: "Video-chat",
                    }
                ],
            },
        ],
    },
    {
        id: 2,
        label: "Components",
        nodes: [
            {
                id: 1,
                label: "UI-Kits",
                nodes: [
                    {
                        id: 1,
                        label: "Typography"
                    },
                    {
                        id: 2,
                        label: "Avatars"
                    },
                    {
                        id: 3,
                        label: "Grid"
                    }
                ],
            },
            {
                id: 2,
                label: "Bonus-UI",
                nodes: [
                    {
                        id: 1,
                        label: "Toasts",
                    },
                    {
                        id: 2,
                        label: "Rating",
                    },
                    {
                        id: 3,
                        label: "Pagination",
                    },
                ],
            },
            {
                id: 3,
                label: "Charts",
                nodes: [
                    {
                        id: 1,
                        label: "Apex-chart",
                    },
                    {
                        id: 2,
                        label: "Google-chart",
                    },
                    {
                        id: 3,
                        label: "Echarts",
                    }
                ],
            },
        ],
    },
    {
        id: 3,
        label: "Miscellaneous",
        nodes: [
            {
                id: 1,
                label: "Gallery",
                nodes: [
                    {
                        id: 1,
                        label: "Gallery-grid"
                    },
                    {
                        id: 2,
                        label: "Gallery-grid-desc"
                    },
                    {
                        id: 3,
                        label: "Masonry-gallery"
                    }
                ],
            },
            {
                id: 2,
                label: "Blog",
                nodes: [
                    {
                        id: 1,
                        label: "Blog-details",
                    },
                    {
                        id: 2,
                        label: "Blog-single",
                    },
                    {
                        id: 3,
                        label: "Add-post",
                    },
                ],
            },
            {
                id: 3,
                label: "Editors",
                nodes: [
                    {
                        id: 1,
                        label: "Summer-note",
                    },
                    {
                        id: 2,
                        label: "CK-editor",
                    },
                    {
                        id: 3,
                        label: "MDE-editor",
                    }
                ],
            },
        ],
    }
])