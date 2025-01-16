<template>
    <div v-if="isAdmin" class="container-fluid">
        <div class="row">
            <div class="d-flex justify-content-end mb-3">
                <router-link class="btn btn-primary" to="users_management/createuser">
                    <i data-feather="plus-square"></i> Create New User
                </router-link>
            </div>
            <Card3 colClass="col-sm-12" title="Users Management Overview" headerTitle="true" cardhaderClass="title-header"
                text="true" :desc="desc" :btnclass="'btn-primary'" >
                <SupportTable />
            </Card3>
        </div>
    </div>
    <div v-else>
        <h3>Access Denied</h3>
        <p>You don't have permission to access this page.</p>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue';
import { useAuth } from '@/composables/useAuth';
import { useUserManagement } from '@/composables/useUserManagement';

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/users_management/UserMTable.vue"))
const { requireAuth, isAdmin } = useAuth()
const { fetchUsers } = useUserManagement()

let desc = ref<string>("List Of User Accounts");

onMounted(async () => {
  const hasAccess = await requireAuth('admin')
  if (!hasAccess) return
  
  await fetchUsers()
})
</script>
