<template>
    <Card1 colClass="col-xxl-5 col-xl-7 box-col-7 proorder-xl-9 proorder-md-10" dropdown="true" headerTitle="true"
        title="Sales by Product" cardhaderClass="card-no-border pb-0" cardbodyClass="sales-product px-0 pb-0">

        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>Files Name</th>
                        <th>Amount</th>
                        <th>% Sold</th>
                        <th>Progressbar</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in saleproduct" :key="index">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="flex-shrink-0"><img :src="getImages(item.img)" alt=""></div>
                                <div class="flex-grow-1"><router-link to="/ecommerce/product_list">
                                        <h5>{{ item.name }}</h5>
                                    </router-link></div>
                            </div>
                        </td>
                        <td> {{ item.amonunt }}</td>
                        <td> {{ item.sold }}</td>
                        <td>
                            <div class="progress  b-r-2" :class="item.progressclass">
                                <div class="progress-bar" role="progressbar" :style="{ 'width': item.width }"
                                    aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { saleproduct } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>