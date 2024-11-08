<template>
    <Card1 colClass="col-xxl-3 col-xl-6 col-md-5 box-col-6 proorder-xl-6 proorder-md-7" dropdown="true" headerTitle="true"
        title="Notifications" cardhaderClass="card-no-border pb-0">

        <ul class="notification-box">
            <li class="d-flex" v-for="(item, index) in notificationbox" :key="index">
                <div class="flex-shrink-0" :class="item.bgclass"><img :src="getImages(item.img)" alt="Wallet"></div>
                <div class="flex-grow-1"> <router-link to="/app/private_chat">
                        <h5>{{ item.title }}</h5>
                    </router-link>
                    <p class="text-truncate">{{ item.desc }}</p>
                </div><span>{{ item.date }}</span>
            </li>

        </ul>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { notificationbox } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>