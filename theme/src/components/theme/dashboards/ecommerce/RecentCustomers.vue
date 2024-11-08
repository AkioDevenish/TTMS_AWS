<template>
    <Card1 colClass="col-xl-3 col-lg-5 col-sm-6" dropdown="true" headerTitle="true" title="Recent Customers"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 ">
        <ul class="recent-customers">
            <li class="d-flex align-items-center gap-2" v-for="(item, index) in customers" :key="index">
                <div class="flex-shrink-0"><img :src="getImages(item.img)" alt=""></div>
                <div class="flex-grow-1"><router-link to="/ecommerce/cart">
                        <h5>{{ item.name }}</h5>
                    </router-link>
                    <p class="text-truncate">{{ item.ids }}<span :class="item.textclass">{{ item.text }}</span></p>
                </div>
                <div class="active-status active-online"></div>
                <div class="recent-text">
                    <h5>${{ item.price }}</h5>
                    <p>{{ item.min }}</p>
                </div>
            </li>

        </ul>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { customers } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>