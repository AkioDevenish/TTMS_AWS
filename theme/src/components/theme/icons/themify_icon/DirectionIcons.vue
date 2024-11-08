<template>
    <Card3 colClass="col-sm-12" title="Arrows & Direction Icons" headerTitle="true">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-6 col-lg-4" v-for="(di, index) in directional" :key="index"
                v-on:click="icon_bar(di.name)">
                <i class="" :class="di.name"></i>{{ di.name }}
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineEmits, defineAsyncComponent } from 'vue';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let customAnimation = {
    enter: "animated bounce",
    exit: "animated bounce",
}
let emit = defineEmits(['selected'])
let icon_bar_status = ref<boolean>(false)
let select_icon = {
    class: '',
    tag: ''
}
let directional = ref([{ name: 'icon-arrow-up' }, { name: 'icon-arrow-right' }, { name: 'icon-arrow-left' }, { name: 'icon-arrow-down' }, { name: 'icon-arrows-vertical' }, { name: 'icon-arrows-horizontal' }, { name: 'icon-angle-up' }, { name: 'icon-angle-right' }, { name: 'icon-angle-left' }, { name: 'icon-angle-down' }, { name: 'icon-angle-double-up' }, { name: 'icon-angle-double-right' }, { name: 'icon-angle-double-left' }, { name: 'icon-angle-double-down' }, { name: 'icon-move' }, { name: 'icon-fullscreen' }, { name: 'icon-arrow-top-right' }, { name: 'icon-arrow-top-left' }, { name: 'icon-arrow-circle-up' }, { name: 'icon-arrow-circle-right' }, { name: 'icon-arrow-circle-left' }, { name: 'icon-arrow-circle-down' }, { name: 'icon-arrows-corner' }, { name: 'icon-split-v' }, { name: 'icon-split-v-alt' }, { name: 'icon-split-h' }, { name: 'icon-hand-point-up' }, { name: 'icon-hand-point-right' }, { name: 'icon-hand-point-left' }, { name: 'icon-hand-point-down' }, { name: 'icon-back-right' }, { name: 'icon-back-left' }, { name: 'icon-exchange-vertical' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>
<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>