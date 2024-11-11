<template>
    <Card1 cardClass="profile-greeting p-0">
        <div class="img-overlay">
            <h1 >Good day, Lena Miller</h1>
            <p>Welcome to the TTMS Automatic Weather Stations Dashboard! We are delighted that you have visited us.</p>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>