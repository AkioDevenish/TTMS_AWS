<template>
      <Card3 colClass="col-sm-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"  title="With Icons Breadcrumb"
        :desc="desc">
         <ol class="breadcrumb bg-white p-l-0">
            <li class="breadcrumb-item"><a href="javascript:void(0)"><i class="fa fa-home"></i></a></li>
            <li class="breadcrumb-item active">Bonus Ui</li>
        </ol>
        <ol class="breadcrumb bg-white m-b-0 p-b-0 p-l-0">
            <li class="breadcrumb-item"><a href="javascript:void(0)"><i class="fa fa-home"></i></a></li>
            <li class="breadcrumb-item">Bonus Ui</li>
            <li class="breadcrumb-item active">Breadcrumb</li>
        </ol>
      </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("You can set icons breadcrumb using <code>.breadcrumb </code>class.")

</script>