<template>
    <div class="container-fluid">
        <div class="user-profile">
            <div class="row">
                <ProfileHeader />
                <UserTable />
                <ApiTable />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';

const ProfileHeader = defineAsyncComponent(() => import("@/components/theme/user/profile/ProfileHeader.vue"))
const UserTable = defineAsyncComponent(() => import("@/components/theme/user/profile/UserTable.vue"))
const ApiTable = defineAsyncComponent(() => import("@/components/theme/user/profile/ApiTable.vue"))
</script>