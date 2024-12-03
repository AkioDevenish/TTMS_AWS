<template>
    <Card1 colClass="col-xl-6 box-col-7 proorder-xl-9 proorder-md-10" headerTitle="true"
        title="Scheduled Updates" cardhaderClass="card-no-border pb-0" cardbodyClass="sales-product px-0 pb-0">

        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th></th>
                        <th>Time</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in saleproduct" :key="index">
                        <td>
                            <div class="d-flex align-items-center">
                                <h5>{{ item.name }}</h5>
                            </div>
                        </td>
                        <td></td>
                        <td> {{ item.time }}</td>
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
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>