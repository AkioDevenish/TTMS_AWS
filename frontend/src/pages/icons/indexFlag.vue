<template>
    <div class="container-fluid">
        <div class="row">

            <Card3 colClass="col-sm-12" titleClass="m-b-0" headerTitle="true" title="Flag Icons">
                <div class="row icon-lists flag-icons">
                    <div class="col-12 col-sm-6 col-xl-4" v-for="(fi, index) in flag_icons" :key="index"
                        v-on:click="icon_bar(fi.abbrivation)">
                        <div class="d-flex">
                            <i class="flag-icon" :class="'flag-icon-' + fi.abbrivation"></i>
                            <div class="flex-grow-1  align-self-center">
                                <h5 v-text="fi.abbrivation"></h5>
                                <h6 class="mt-0" v-text="fi.name"></h6>
                            </div>
                        </div>
                    </div>
                </div>
            </Card3>
        </div>
    </div>
    <div class="icon-hover-bottom p-fixed fa-fa-icon-show-div" :class="{ 'opecity-0': !icon_bar_status }"
        :style="[icon_bar_status ? { 'display': 'block' } : { 'display': 'none' }]">
        <div class="container-fluid">
            <div class="row">
                <div class="icon-popup">
                    <div class="close-icon" v-on:click="close_icon_bar">
                        <i class="icofont icofont-close"></i>
                    </div>
                    <div class="icon-first">
                        <i class="fa-2x" :class="[select_icon.class]"></i>
                    </div>
                    <div class="icon-class">
                        <label class="icon-title">Class</label>
                        <span>icon-drupal</span>
                    </div>
                    <div class="icon-last icon-last">
                        <label class="icon-title">Markup</label>
                        <div class="form-inline">
                            <div class="form-group">
                                <input class="inp-val form-control m-r-10" type="text" ref="copy_text"
                                    :value="select_icon.tag" />
                                <button class="btn btn-primary notification" @click="copy_icon">Copy text</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { icon_bar_status, select_icon, flag_icons } from "@/composables/common/flagIcon"
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
function icon_bar(icon: string) {

    select_icon.value.class = 'flag-icon flag-icon-' + icon;
    select_icon.value.tag = '<i class="flag-icon flag-icon-' + icon + '"></i>';

    icon_bar_status.value = true;
}
function close_icon_bar() {
    icon_bar_status.value = false;
}
function copy_icon() {
    toast.info(' Code Copied to clipboard! ', {
        hideProgressBar: true, autoClose: 2000, theme: 'colored', position: 'bottom-right',
    });
    navigator.clipboard.writeText(select_icon.value.tag);
    document.execCommand('copy');

}
</script>