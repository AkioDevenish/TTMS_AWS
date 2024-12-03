<template>
    <Card3 colClass="col-sm-12" headerTitle="true" title="Brand Icons">
        <div class="row icon-lists">

            <div class="col-sm-6 col-md-4 col-xl-3" v-for="(brand, index) in branddicons" :key="index"
                v-on:click="icon_bar(brand.name)">
                <i class="" :class="'fa fa-' + brand.name"></i>fa-{{ brand.name }}
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
let branddicons = ref([{ name: 'adn' }, { name: 'android' }, { name: 'apple' }, { name: 'behance' }, { name: 'behance-square' }, { name: 'bitbucket' }, { name: 'bitbucket-square' }, { name: 'bitcoin' }, { name: 'btc' }, { name: 'codepen' }, { name: 'css3' }, { name: 'delicious' }, { name: 'deviantart' }, { name: 'digg' }, { name: 'dribbble' }, { name: 'dropbox' }, { name: 'drupal' }, { name: 'empire' }, { name: 'facebook' }, { name: 'facebook-square' }, { name: 'flickr' }, { name: 'foursquare' }, { name: 'ge' }, { name: 'git' }, { name: 'git-square' }, { name: 'github' }, { name: 'github-alt' }, { name: 'github-square' }, { name: 'gittip' }, { name: 'google' }, { name: 'google-plus' }, { name: 'google-plus-square' }, { name: 'hacker-news' }, { name: 'html5' }, { name: 'instagram' }, { name: 'joomla' }, { name: 'jsfiddle' }, { name: 'linkedin' }, { name: 'linkedin-square' }, { name: 'linux' }, { name: 'maxcdn' }, { name: 'openid' }, { name: 'pagelines' }, { name: 'pied-piper' }, { name: 'pied-piper-alt' }, { name: 'pinterest' }, { name: 'pinterest-square' }, { name: 'qq' }, { name: 'ra' }, { name: 'rebel' }, { name: 'reddit' }, { name: 'reddit-square' }, { name: 'renren' }, { name: 'share-alt' }, { name: 'share-alt-square' }, { name: 'skype' }, { name: 'slack' }, { name: 'soundcloud' }, { name: 'spotify' }, { name: 'stack-exchange' }, { name: 'stack-overflow' }, { name: 'steam' }, { name: 'steam-square' }, { name: 'stumbleupon' }, { name: 'stumbleupon-circle' }, { name: 'tencent-weibo' }, { name: 'trello' }, { name: 'tumblr' }, { name: 'tumblr-square' }, { name: 'twitter' }, { name: 'twitter-square' }, { name: 'vimeo-square' }, { name: 'vine' }, { name: 'vk' }, { name: 'wechat' }, { name: 'weibo' }, { name: 'weixin' }, { name: 'windows' }, { name: 'wordpress' }, { name: 'xing' }, { name: 'xing-square' }, { name: 'yahoo' }, { name: 'youtube' }, { name: 'youtube-play' }, { name: 'youtube-square' }])
function icon_bar(icon: string) {
    emit('selected', icon);

}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/vendors/animate.scss"
</style>