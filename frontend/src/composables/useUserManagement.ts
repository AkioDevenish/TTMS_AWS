import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuth } from './useAuth'

interface User {
    id: number;
    name: string;
    email: string;
    organization: string;
    role: string;
    package: string;
    status: 'Active' | 'Inactive' | 'Pending' | 'Paused';
    isPaused: boolean;
}

export function useUserManagement() {
    const router = useRouter()
    const { logout, checkAuth } = useAuth()
    const allData = ref<User[]>([])
    const loading = ref<boolean>(true)
    const filterQuery = ref<string>("")
    const currentPage = ref<number>(1)
    const elementsPerPage = ref<number>(10)
    const successMessage = ref<string>("")
    const errorMessage = ref<string>("")

    const getHeaders = () => {
        const token = localStorage.getItem('access_token')
        
        if (!token) {
            throw new Error('No token found')
        }
        
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }

    // Fetch users from API
    const fetchUsers = async () => {
        try {
            loading.value = true
            const headers = getHeaders()
            const response = await axios.get('http://127.0.0.1:8000/users/', { headers })
            
            if (Array.isArray(response.data)) {
                allData.value = response.data.map((user: any) => ({
                    id: user.id,
                    name: user.name,
                    email: user.email,
                    organization: user.organization,
                    role: user.role || 'user',
                    package: user.package,
                    status: user.status || 'Pending',
                    isPaused: user.isPaused || false
                }))
            }
        } catch (error: any) {
            console.error('Error fetching users:', error.response?.data || error.message)
            errorMessage.value = 'Failed to fetch users'
            allData.value = []
        } finally {
            loading.value = false
        }
    }

    // Update user status
    const updateUserStatus = async (userId: number, newStatus: 'Active' | 'Inactive' | 'Pending' | 'Paused') => {
        try {
            const response = await axios.patch(`http://127.0.0.1:8000/users/${userId}/`, {
                status: newStatus
            }, {
                headers: getHeaders()
            })

            if (response.status === 200) {
                const userIndex = allData.value.findIndex(user => user.id === userId)
                if (userIndex !== -1) {
                    allData.value[userIndex].status = newStatus
                }
                successMessage.value = 'Status updated successfully'
            }
        } catch (error) {
            console.error('Error updating user status:', error)
            errorMessage.value = 'Failed to update user status'
        }
    }

    // Toggle user pause state
    const togglePauseUser = async (userId: number) => {
        try {
            const response = await axios.post(`http://127.0.0.1:8000/users/${userId}/toggle-pause/`, {}, {
                headers: getHeaders()
            })

            if (response.status === 200) {
                const userIndex = allData.value.findIndex(user => user.id === userId)
                if (userIndex !== -1) {
                    allData.value[userIndex].isPaused = !allData.value[userIndex].isPaused
                    allData.value[userIndex].status = allData.value[userIndex].isPaused ? 'Paused' : 'Active'
                }
                const action = allData.value[userIndex].isPaused ? 'paused' : 'resumed'
                successMessage.value = `User has been ${action} successfully`
            }
        } catch (error) {
            console.error('Error toggling user pause:', error)
            errorMessage.value = 'Failed to toggle user pause status'
        }
    }

    // Delete user
    const deleteUser = async (userId: number): Promise<boolean> => {
        try {
            loading.value = true
            errorMessage.value = ''
            successMessage.value = ''

            const response = await axios.delete(`http://127.0.0.1:8000/users/${userId}/`, {
                headers: getHeaders()
            })

            if (response.status === 200) {
                allData.value = allData.value.filter(user => user.id !== userId)
                successMessage.value = response.data.message || 'User deleted successfully'
                return true
            }
            return false
        } catch (error: any) {
            console.error('Delete error:', error.response || error)
            if (error.response?.status === 401) {
                errorMessage.value = 'Authentication failed. Please check your session.'
                logout()
            } else if (error.response?.status === 403) {
                errorMessage.value = 'You do not have permission to delete users'
            } else {
                errorMessage.value = error.response?.data?.message || 'Failed to delete user'
            }
            return false
        } finally {
            loading.value = false
        }
    }

    // Pagination methods remain the same
    const paginatedData = computed(() => {
        const start = (currentPage.value - 1) * elementsPerPage.value
        const end = start + elementsPerPage.value
        return allData.value.slice(start, end)
    })

    const totalPages = computed(() => {
        return Math.ceil(allData.value.length / elementsPerPage.value)
    })

    return {
        allData,
        loading,
        filterQuery,
        currentPage,
        elementsPerPage,
        paginatedData,
        totalPages,
        fetchUsers,
        updateUserStatus,
        togglePauseUser,
        deleteUser,
        successMessage,
        errorMessage,
        getHeaders
    }
} 