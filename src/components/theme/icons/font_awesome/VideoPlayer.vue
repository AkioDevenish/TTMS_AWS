<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="Video Player Icons">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-4 col-xl-3" v-for="(video, index) in videoicons" :key="index"
                v-on:click="icon_bar(video.name)">
                <i class="" :class="'fa fa-' + video.name"></i>fa-{{ video.name }}
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
let videoicons = ref([{ name: 'arrows-alt' }, { name: 'backward' }, { name: 'compress' }, { name: 'eject' }, { name: 'expand' }, { name: 'fast-backward' }, { name: 'fast-forward' }, { name: 'forward' }, { name: 'pause' }, { name: 'play' }, { name: 'play-circle' }, { name: 'play-circle-o' }, { name: 'step-backward' }, { name: 'step-forward' }, { name: 'stop' }, { name: 'youtube-play' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>