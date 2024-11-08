<template>
     <Card3 colClass="col-md-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"   title="Pagination With Active And Disabled"
        :desc="desc">
        <nav aria-label="...">
            <ul class="pagination pagination-success pagin-border-success">
                <li class="page-item disabled"><a class="page-link" href="javascript:void(0)" tabindex="-1">Previous</a>
                </li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">1</a></li>
                <li class="page-item active"><a class="page-link" href="javascript:void(0)">2 <span
                            class="sr-only">(current)</span></a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">3</a></li>
                <li class="page-item"><a class="page-link" href="javascript:void(0)">Next</a></li>
            </ul>
        </nav>
     </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use <code>.disabled </code>for links that appear un-clickable and<code> .active</code> to indicate the current page.")
</script>