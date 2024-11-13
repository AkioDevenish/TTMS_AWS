<template>
    <div class="form-group w-100">
        <div class="Typeahead Typeahead--twitterUsers">
            <div class="u-posRelative d-flex align-items-center">
                <svg class="search-bg svg-color">
                    <use href="@/assets/svg/icon-sprite.svg#search"></use>
                </svg>
                <input class="demo-input py-0 Typeahead-input form-control-plaintext w-100" type="text"
                    placeholder="Search Mofi .." :class="filtered ? 'open' : ''" @keyup="searchTerm" v-model="termss">
            </div>
            <div class="custom-scrollbar" :class="searchResult ? 'Typeahead-menu is-open ' : 'Typeahead-menu '" v-if="menuItems.length">
                <div class="ProfileCard u-cf" v-for="(menuItem, index) in menuItems.slice(0, 8)" :key="index">
                    <div class="ProfileCard-avatar header-search">

                        <svg>
                            <use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1}`"></use>
                        </svg>
                    </div>
                    <div class="ProfileCard-details">
                        <div class="ProfileCard-realName">
                            <span @click="removeFix()"><router-link :to="{ path: menuItem.path }" class="realname">{{
                                menuItem.title
                            }}</router-link></span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="custom-scrollbar" :class="searchResultEmpty ? 'Typeahead-menu is-open' : 'Typeahead-menu'">
                <div class="tt-dataset tt-dataset-0">
                    <div class="EmptyMessage"> Your search turned up 0 results. Opps There are no result found. </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useMenuStore } from "@/store/menu";
import { storeToRefs } from "pinia";
import { ref, watch } from 'vue'
let filtered = ref<boolean>(false);
let termss = ref<string>("");
let store = useMenuStore();
let { searchData: menuItems } = storeToRefs(store);

let searchOpen = store.searchOpen;
let searchResult = ref<boolean>(false);
let searchResultEmpty = ref<boolean>(false);
watch(
    () => [menuItems, termss],
    () => {
        termss.value ? addFix() : removeFix();
        if (!menuItems.value.length) searchResultEmpty.value = true;
        else searchResultEmpty.value = false;
    },
    { deep: true },
);
function searchTerm() {
    store.searchTerm(termss.value);
}
function addFix() {

    searchResult.value = true;
}
function removeFix() {
    searchResult.value = false;
    termss.value = "";
}
function collapseFilter() {
    filtered.value = !filtered.value;
}

</script>