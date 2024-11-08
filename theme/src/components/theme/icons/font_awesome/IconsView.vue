<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="20 Icons">
        <div class="row icon-lists">
            <div class="col-sm-6 col-md-4 col-xl-3" v-for="(ico, index) in icons" :key="index"
                v-on:click="icon_bar(ico.name)">
                <i class="" :class="'fa fa-' + ico.name"></i>fa fa-{{ ico.name }}
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
let icons = ref([{ name: 'bluetooth' }, { name: 'bluetooth-b' }, { name: 'codiepie' }, { name: 'credit-card-alt' }, { name: 'edge' }, { name: 'fort-awesome' }, { name: 'hashtag' }, { name: 'mixcloud' }, { name: 'modx' }, { name: 'pause-circle' }, { name: 'pause-circle-o' }, { name: 'percent' }, { name: 'product-hunt' }, { name: 'reddit-alien' }, { name: 'scribd' }, { name: 'shopping-bag' }, { name: 'shopping-basket' }, { name: 'stop-circle' }, { name: 'stop-circle-o' }, { name: 'usb' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>
