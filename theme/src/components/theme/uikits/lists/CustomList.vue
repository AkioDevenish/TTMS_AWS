<template>
    <Card3 colClass="col-md-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Custom content lists"
        :desc="desc">
        <div class="list-group main-lists-content">
            <a class="list-group-item list-group-item-action " :class="item.class" v-for="(item, index) in customs"
                :key="index" href="#" aria-current="true">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div class="list-wrapper"><img class="list-img" :src="getImages(item.img)" alt="profile">
                        <div class="list-content">
                            <h5>{{ item.name }}</h5>
                            <p>{{ item.email }}</p>
                        </div>
                    </div><small>{{ item.day }}</small>
                </div>
                <p class="mb-1">{{ item.desc }}</p><small class="text-muted">{{ item.follow }}</small>
            </a>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { customs } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.list-group-item</code> through make custom design of all lists.")
</script>