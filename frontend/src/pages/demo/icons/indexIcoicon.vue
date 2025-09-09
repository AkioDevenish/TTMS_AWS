<template>
    <div class="container-fluid">
        <div class="row">
            <AbstractIcon @selected="icon_bar" />
            <AnimalIcon @selected="icon_bar" />
            <BrandIcons @selected="icon_bar" />
            <BusinessIcons @selected="icon_bar" />
            <ChartIcons @selected="icon_bar" />
            <ConstructionIcons @selected="icon_bar" />
            <CurrencyIcons @selected="icon_bar" />
            <DeviceIcons @selected="icon_bar" />
            <DirectionalIcons @selected="icon_bar" />
            <EducationIcons @selected="icon_bar" />
            <EmoticonIcons @selected="icon_bar" />
            <FiletypeIcons @selected="icon_bar" />
            <FoodIcons @selected="icon_bar" />
            <KidsIcons @selected="icon_bar" />
            <LawIcons @selected="icon_bar" />
            <MathematicalIcons @selected="icon_bar" />
            <MedicalIcons @selected="icon_bar" />
            <MobileIcons @selected="icon_bar" />
            <MultimediaIcons @selected="icon_bar" />
            <PaymentIcons @selected="icon_bar" />
            <PersonIcons @selected="icon_bar" />
            <SearchIcons @selected="icon_bar" />
            <SocialIcons @selected="icon_bar" />
            <SportIcons @selected="icon_bar" />
            <TextIcons @selected="icon_bar" />
            <TransportIcons @selected="icon_bar" />
            <TravelIcons @selected="icon_bar" />
            <WeatherIcons @selected="icon_bar" />
            <WebIcons @selected="icon_bar" />
        </div>
    </div>
    <div class="icon-hover-bottom p-fixed fa-fa-icon-show-div" :class="{ 'opecity-0': !icon_bar_status }"
        :style="[icon_bar_status ? { 'display': 'block' } : { 'display': 'none' }]">
        <div class="container-fluid">
            <div class="row">
                <div class="icon-popup">
                    <div class="close-icon" v-on:click="close_icon_bar"><i class="icofont icofont-close"></i></div>
                    <div class="icon-first"><i class="fa-2x" :class="[select_icon.class]"></i></div>
                    <div class="icon-class">
                        <label class="icon-title">Class</label><span>icon-drupal</span>
                    </div>
                    <div class="icon-last icon-last">
                        <label class="icon-title">Markup</label>
                        <div class="form-inline">
                            <div class="form-group">
                                <input class="inp-val form-control m-r-10" type="text" ref="text" :value="select_icon.tag">
                                <button class="btn btn-primary notification" v-on:click="copy_icon">Copy text</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
import { icon_bar_status, select_icon, } from "@/composables/common/flagIcon"
const AbstractIcon = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/AbstractIcon.vue"))
const AnimalIcon = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/AnimalIcon.vue"))
const BrandIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/BrandIcons.vue"))
const BusinessIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/BusinessIcons.vue"))
const ChartIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/ChartIcons.vue"))
const ConstructionIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/ConstructionIcons.vue"))
const CurrencyIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/CurrencyIcons.vue"))
const DeviceIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/DeviceIcons.vue"))
const DirectionalIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/DirectionalIcons.vue"))
const EducationIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/EducationIcons.vue"))
const FiletypeIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/FiletypeIcons.vue"))
const EmoticonIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/EmoticonIcons.vue"))
const FoodIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/FoodIcons.vue"))
const KidsIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/KidsIcons.vue"))
const LawIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/LawIcons.vue"))
const MathematicalIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/MathematicalIcons.vue"))
const MedicalIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/MedicalIcons.vue"))
const MobileIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/MobileIcons.vue"))
const MultimediaIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/MultimediaIcons.vue"))
const PaymentIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/PaymentIcons.vue"))
const PersonIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/PersonIcons.vue"))
const SearchIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/SearchIcons.vue"))
const SocialIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/SocialIcons.vue"))
const SportIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/SportIcons.vue"))
const TextIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/TextIcons.vue"))
const TransportIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/TransportIcons.vue"))
const TravelIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/TravelIcons.vue"))
const WeatherIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/WeatherIcons.vue"))
const WebIcons = defineAsyncComponent(() => import("@/components/theme/icons/ico_icon/WebIcons.vue"))

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
function icon_bar(icon: string) {
    select_icon.value.class = 'icofont icofont-' + icon;
    select_icon.value.tag = '<i class="icofont icofont-' + icon + '"></i>';
    icon_bar_status.value = true;
}
function close_icon_bar() {
    icon_bar_status.value = false;
}
function copy_icon() {
    toast.info('Code Copied to clipboard! ', {
        hideProgressBar: true, autoClose: 2000, theme: 'colored', position: 'bottom-right',
    });
    navigator.clipboard.writeText(select_icon.value.tag);
    document.execCommand('copy');
}
</script>