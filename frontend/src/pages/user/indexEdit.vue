<template>
    <div class="container-fluid">
        <div class="edit-profile">
            <div class="row justify-content-center">
                <UserProfile />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const UserProfile = defineAsyncComponent(() => import("@/components/theme/user/edit/UserProfile.vue"))
const EditProfile = defineAsyncComponent(() => import("@/components/theme/user/edit/EditProfile.vue"))
</script>