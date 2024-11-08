<template>
    <Card1 colClass="col-xl-5 col-md-6 proorder-xl-1 proorder-md-1" cardClass="profile-greeting p-0">
        <div class="img-overlay">
            <h1>Good day, Lena Miller</h1>
            <p>Welcome to the Mofi family! We are delighted that you have visited our dashboard.</p><router-link class="btn"
                to="/">Go Premium</router-link>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>