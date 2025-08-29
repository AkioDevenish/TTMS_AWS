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
                    <tr v-for="(user, index) in recentUsers" :key="index" class="user-row">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="user-avatar me-3">
                                    <div class="avatar-initial">
                                        {{ getUserInitials(user) }}
                                    </div>
                                </div>
                                <div class="flex-grow-1">
                                    <h6 class="mb-0 user-name">{{ (user as any).username || `${(user as any).first_name} ${(user as any).last_name}`.trim() }}</h6>
                                    <span class="text-muted user-role">{{ (user as any).role || ((user as any).is_superuser ? 'Admin' : (user as any).is_staff ? 'Staff' : 'User') }}</span>
                                </div>
                            </div>
                        </td>
                        <td>
                            <span class="user-email">{{ (user as any).email }}</span>
                        </td>
                        <td class="text-center">
                            <span class="status-badge" :class="getStatusClass((user as any).status)">
                                {{ (user as any).status }}
                            </span>
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

const recentUsers = computed(() => props.users.slice(0, 8))

const getUserInitials = (user: any) => {
    if (user.username) {
        return user.username.charAt(0).toUpperCase()
    }
    if (user.first_name && user.last_name) {
        return (user.first_name.charAt(0) + user.last_name.charAt(0)).toUpperCase()
    }
    if (user.first_name) {
        return user.first_name.charAt(0).toUpperCase()
    }
    if (user.email) {
        return user.email.charAt(0).toUpperCase()
    }
    return 'U'
}

const getStatusClass = (status: string) => {
    const statusMap: { [key: string]: string } = {
        'Active': 'status-active',
        'Inactive': 'status-inactive',
        'Pending': 'status-pending',
        'Suspended': 'status-suspended',
        'default': 'status-default'
    }
    return statusMap[status] || statusMap['default']
}

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
.user-row {
    transition: background-color 0.2s ease;
}

.user-row:hover {
    background-color: #f8f9fa;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
    font-size: 16px;
}

.avatar-initial {
    line-height: 1;
}

.user-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #333;
}

.user-role {
    font-size: 0.8rem;
    color: #6c757d;
}

.user-email {
    font-size: 0.85rem;
    color: #495057;
}

.status-badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-align: center;
    min-width: 80px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    margin: 0 auto;
}

/* Ensure the status column content is centered */
td.text-center {
    text-align: center !important;
}

/* Ensure the status column header is also centered */
th.text-center {
    text-align: center !important;
}

.status-active {
    background-color: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

.status-inactive {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.status-pending {
    background-color: #fff3cd;
    color: #856404;
    border-color: #ffeaa7;
}

.status-suspended {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.status-default {
    background-color: #e2e3e5;
    color: #383d41;
    border-color: #d6d8db;
}
</style>