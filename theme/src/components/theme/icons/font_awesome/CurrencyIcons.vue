<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="Currency Icons">
        <div class="row icon-lists">
            <div class="col-sm-6 col-md-4 col-xl-3" v-for="(cur, index) in currencyicons" :key="index"
                v-on:click="icon_bar(cur.name)">
                <i class="" :class="'fa fa-' + cur.name"></i>fa-{{ cur.name }}
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
let currencyicons = ref([{ name: 'bitcoin' }, { name: 'btc' }, { name: 'cny' }, { name: 'dollar' }, { name: 'eur' }, { name: 'euro' }, { name: 'gbp' }, { name: 'inr' }, { name: 'jpy' }, { name: 'krw' }, { name: 'money' }, { name: 'rmb' }, { name: 'rouble' }, { name: 'rub' }, { name: 'ruble' }, { name: 'rupee' }, { name: 'try' }, { name: 'turkish-lira' }, { name: 'usd' }, { name: 'won' }, { name: 'yen' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>
