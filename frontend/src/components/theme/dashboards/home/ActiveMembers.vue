<template>
    <Card1 colClass="col-xl-6 col-lg-6 col-md-6 order-5" 
        headerTitle="true"
        title="Recent Users" 
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="active-members px-0 pb-0">
        <div class="table-responsive theme-scrollbar">
            <table class="table table-sm display mb-0" style="width:100%">
                <thead>
                    <tr>
                        <th class="py-2">User Info</th>
                        <th class="py-2">Email</th>
                        <th class="text-center py-2">Status</th>
                    </tr>
                </thead>
                <tbody v-if="loading">
                    <tr>
                        <td colspan="3" class="text-center">Loading users...</td>
                    </tr>
                </tbody>
                <tbody v-else-if="recentUsers.length">
                    <tr v-for="(user, index) in recentUsers" :key="index">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="flex-grow-1">
                                    <h5 class="mb-0">{{ (user as any).username || `${(user as any).first_name} ${(user as any).last_name}`.trim() }}</h5>
                                    <span class="text-muted">{{ (user as any).role || ((user as any).is_superuser ? 'Admin' : (user as any).is_staff ? 'Staff' : 'User') }}</span>
                                </div>
                            </div>
                        </td>
                        <td>{{ (user as any).email }}</td>
                        <td>
                            <p class="members-box text-center" :class="(user as any).status === 'Active' ? 'bg-light-success' : 'bg-light-danger'">
                                {{ (user as any).status }}
                            </p>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="3" class="text-center">No users found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, onUnmounted, computed, defineProps } from 'vue'
import { useUserStore } from '@/store/user'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const userStore = useUserStore()

const props = defineProps({
  users: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    required: true
  }
})

const recentUsers = computed(() => props.users.slice(0, 4))

let refreshInterval: number;

onMounted(async () => {
    await userStore.fetchUsers()
    refreshInterval = window.setInterval(() => userStore.fetchUsers(), 300000)
})

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval)
    }
})
</script>

<style scoped>
.members-box {
    padding: 4px 8px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
}
.bg-light-success {
    background-color: #e6fff3;
    color: #51bb25;
}
.bg-light-danger {
    background-color: #fff5f5;
    color: #dc3545;
}
</style>