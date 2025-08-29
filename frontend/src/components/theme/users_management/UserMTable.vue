<template>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th class="px-4">Name</th>
                    <th class="px-4">Organization</th>
                    <th class="px-4">Email</th>
                    <th class="px-4">Role</th>
                    <th class="px-4">Package</th>
                    <th class="px-4">Expires At</th>
                    <th class="px-4">Status</th>
                    <th class="px-4">Actions</th>
                </tr>
            </thead>
            <tbody v-if="loading">
                <tr>
                    <td colspan="8" class="text-center py-4">Loading...</td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr v-for="user in users" :key="user.id" class="user-row" @click="handleUserClick(user)" :title="`Click to view ${user.name || user.email} details`">
                    <td class="px-4 py-3 clickable-cell">{{ user.name || `${user.first_name || ''} ${user.last_name || ''}`.trim() || '-' }}</td>
                    <td class="px-4 py-3 clickable-cell">{{ user.organization || '-' }}</td>
                    <td class="px-4 py-3 clickable-cell">{{ user.email || 'Email Not Available' }}</td>
                    <td class="px-4 py-3 clickable-cell">{{ user.role || 'User' }}</td>
                    <td class="px-4 py-3 clickable-cell">{{ user.package || '-' }}</td>
                    <td class="px-4 py-3 clickable-cell">
                                    <span :class="{'text-expired': isExpiringSoon(user.expires_at)}">
                                        {{ formatDate(user.expires_at) }}
                                    </span>
                    </td>
                    <td class="status-cell px-4 py-3 clickable-cell">
                        <span 
                            :class="[
                                'status-badge',
                                `status-${(user.status || 'Active').toLowerCase()}`
                            ]"
                        >
                            {{ user.status || 'Active' }}
                        </span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="action-buttons">
                            <button 
                                class="suspend-btn"
                                :class="{ 'suspended': user.status === 'Suspended' }"
                                @click.stop="handleSuspendUser(user.id)"
                                :title="user.status === 'Suspended' ? 'Reactivate user account' : 'Suspend user account'"
                            >
                                <i class="fa" :class="user.status === 'Suspended' ? 'fa-play' : 'fa-ban'"></i>
                            </button>
                            <button 
                                class="delete-btn"
                                @click.stop="handleDeleteUser(user.id)"
                            >
                                <i class="fa fa-trash"></i>
                            </button>
                            <button 
                                class="view-btn"
                                @click.stop="handleUserClick(user)"
                                title="View user profile"
                            >
                                <i class="fa fa-eye"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAuthStore } from '@/store/auth'
import Swal from 'sweetalert2'

const router = useRouter()
const userStore = useUserStore()
const users = computed(() => userStore.users)
const loading = computed(() => userStore.loading)

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)

onMounted(async () => {
    if (!currentUser.value?.is_superuser) {
        window.history.back()
        return
    }
})

const handleDeleteUser = async (userId: number) => {
    try {
        const result = await Swal.fire({
            title: 'Delete User',
            text: 'Are you sure you want to delete this user? This action cannot be undone.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, delete',
            cancelButtonText: 'Cancel',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                try {
                    const success = await userStore.deleteUser(userId)
                    if (!success) {
                        throw new Error(userStore.error || 'Failed to delete user')
                    }
                    return success
                } catch (error) {
                    Swal.showValidationMessage(
                        `Delete failed: ${userStore.error || 'Unknown error occurred'}`
                    )
                }
            },
            allowOutsideClick: () => !Swal.isLoading()
        })
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Deleted!',
                text: 'User has been deleted successfully.',
                icon: 'success',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
            await userStore.fetchUsers() // Refresh the list
        }
    } catch (error) {
        console.error('Error in handleDeleteUser:', error)
        Swal.fire({
            title: 'Error',
            text: userStore.error || 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

const handleSuspendUser = async (userId: number) => {
    const user = users.value.find(u => u.id === userId)
    const isSuspended = user?.status === 'Suspended'
    try {
        const result = await Swal.fire({
            title: `${isSuspended ? 'Reactivate' : 'Suspend'} User Account`,
            text: `${isSuspended 
                ? 'This will allow the user to log in again.' 
                : 'This will prevent the user from logging in to their account.'}`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: isSuspended ? '#28a745' : '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: `Yes, ${isSuspended ? 'reactivate' : 'suspend'} account`,
            cancelButtonText: 'Cancel'
        })
        if (result.isConfirmed) {
            const success = await userStore.toggleSuspendUser(userId)
            if (success) {
                Swal.fire({
                    title: 'Success',
                    text: `User account ${isSuspended 
                        ? 'reactivated successfully. User can now log in.' 
                        : 'suspended successfully. User cannot log in until reactivated.'}`,
                    icon: 'success',
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000
                })
            } else {
                throw new Error(userStore.error)
            }
        }
    } catch (error) {
        console.error('Error in handleSuspendUser:', error)
        Swal.fire({
            title: 'Error',
            text: userStore.error || 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

const handleUserClick = (user: any) => {
    // Navigate to user profile page first
    router.push({
        path: '/users/profile',
        query: { id: user.id }
    })
}

const formatDate = (dateString: string | null) => {
    if (!dateString) return 'No expiry date'
    // Remove any time component from the date string
    const dateOnly = dateString.split('T')[0]
    const date = new Date(dateOnly)
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

const isExpiringSoon = (dateString: string | null) => {
    if (!dateString) return false
    const expiryDate = new Date(dateString)
    const now = new Date()
    return expiryDate < now
}
</script>

<style scoped>
.user-row {
    transition: background-color 0.2s ease;
    cursor: pointer;
}

.user-row:hover {
    background-color: #f8f9fa;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.clickable-cell {
    cursor: pointer;
}

.clickable-cell:hover {
    color: #007bff;
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-align: center;
    min-width: 80px;
}

.status-active {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-inactive {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status-suspended {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.status-pending {
    background-color: #e2e3e5;
    color: #383d41;
    border: 1px solid #d6d8db;
}

.suspend-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.suspend-btn.suspended {
    background-color: #28a745;
}

.suspend-btn:hover {
    background-color: #c82333;
    transform: scale(1.1);
}

.delete-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-btn:hover {
    background-color: #c82333;
    transform: scale(1.1);
}

.view-btn {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.view-btn:hover {
    background-color: #0056b3;
    transform: scale(1.1);
}

.suspend-btn i,
.delete-btn i {
    font-size: 14px;
}

.text-expired {
    color: #dc3545;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}
</style>