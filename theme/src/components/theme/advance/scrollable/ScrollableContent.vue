<template>
    <Card3 colClass="col-xxl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Scrollable Content"
        :desc="desc">
        <perfect-scrollbar class="vertical-scroll scroll-demo scroll-b-none" :settings="settings5">
            <div class="list-group main-lists-content">
                <a class="list-group-item list-group-item-action "
                    :class="item.actve ? 'active bg-primary' : 'list-hover-primary'" v-for="(item, index) in scrollable"
                    :key="index" href="#" aria-current="true">
                    <div class="list-wrapper gap-0"><img class="list-img" :src="getImages(item.img)" alt="profile">
                        <div class="list-content">
                            <h6 class="text-white">{{ item.name }}</h6>
                            <p>{{ item.email }}</p><small>{{ item.days }}</small>
                        </div>
                    </div>
                </a>
            </div>

        </perfect-scrollbar>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from "vue"
import { scrollable } from "@/core/data/scrollable"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.list-group-item </code>through made profile and with used <code>.vertical-scroll </code>.")
const settings5 = {
    maxScrollbarLength: 60,
    suppressScrollY: true,
    suppressScrollX: false
}
</script>