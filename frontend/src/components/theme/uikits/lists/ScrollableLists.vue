<template>
    <Card3 colClass="col-xxl-4" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Default lists" :desc="desc">
        <div class="list-group main-lists-content scrollbar-wrapper theme-scrollbar">
            <a class="list-group-item list-group-item-action" :class="item.class" v-for="(item, index) in scrollable"
                :key="index" href="#" aria-current="true">
                <div class="list-wrapper gap-0"><img class="list-img" :src="getImages(item.img)" alt="profile">
                    <div class="list-content">
                        <h6>{{ item.title }}</h6>
                        <p>{{ item.email }}</p><small>{{ item.day }}</small>
                    </div>
                </div>
            </a>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { scrollable } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the property <code>overflow:auto </code>through scrollable lists.")
</script>