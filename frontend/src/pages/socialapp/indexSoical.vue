<template>
    <div class="container-fluid">
        <div class="user-profile social-app-profile">
            <SocialHeader />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const SocialHeader = defineAsyncComponent(() => import("@/components/theme/socialapp/SocialHeader.vue"))
</script>