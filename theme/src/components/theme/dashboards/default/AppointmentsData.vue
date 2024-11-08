<template>
    <Card1 colClass="col-xxl-5 col-xl-6 box-col-6 proorder-xl-7 proorder-md-8" headerTitle="true"
        title="Upcoming Appointments" cardhaderClass="card-no-border pb-0" cardbodyClass="appointments relative">
        <div class="row">
            <div class="col-5">
                <ul class="appointments-user">
                    <li class="d-flex align-items-center" v-for="(item, index) in upcoming" :key="index">
                        <div class="flex-shrink-0"><img :src="getImages(item.img)" alt=""></div>
                        <div class="flex-grow-1"><router-link to="/app/private_chat">
                                <h5>{{ item.name }}</h5>
                            </router-link>
                            <p>{{ item.date }}<span>({{ item.time }})</span></p>
                        </div>
                    </li>

                </ul>
            </div>
            <div class="col-7">
                <div class="datepicker-here mod" id="datepicker">
                    <Datepicker :inline="{ input: false }" auto-apply v-model="date" :format="format" />
                </div>
            </div>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { upcoming } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let date = ref<Date | null>(null);

let format = (date: Date | null): string => {
    if (date === null) {
        return '';
    }

    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();

    return ` ${day}/${month}/${year}`;
};

</script>