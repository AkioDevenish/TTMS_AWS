<template>
     <Card3 colClass="col-md-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"   title="Pagination With Icons"
        :desc="desc">
        <nav aria-label="Page navigation example">
            <ul class="pagination pagination-secondary pagin-border-secondary">
                <li class="page-item"><a class="page-link" href="javascript:void(0)" aria-label="Previous"><span
                            aria-hidden="true">«</span><span class="sr-only">Previous</span></a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">1</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">2</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">3</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">...</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">20</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)" aria-label="Next"><span
                            aria-hidden="true">»</span><span class="sr-only">Next</span></a></li>
            </ul>
        </nav>
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use an icon or symbol in place of text for some pagination links.")
</script>