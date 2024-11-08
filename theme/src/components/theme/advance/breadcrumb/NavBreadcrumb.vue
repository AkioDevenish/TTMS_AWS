<template>
     <Card3 colClass="col-sm-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"  title="Variation Of Breadcrumb" 
        :desc="desc">
         <nav class="breadcrumb breadcrumb-no-divider mb-0 gap-2"><a class="breadcrumb-item mb-1 mb-xl-0"
                href="javascript:void(0)">Home -></a><a class="breadcrumb-item ps-0 mb-1 mb-xl-0"
                href="javascript:void(0)">Tables -></a><a class="breadcrumb-item ps-0 mb-1 mb-xl-0"
                href="javascript:void(0)">Bootstrap Tables -></a><span class="breadcrumb-item active ps-0">Basic
                Tables</span></nav>
     </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("You can set variations breadcrumb using <code>.breadcrumb </code>class through any icons sets.")

</script>