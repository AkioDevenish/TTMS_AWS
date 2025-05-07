<template>
    <div v-if="isAdmin" class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12" title="Create New User" headerTitle="true" cardhaderClass="title-header">
                <NewUser />
            </Card3>
        </div>
    </div>
    <div v-else>
        <h3>Access Denied</h3>
        <p>You don't have permission to access this page.</p>
    </div>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const NewUser = defineAsyncComponent(() => import("@/components/theme/users_management/createuser/NewUser.vue"))
const authStore = useAuthStore()
const { isAdmin } = authStore

onMounted(() => {
  // Use isAdmin directly
})
</script>