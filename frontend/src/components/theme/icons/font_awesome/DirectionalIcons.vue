<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="Directional Icons">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-4 col-xl-3" v-for="(dire, index) in directionalicons" :key="index"
                v-on:click="icon_bar(dire.name)">
                <i class="" :class="'fa fa-' + dire.name"></i>fa-{{ dire.name }}
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
let directionalicons = ref([{ name: 'angle-double-down' }, { name: 'angle-double-left' }, { name: 'angle-double-right' }, { name: 'angle-double-up' }, { name: 'angle-down' }, { name: 'angle-left' }, { name: 'angle-right' }, { name: 'angle-up' }, { name: 'arrow-circle-down' }, { name: 'arrow-circle-left' }, { name: 'arrow-circle-o-down' }, { name: 'arrow-circle-o-left' }, { name: 'arrow-circle-o-right' }, { name: 'arrow-circle-o-up' }, { name: 'arrow-circle-right' }, { name: 'arrow-circle-up' }, { name: 'arrow-down' }, { name: 'arrow-left' }, { name: 'arrow-right' }, { name: 'arrow-up' }, { name: 'arrows' }, { name: 'arrows-alt' }, { name: 'arrows-h' }, { name: 'arrows-v' }, { name: 'caret-down' }, { name: 'caret-left' }, { name: 'caret-right' }, { name: 'caret-up' }, { name: 'caret-square-o-left' }, { name: 'caret-square-o-right' }, { name: 'caret-square-o-up' }, { name: 'caret-square-o-down' }, { name: 'chevron-circle-down' }, { name: 'chevron-circle-left' }, { name: 'chevron-circle-right' }, { name: 'chevron-circle-up' }, { name: 'chevron-down' }, { name: 'chevron-left' }, { name: 'chevron-right' }, { name: 'chevron-up' }, { name: 'hand-o-down' }, { name: 'hand-o-left' }, { name: 'hand-o-right' }, { name: 'hand-o-up' }, { name: 'long-arrow-down' }, { name: 'long-arrow-left' }, { name: 'long-arrow-right' }, { name: 'long-arrow-up' }, { name: 'toggle-down' }, { name: 'toggle-left' }, { name: 'toggle-right' }, { name: 'toggle-up' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>