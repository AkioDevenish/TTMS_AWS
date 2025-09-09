<template>
    <div class="container-fluid">
        <div class="user-profile">
            <UserProfile />
        </div>
    </div>
</template>
<script lang="ts" setup>

import { ref, defineAsyncComponent, onMounted } from 'vue';
const UserProfile = defineAsyncComponent(() => import("@/components/theme/advance/tour/UserProfile.vue"))

</script>