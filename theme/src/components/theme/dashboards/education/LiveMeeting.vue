<template>
    <Card1 colClass="col-xl-4 col-md-6 proorder-md-5" dropdown="true" headerTitle="true" title="Live Meeting"
        cardhaderClass="card-no-border pb-0" cardbodyClass="live-meet" meet="true">
        <div class="live-metting"> <img class="img-fluid" src="@/assets/images/dashboard-4/metting/teacher.png" alt="">
            <div class="star-img"><img class="img-fluid" v-for="(item, index) in meting" :key="index"
                    :src="getImages(item.img)" alt=""></div>
        </div>
        <ul>
            <li>
                <h5 class="text-truncate"> <span>Class: </span>Technique of Drawing in One Line</h5>
            </li>
            <li>
                <h5 class="text-truncate"> <span>Batch: </span>GDM (2/3) </h5>
            </li>
            <li><a href="https://support.pixelstrap.com/ " target="_blank">
                    <h5 class="font-primary text-truncate"> <span>Class Link: </span>https://support.pixelstrap.com/
                    </h5>
                </a></li>
        </ul>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { meting } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>