<template>
    <Card3 colClass="col-xxl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Pagination Alignment"
        :desc="desc">
         <nav aria-label="Page navigation example" v-for="(item, index) in size" :key="index">
            <ul class="pagination  pagination-warning pagin-border-info" :class="item.size">
                <li class="page-item"><a class="page-link" href="javascript:void(0)">Previous</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">1</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">2</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">3</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">Next</a></li>
            </ul>
        </nav>
    </Card3>
</template>
<script lang="ts" setup>
import {size } from "@/core/data/advance"
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use <code>[pagination-lg/pagination-md/pagination-lg]</code> for additional sizes.")

</script>