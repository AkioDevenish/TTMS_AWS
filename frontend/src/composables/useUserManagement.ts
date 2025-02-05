import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuth } from './useAuth'

interface User {
  id: number;
  username: string;
  email: string;
  organization: string;
  role: string;
  package: string;
  status: 'Active' | 'Inactive' | 'Pending' | 'Paused' | 'Suspended';
  isPaused: boolean;
  expires_at: string | null;
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
      const response = await axios.get('/users/')
      console.log(response.data)

      if (Array.isArray(response.data)) {
        allData.value = response.data.map((user: any) => ({
          id: user.id,
          username: user.username,
          email: user.email,
          organization: user.organization || 'N/A',
          role: user.role || 'User',
          package: user.package || 'N/A',
          status: user.status || 'Pending',
          isPaused: user.isPaused || false,
          expires_at: user.expires_at || null
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
  const updateUserStatus = async (userId: number, newStatus: 'Active' | 'Inactive' | 'Pending' | 'Paused' | 'Suspended') => {
    try {
      const response = await axios.patch(`/users/${userId}/`, {
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

  // Toggle user suspend state
  const toggleSuspendUser = async (userId: number): Promise<boolean> => {
    try {
      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      const user = allData.value.find(u => u.id === userId)
      const newStatus = user?.status === 'Suspended' ? 'Active' : 'Suspended'

      const response = await axios.patch(`/users/${userId}/`, {
        status: newStatus
      }, {
        headers: getHeaders()
      })

      if (response.status === 200) {
        const userIndex = allData.value.findIndex(user => user.id === userId)
        if (userIndex !== -1) {
          allData.value[userIndex].status = newStatus
        }
        return true
      }
      return false
    } catch (error: any) {
      console.error('Error toggling user suspend:', error)
      errorMessage.value = error.response?.data?.message || 'Failed to toggle user suspend status'
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete user
  const deleteUser = async (userId: number): Promise<boolean> => {
    try {
      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      const response = await axios.delete(`/users/${userId}/`, {
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

  // Update the status cycle function
  const cycleStatus = async (user: any) => {
    const statusMap = {
      'Active': 'Inactive',
      'Inactive': 'Active',
      'Suspended': 'Active'
    } as const

    // ... rest of the function remains the same
  }

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
    toggleSuspendUser,
    deleteUser,
    successMessage,
    errorMessage,
    getHeaders
  }
} 