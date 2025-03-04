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
                <tr v-for="user in allData" :key="user.id" class="user-row">
                    <td class="clickable" @click="navigateToProfile(user.id)" colspan="6">
                        <div class="d-flex">
                            <div class="user-info">
                                <div>{{ user.username || '-' }}</div>
                                <div>{{ user.organization || '-' }}</div>
                                <div>{{ user.email || 'N/A' }}</div>
                                <div>{{ user.role || 'User' }}</div>
                                <div>{{ user.package || '-' }}</div>
                                <div>
                                    <span :class="{'text-expired': isExpiringSoon(user.expires_at)}">
                                        {{ formatDate(user.expires_at) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </td>
                    <td class="status-cell px-4 py-3">
                        <button 
                            :class="[
                                'status-btn',
                                `status-${(user.status || 'Active').toLowerCase()}`
                            ]"
                            @click.stop="cycleStatus(user)"
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
                                @click.stop="handleSuspendUser(user.id)"
                                :title="user.status === 'Suspended' ? 'Reactivate user account' : 'Suspend user account'"
                            >
                                <i class="fa" :class="user.status === 'Suspended' ? 'fa-play' : 'fa-ban'"></i>
                            </button>
                            <button 
                                class="action-btn delete-btn"
                                @click.stop="handleDeleteUser(user.id)"
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
    const hasVerifiedBills = user.bills?.some((bill: any) => bill.receipt_verified) || false
    
    if (!hasVerifiedBills && !user.is_staff && !user.is_superuser) {
        errorMessage.value = 'Cannot change status until receipt is verified'
        return
    }
    
    try {
        const statusMap = {
            'Active': 'Inactive',
            'Inactive': 'Active',
            'Suspended': 'Active',
            'Pending': hasVerifiedBills ? 'Active' : 'Pending'
        } as const
        
        const newStatus = statusMap[user.status as keyof typeof statusMap] || 'Active'
        const success = await updateUserStatus(user.id, newStatus)
        
        if (success) {
            Swal.fire({
                title: 'Status Updated',
                text: `User status changed to ${newStatus}`,
                icon: 'success',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
        }
    } catch (error) {
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
            const success = await toggleSuspendUser(userId)
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
    const expiryDate = new Date(dateString)
    const now = new Date()
    return expiryDate < now
}

const navigateToProfile = (userId: number) => {
    router.push({
        path: `/users/profile`,
        query: { id: userId.toString() }
    })
}
</script>

<style scoped>
.user-row {
    cursor: default;
}

.clickable {
    cursor: pointer;
}

.user-info {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    width: 100%;
    gap: 1rem;
    align-items: center;
}

.suspend-btn {
    background-color: #dc3545;
    color: white;
}

.suspend-btn.suspended {
    background-color: #28a745;
}

.text-expired {
    color: #dc3545;
}
</style>