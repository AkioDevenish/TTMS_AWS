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
                <tr v-for="user in allData" :key="user.id">

                    <td class="px-4 py-3">{{ user.username || '-' }}</td>
                    <td class="px-4 py-3">{{ user.organization || '-' }}</td>
                    <td class="px-4 py-3">{{ user.email || 'N/A' }}</td>
                    <td class="px-4 py-3">{{ user.role || 'User' }}</td>
                    <td class="px-4 py-3">{{ user.package || '-' }}</td>
                    <td class="px-4 py-3">
                        <span :class="{'text-danger': isExpiringSoon(user.expires_at)}">
                            {{ formatDate(user.expires_at) }}
                        </span>
                    </td>
                    <td class="status-cell px-4 py-3">
                        <button 
                            :class="[
                                'status-btn',
                                `status-${(user.status || 'Active').toLowerCase()}`
                            ]"
                            @click="cycleStatus(user)"
                        >
                            <span class="status-dot"></span>
                            {{ user.status || 'Active' }}
                        </button>
                    </td>
                    <td class="px-4 py-3">
                        <div class="action-buttons">
                            <button 
                                class="action-btn suspend-btn"
                                :class="{ 'suspended': user.status === 'Suspended' }"
                                @click="handleSuspendUser(user.id)"
                                :title="user.status === 'Suspended' ? 'Reactivate user account' : 'Suspend user account'"
                            >
                                <i class="fa" :class="user.status === 'Suspended' ? 'fa-play' : 'fa-ban'"></i>
                            </button>
                            <button 
                                class="action-btn delete-btn"
                                @click="handleDeleteUser(user.id)"
                            >
                                <i class="fa fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useUserManagement } from '@/composables/useUserManagement'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const { 
    loading, 
    filterQuery, 
    toggleSuspendUser, 
    deleteUser, 
    updateUserStatus, 
    fetchUsers, 
    allData,
    errorMessage,
    getHeaders 
} = useUserManagement()

const { currentUser, checkAuth } = useAuth()
const router = useRouter()

onMounted(async () => {
    await checkAuth()
    if (!currentUser.value?.is_superuser) {
        router.go(-1)
        return
    }
    await fetchUsers()
})

const cycleStatus = async (user: any) => {
    if (user.status === 'Pending') {
        errorMessage.value = 'Cannot change status of pending users'
        return
    }
    
    try {
        const statusMap = {
            'Active': 'Inactive',
            'Inactive': 'Active',
            'Paused': 'Active'
        } as const
        
        const newStatus = statusMap[user.status as keyof typeof statusMap] || 'Inactive'
        
        const success = await updateUserStatus(user.id, newStatus)
        
        if (success) {
            // Show success toast
            Swal.fire({
                title: 'Status Updated',
                text: `User status changed to ${newStatus}`,
                icon: 'success',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
        } else {
            // Show error toast
            Swal.fire({
                title: 'Error',
                text: errorMessage.value || 'Failed to update status',
                icon: 'error',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
        }
    } catch (error) {
        console.error('Error in cycleStatus:', error)
        Swal.fire({
            title: 'Error',
            text: 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

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
                    const success = await deleteUser(userId)
                    if (!success) {
                        throw new Error(errorMessage.value || 'Failed to delete user')
                    }
                    return success
                } catch (error) {
                    Swal.showValidationMessage(
                        `Delete failed: ${errorMessage.value || 'Unknown error occurred'}`
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
            await fetchUsers() // Refresh the list
        }
    } catch (error) {
        console.error('Error in handleDeleteUser:', error)
        Swal.fire({
            title: 'Error',
            text: errorMessage.value || 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

const handleSuspendUser = async (userId: number) => {
    const user = allData.value.find(u => u.id === userId)
    const isSuspended = user?.status === 'Suspended'
    
    try {
        const result = await Swal.fire({
            title: `${isSuspended ? 'Reactivate' : 'Suspend'} User Account`,
            text: `Are you sure you want to ${isSuspended ? 'reactivate' : 'suspend'} this user account?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: isSuspended ? '#28a745' : '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: `Yes, ${isSuspended ? 'reactivate' : 'suspend'} account`,
            cancelButtonText: 'Cancel'
        })

        if (result.isConfirmed) {
            const success = await toggleSuspendUser(userId)
            if (success) {
                Swal.fire({
                    title: 'Success',
                    text: `User account ${isSuspended ? 'reactivated' : 'suspended'} successfully`,
                    icon: 'success',
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000
                })
            } else {
                throw new Error(errorMessage.value)
            }
        }
    } catch (error) {
        console.error('Error in handleSuspendUser:', error)
        Swal.fire({
            title: 'Error',
            text: errorMessage.value || 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
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
    // Remove any time component from the date string
    const dateOnly = dateString.split('T')[0]
    const expiryDate = new Date(dateOnly)
    const today = new Date()
    today.setHours(0, 0, 0, 0) // Reset time component
    const daysUntilExpiry = Math.ceil((expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
    return daysUntilExpiry <= 7 && daysUntilExpiry > 0
}
</script>

<style scoped>
.suspend-btn {
    background-color: #dc3545;
    color: white;
}

.suspend-btn.suspended {
    background-color: #28a745;
}
</style>