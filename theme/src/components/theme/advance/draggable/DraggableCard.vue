<template>
  <Card3 colClass="col-xxl-4 col-md-6" v-for="(items, index) in draggable" :key="index" :cardClass="items.cardclass"
    pre="true" preClass="f-m-light mt-1" headerTitle="true" :title="items.title" :desc="items.desc">
    <ul class="list-group">
      <li class="list-group-item" v-for="(item, index) in items.children" :key="index"
        :class="item.activeclass == true ? 'active bg-warning-light' : ''"> <i class="icofont icofont-arrow-right"></i>{{
          item.title }}</li>
    </ul>
  </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { draggable } from "@/core/data/advance"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
</script>