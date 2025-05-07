import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const users = ref<any[]>([])
  const loading = ref(false)
  const error = ref<any>(null)
  const initialized = ref(false)
  let initPromise: Promise<void> | null = null

  // Fetch all users and their bills
  const fetchUsers = async (): Promise<void> => {
    if (initialized.value) return
    if (initPromise) return initPromise
    loading.value = true
    error.value = null
    initPromise = (async () => {
      try {
        const userRes = await axios.get('/users/')
        if (Array.isArray(userRes.data)) {
          // Fetch bills for each user in parallel
          const billsRes = await Promise.all(
            userRes.data.map((user: any) =>
              axios.get('/bills/', { params: { user_id: user.id } })
            )
          )
          users.value = userRes.data.map((user: any, idx: number) => ({
            ...user,
            bills: billsRes[idx].data || []
          })) as any[]
        } else {
          users.value = []
        }
        initialized.value = true
      } catch (err: any) {
        error.value = err as any
        users.value = []
      } finally {
        loading.value = false
        initPromise = null
      }
    })()
    return initPromise
  }

  // Fetch a single user and their bills
  const fetchUser = async (userId: number | string): Promise<any | null> => {
    loading.value = true
    error.value = null
    try {
      const userRes = await axios.get(`/users/${userId}/`)
      const billsRes = await axios.get('/bills/', { params: { user_id: userId } })
      return {
        ...userRes.data,
        bills: billsRes.data || []
      }
    } catch (err: any) {
      error.value = err as any
      return null
    } finally {
      loading.value = false
    }
  }

  // Fetch bills for a specific user
  const fetchBillsForUser = async (userId: number | string): Promise<any[]> => {
    loading.value = true
    error.value = null
    try {
      const billsRes = await axios.get('/bills/', { params: { user_id: userId } })
      return billsRes.data || []
    } catch (err: any) {
      error.value = err as any
      return []
    } finally {
      loading.value = false
    }
  }

  // Update user status
  const updateUserStatus = async (userId: number, newStatus: string): Promise<boolean> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch(`/users/${userId}/`, { status: newStatus })
      if (response.status === 200) {
        const userIndex = users.value.findIndex(user => user.id === userId)
        if (userIndex !== -1) {
          users.value[userIndex].status = newStatus
        }
        return true
      }
      return false
    } catch (err: any) {
      error.value = err
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete user
  const deleteUser = async (userId: number): Promise<boolean> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.delete(`/users/${userId}/`)
      if (response.status === 200 || response.status === 204) {
        users.value = users.value.filter(user => user.id !== userId)
        return true
      }
      return false
    } catch (err: any) {
      error.value = err
      return false
    } finally {
      loading.value = false
    }
  }

  // Toggle suspend/activate user
  const toggleSuspendUser = async (userId: number): Promise<boolean> => {
    loading.value = true
    error.value = null
    try {
      const user = users.value.find(u => u.id === userId)
      if (!user) return false
      const newStatus = user.status === 'Suspended' ? 'Active' : 'Suspended'
      const response = await axios.patch(`/users/${userId}/`, { status: newStatus })
      if (response.status === 200) {
        user.status = newStatus
        return true
      }
      return false
    } catch (err: any) {
      error.value = err
      return false
    } finally {
      loading.value = false
    }
  }

  // Reset store (for logout or reload)
  const reset = () => {
    users.value = []
    initialized.value = false
    initPromise = null
    error.value = null
  }

  return {
    users,
    loading,
    error,
    fetchUsers,
    fetchUser,
    fetchBillsForUser,
    updateUserStatus,
    deleteUser,
    toggleSuspendUser,
    reset
  }
}) 