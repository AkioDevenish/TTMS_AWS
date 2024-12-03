<template>
    <Card3 colClass="col-sm-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Basic Tree" :desc="desc">
        <div class="tree-container">
            <treeview :nodes="nodes" :config="config"></treeview>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import treeview from "vue3-treeview";
import "vue3-treeview/dist/style.css";
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the dynamic tree view with checkboxes.")
let nodes = ref({
    id1: {
        text: "Admin",
        children: ["id11", "id12"],
    },
    id11: {
        text: "Assets",
        children: ["id113", "id118"],
    },
    id12: {
        text: "Default",
        children: ["id131", "id122"],
    },
    id111: {
        text: "CSS",
        children: ["id114", "id115"],
    },
    id114: {
        text: "Css One",
    },
    id115: {
        text: "Css Two",
    },
    id113: {
        text: "Js",
        children: ["id116", "id117"],
    },
    id116: {
        text: "Js One"
    },
    id117: {
        text: "Js Two"
    },
    id118: {
        text: "Scss",
        children: ["id119"]
    },
    id119: {
        text: "Sub Child",
        children: ["id120", "id121"]
    },
    id120: {
        text: "Sub File"
    },
    id121: {
        text: "Sub File"
    },
    id131: {
        text: "Dashboard"
    },
    id122: {
        text: "Typography"
    },
    id2: {
        text: "index file",
    },
});

let config = ref({
    roots: ["id1", "id2"],

});
</script>