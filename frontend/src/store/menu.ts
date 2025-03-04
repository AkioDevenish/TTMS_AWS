import { defineStore } from "pinia";
import { ref, onMounted, watch } from "vue";
import { menu } from "@/core/data/menu";
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth';

interface searchdatas {
    icon1: string,
    icon2: string,
    path: string,
    title: string
}
interface search {
    icon1: string,
    icon2: string,
    path: string,
    title: string,
    bookmark: string
}
interface MenuItem {
    headTitle1?: string;
    headTitle2?: string;
    title?: string;
    path?: string;
    icon?: string;
    icon1?: string;
    type: string;
    children?: MenuItem[];
    isPinned?: boolean;
    requireRole?: string;
}

export const useMenuStore = defineStore("menu", () => {
    const { currentUser, isAdmin } = useAuth();
    console.log('currentUser', currentUser);
    console.log('isAdmin', isAdmin);
    let data = ref<MenuItem[]>([]);

    const filterMenuByRole = () => {
        console.log('MenuStore - Is Admin:', isAdmin.value);
        return menu.filter(item => {
            // Hide admin-only items for non-admin users
            if (item.requireRole === 'admin') {
                return isAdmin.value;
            }
            return true;
        });
    };

    onMounted(() => {
        data.value = filterMenuByRole();
    });

    watch(() => currentUser.value, () => {
        data.value = filterMenuByRole();
    });

    let togglesidebar = ref<boolean>(true);
    let activeoverlay = ref<boolean>(true);
    let customizer = ref<string>("");
    let searchData = ref<searchdatas[]>([]);
    let searchDatas = ref<search[]>([]);
    let searchOpen = ref<boolean>(false);
    let hideRightArrowRTL = ref<boolean>(false)
    let hideLeftArrowRTL = ref<boolean>(true)
    let hideRightArrow = ref<boolean>(true)
    let hideLeftArrow = ref<boolean>(true)
    let width = ref<number>(0)
    let height = ref<number>(0)
    let margin = ref<number>(0)
    let menuWidth = ref<number>(0)
    let searchKey = ref('')
    let perentName = ref<string | undefined>('')
    let subName = ref<string>('')
    let childName = ref<string | undefined>('')
    let bodyToggle = ref(false)
    let perentToggle = ref<boolean>(false)
    let subToggle = ref<boolean>(false)
    let childToggle = ref<boolean>(false)

    let active = ref<boolean>(false)


    onMounted(() => {
        if (window.innerWidth < 991) {
            togglesidebar.value = false
        }
    })
    function openActives() {
        active.value = !active.value
    }
    function togglePinned(item: any) {

        item.isPinned = !item.isPinned;
    };
    function toggle_sidebar() {
        togglesidebar.value = !togglesidebar.value;
        if (window.innerWidth < 991) {
            activeoverlay.value = true;
        } else {
            activeoverlay.value = false;
        }
        activeoverlay.value = false;
    }
    function subMenuToggle(Name: string) {
        perentName.value = perentName.value != Name ? Name : ""
        perentToggle.value = perentName.value != "" ? true : false
    }
    function subChildMenu(subTitle: string) {
        subName.value = subName.value != subTitle ? subTitle : ''
        subToggle.value = subName.value != "" ? true : false
    }
    function childMenu(childTitle: string) {
        childName.value = childName.value != childTitle ? childTitle : "";
        childToggle.value = childName.value != '' ? true : false

    }
    function searchTerm(term: any) {
        const items: any = [];
        const searchval = term.toLowerCase();

        // Early return for empty search
        if (!searchval) {
            searchData.value = [];
            return;
        }

        // Add user-related items to search results if they match
        const userRelatedItems = [
            {
                title: "Create New User",
                path: "/pages/users_management/createuser",
                icon1: "users",
                type: "link"
            },
            {
                title: "Profile",
                path: "/users/profile",
                icon1: "user",
                type: "link"
            }
        ];

        // Check if search term matches user-related keywords
        const userKeywords = ["user", "profile", "create"];
        if (userKeywords.some(keyword => searchval.includes(keyword))) {
            items.push(...userRelatedItems);
        }

        // Regular menu item search
        data.value.forEach((menuItems: any) => {
            if (menuItems.title?.toLowerCase().startsWith(searchval) && menuItems.type === 'link') {
                items.push(menuItems);
            }
            else if (menuItems.title?.toLowerCase().includes(searchval) && menuItems.type === 'link') {
                items.push(menuItems);
            }

            menuItems.children?.forEach((subItems: any) => {
                if (subItems.title?.toLowerCase().startsWith(searchval) && subItems.type === 'link') {
                    subItems.icon1 = menuItems.icon1;
                    items.push(subItems);
                }
                else if (subItems.title?.toLowerCase().includes(searchval) && subItems.type === 'link') {
                    subItems.icon1 = menuItems.icon1;
                    items.push(subItems);
                }

                subItems.children?.forEach((suSubItems: any) => {
                    if (suSubItems.title?.toLowerCase().startsWith(searchval)) {
                        suSubItems.icon1 = menuItems.icon1;
                        items.push(suSubItems);
                    }
                    else if (suSubItems.title?.toLowerCase().includes(searchval)) {
                        suSubItems.icon1 = menuItems.icon1;
                        items.push(suSubItems);
                    }
                });
            });
        });

        // Sort results
        items.sort((a: any, b: any) => {
            const aStarts = a.title.toLowerCase().startsWith(searchval);
            const bStarts = b.title.toLowerCase().startsWith(searchval);
            if (aStarts && !bStarts) return -1;
            if (!aStarts && bStarts) return 1;
            return 0;
        });

        searchData.value = items;
    }
    function searchterm(terms: any) {
        const items: any = [];

        const searchval = terms.toLowerCase()

        data.value.filter((menuItems: any) => {

            if (menuItems.title?.toLowerCase().includes(terms) && menuItems.type === 'link') {
                items.push(menuItems);
            }
            menuItems.children?.filter((subItems: any) => {
                if (subItems.title?.toLowerCase().includes(terms) && subItems.type === 'link') {
                    subItems.icon1 = menuItems.icon1
                    items.push(subItems);

                }
                if (!subItems.children) return false;
                subItems.children?.filter((suSubItems: any) => {
                    if (suSubItems.title?.toLowerCase().includes(terms)) {
                        suSubItems.icon1 = menuItems.icon1
                        items.push(suSubItems);
                    }
                })

            })
            searchDatas.value = items;
        })
    }


    onMounted(() => {
        data.value.filter((menuItem) => {
            if (menuItem.path) {
                if (menuItem.path == useRoute().path) {
                    perentName.value = menuItem.title
                }
            }
            else {
                menuItem.children?.filter((subItem) => {
                    if (subItem.path) {
                        if (subItem.path == useRoute().path) {
                            perentName.value = menuItem.title
                            childName.value = subItem.title
                        }
                    }
                    subItem.children?.filter((childItem) => {
                        if (childItem.path) {
                            if (childItem.path == useRoute().path) {
                                perentName.value = menuItem.title
                                childName.value = subItem.title
                            }
                        }
                    })
                })
            }
        })
    })
    return {
        data,
        togglesidebar,
        activeoverlay,
        toggle_sidebar,
        customizer,
        searchTerm,
        togglePinned,
        searchterm,
        searchData,
        searchOpen,
        hideRightArrowRTL,
        hideLeftArrowRTL,
        hideRightArrow,
        hideLeftArrow,
        width,
        height,
        margin,
        menuWidth,
        searchDatas,
        bodyToggle,
        subMenuToggle,
        subChildMenu,
        childMenu,
        perentName,
        subName,
        childName,
        perentToggle,
        subToggle,
        childToggle,
        openActives,
        active,
    };
});
