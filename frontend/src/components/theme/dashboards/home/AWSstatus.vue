<template>
    <Card1  dropdown="true" headerTitle="true" title="Automatic Weather Stations - Status"
        cardhaderClass="card-no-border pb-0" cardbodyClass="designer-card">
        <div>
            <div class="d-flex align-items-center gap-2">
                <div class="flex-shrink-0"><img src="@/assets/images/dashboard-2/user/16.png" alt="user"></div>
                <div class="flex-grow-1"><router-link to="/ecommerce/details/1">
                        <h5>Trinidad and Tobago Met Services</h5>
                    </router-link>
                    <p>metfeedback@gov.tt</p>
                </div>
            </div>
            <div class="design-button">
                <button class="btn bg-light-primary font-primary f-w-500 me-1" >T09 Brigand Hill</button>
                <button class="btn bg-light-secondary font-secondary f-w-500 me-1">T16 Lochmaben</button>
                <button class="btn bg-light-tertiary font-tertiary f-w-500 me-1">T18 Matura</button>
                <button class="btn bg-light-tertiary font-tertiary f-w-500 mt-1">T05 Mt. St. Benedict</button>

            </div>
            <div class="ratting-button">
                <div v-for="(item, index) in website" :key="index">
                    <div class="d-flex align-items-center gap-2 mb-0">
                        <div class="flex-shrink-0">
                            <p class="f-w-500">{{ item.number }} </p>
                        </div>
                        <div class="flex-grow-1"><span class="f-w-500">{{ item.title }}</span></div>
                    </div>
                </div>
            </div>
            <h5 class="f-w-500 pb-2">Estimated Maintenance Time: 3:48 </h5>
            <div class="progress progress-striped-primary">
                <div class="progress-bar" role="progressbar" style="width: 50%" aria-valuenow="10" aria-valuemin="0"
                    aria-valuemax="100"></div>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { website } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>