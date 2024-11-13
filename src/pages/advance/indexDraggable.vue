<template>
    <div class="container-fluid">
        <draggable class="row">
            <DraggableCard />
            <FooterCard />
        </draggable>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
const draggable = VueDraggableNext
const DraggableCard = defineAsyncComponent(() => import("@/components/theme/advance/draggable/DraggableCard.vue"))
const FooterCard = defineAsyncComponent(() => import("@/components/common/FooterCard.vue"))
</script>