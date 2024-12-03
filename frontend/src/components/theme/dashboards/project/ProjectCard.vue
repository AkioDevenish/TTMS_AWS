<template>
    <Card1 :colClass="item.col" dropdown="true" headerTitle="true" :title="item.title" cardhaderClass="card-no-border pb-0"
        cardbodyClass="designer-card" v-for="(item, index) in projectdata" :key="index">

        <div>
            <div class="d-flex align-items-center gap-2">
                <div class="flex-shrink-0"><img :src="getImages(item.img)" alt="user"></div>
                <div class="flex-grow-1"><router-link to="/ecommerce/details/1">
                        <h5>{{ item.name }}</h5>
                    </router-link>
                    <p>{{ item.email }}</p>
                </div>
            </div>
            <div class="design-button">
                <button class="btn f-w-500 me-1" :class="item.class1">{{ item.design1 }}</button>
                <button class="btn  f-w-500" :class="item.class2">{{ item.design2 }}</button>
            </div>
            <div class="ratting-button">
                <div v-for="(items, index) in item.ratting" :key="index">
                    <div class="d-flex align-items-center gap-2 mb-0">
                        <div class="flex-shrink-0">
                            <p class="f-w-500">{{ items.rating }} </p>
                        </div>
                        <div class="flex-grow-1"><span class="f-w-500">{{ items.name }}</span></div>
                    </div>
                </div>

            </div>
            <h5 class="f-w-500 pb-2">Task Completed: {{ item.task }}</h5>
            <div class="progress  b-r-2" :class="item.progressclass">
                <div class="progress-bar" role="progressbar" :style="{ 'width': item.width }" aria-valuenow="10"
                    aria-valuemin="0" aria-valuemax="100"></div>
            </div>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { projectdata } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>