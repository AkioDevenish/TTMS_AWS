import { defineStore } from "pinia";
import { ref, onMounted, watch } from "vue";
import { menu } from "@/core/data/menu";
import { useRoute } from 'vue-router'

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
    title: string;

}

export const useMenuStore = defineStore("menu", () => {

    let data = ref(menu)
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

        const searchval = term.toLowerCase()

        data.value.filter((menuItems: any) => {

            if (menuItems.title?.toLowerCase().includes(term) && menuItems.type === 'link') {
                items.push(menuItems);
            }
            menuItems.children?.filter((subItems: any) => {
                if (subItems.title?.toLowerCase().includes(term) && subItems.type === 'link') {
                    subItems.icon1 = menuItems.icon1
                    items.push(subItems);

                }
                if (!subItems.children) return false;
                subItems.children?.filter((suSubItems: any) => {
                    if (suSubItems.title?.toLowerCase().includes(term)) {
                        suSubItems.icon1 = menuItems.icon1
                        items.push(suSubItems);
                    }
                })

            })
            searchData.value = items;
        })
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
