<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="Multimedia">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-6 col-lg-4" v-for="(mm, index) in multimedia" :key="index"
                v-on:click="icon_bar(mm.name)">
                <i class="icofont" :class="'icofont-' + mm.name"></i>{{ mm.name }}
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { multimedia } from "@/composables/common/flagIcon"
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

function icon_bar(icon: string) {
    emit('selected', icon);

}
</script>
<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>