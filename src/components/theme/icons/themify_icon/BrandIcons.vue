<template>
    <Card3 colClass="col-sm-12" title="Brand Icons" headerTitle="true">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-6 col-lg-4" v-for="(br, index) in brand" :key="index"
                v-on:click="icon_bar(br.name)">
                <i class="" :class="br.name"></i>{{ br.name }}
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineEmits, defineAsyncComponent } from 'vue';
let Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const customAnimation = ref<{ enter: string, exit: string }>({
    enter: "animated bounce",
    exit: "animated bounce",
})
let emit = defineEmits(['selected'])
let icon_bar_status = ref<boolean>(false)
let select_icon = {
    class: '',
    tag: ''
}
let brand = ref([{ name: 'icon-flickr' }, { name: 'icon-flickr-alt' }, { name: 'icon-instagram' }, { name: 'icon-google' }, { name: 'icon-github' }, { name: 'icon-facebook' }, { name: 'icon-dropbox' }, { name: 'icon-dropbox-alt' }, { name: 'icon-dribbble' }, { name: 'icon-apple' }, { name: 'icon-android' }, { name: 'icon-yahoo' }, { name: 'icon-trello' }, { name: 'icon-stack-overflow' }, { name: 'icon-soundcloud' }, { name: 'icon-sharethis' }, { name: 'icon-sharethis-alt' }, { name: 'icon-reddit' }, { name: 'icon-microsoft' }, { name: 'icon-microsoft-alt' }, { name: 'icon-linux' }, { name: 'icon-jsfiddle' }, { name: 'icon-joomla' }, { name: 'icon-html5' }, { name: 'icon-css3' }, { name: 'icon-drupal' }, { name: 'icon-wordpress' }, { name: 'icon-tumblr' }, { name: 'icon-tumblr-alt' }, { name: 'icon-skype' }, { name: 'icon-youtube' }, { name: 'icon-vimeo' }, { name: 'icon-vimeo-alt' }, { name: 'icon-twitter' }, { name: 'icon-twitter-alt' }, { name: 'icon-linkedin' }, { name: 'icon-pinterest' }, { name: 'icon-pinterest-alt' }, { name: 'icon-themify-logo' }, { name: 'icon-themify-favicon' }, { name: 'icon-themify-favicon-alt' }])
function icon_bar(icon: string) {

    emit('selected', icon);
}
</script>
<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>