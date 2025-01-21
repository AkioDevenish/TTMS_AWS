<template>
    <Card1 colClass="col-xl-12 col-md-12 proorder-xl-3 proorder-md-2" headerTitle="true"
        title="Recent Users" cardhaderClass="card-no-border pb-0" cardbodyClass="active-members px-0 pb-0">
        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>User Profile</th>
                        <th>Email</th>
                        <th class="text-center">Status</th>
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
                                <div class="flex-shrink-0">
                                    <img src="/dashboard-4/icon/user.png" alt="User">
                                </div>
                                <div class="flex-grow-1">
                                    <h5>{{ user.name }}</h5>
                                    <span>{{ user.role }}</span>
                                </div>
                            </div>
                        </td>
                        <td>{{ user.email }}</td>
                        <td>
                            <p class="members-box text-center" :class="user.status === 'Active' ? 'bg-light-success' : 'bg-light-danger'">
                                {{ user.status }}
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
import { ref, defineAsyncComponent, onMounted, computed } from 'vue'
import { useUserManagement } from '@/composables/useUserManagement'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const { allData, loading, fetchUsers } = useUserManagement()

const recentUsers = computed(() => {
    return (allData.value || [])
        .sort((a, b) => b.id - a.id)
        .slice(0, 5)
})

onMounted(async () => {
    await fetchUsers()
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