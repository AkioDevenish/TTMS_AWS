<template>
    <Card1 colClass="col-xl-3 col-xl-40 col-md-6 proorder-md-1" dropdown="true" headerTitle="true" title="Project Status"
        cardhaderClass="card-no-border pb-0" cardbodyClass="project-status-col ">

        <div class="row">
            <div class="col-6" v-for="(item, index) in projectstatus" :key="index">
                <div class=" b-r-10" :class="item.btnclass">
                    <div class="upcoming-box" :class="item.upcoming">
                        <div class="upcoming-icon " :class="item.iconclass"> <img :src="getImages(item.img)" alt=""></div>
                        <h6>{{ item.title }}</h6>
                        <p>{{ item.desc }}</p>
                    </div>
                </div>
            </div>

        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { projectstatus } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>