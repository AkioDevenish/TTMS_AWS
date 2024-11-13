<template>
    <form class="form-inline search-full col" action="#" method="get">
        <div class="form-group w-100">
            <div class="Typeahead Typeahead--twitterUsers">
                <div class="u-posRelative">
                    <input class="demo-input Typeahead-input form-control-plaintext w-100" type="text"
                        placeholder="Search Mofi .." name="q" title="" :class="filtered ? 'open' : ''" @keyup="searchTerm"
                        v-model="termss">
                    <div class="spinner-border Typeahead-spinner" role="status"><span class="sr-only">Loading...</span>
                    </div><vue-feather class="close-search" type="x"></vue-feather>
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
    </form>
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