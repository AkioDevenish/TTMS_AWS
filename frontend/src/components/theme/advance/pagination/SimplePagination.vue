<template>
     <Card3 colClass="col-md-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"  title="Default Pagination"
        :desc="desc">
         <nav aria-label="Page navigation example">
            <ul class="pagination pagination-primary pagin-border-primary">
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
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>('If the pagination component is used to navigate between a set of search results, an appropriate label could be <code>aria-label="Search results pages"</code>.')
</script>