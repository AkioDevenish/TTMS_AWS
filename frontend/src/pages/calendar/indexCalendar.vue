<template>
    <Card3 colClass="container-fluid calendar-basic">
        <CalenderView />
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const CalenderView = defineAsyncComponent(() => import("@/components/theme/calender/CalenderView.vue"))
</script>