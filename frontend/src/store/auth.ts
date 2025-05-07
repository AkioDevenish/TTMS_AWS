import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

interface LoginCredentials {
  email: string
  password: string
  remember_me: boolean
}

interface User {
  id: number
  username: string
  email: string
  role: string
  is_superuser: boolean
  is_staff: boolean
  first_name: string | null
  last_name: string | null
  status: string
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const loading = ref(false)
  const error = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)

  // Computed properties for role checks
  const isAdmin = computed(() => {
    return !!currentUser.value?.is_superuser || 
           (currentUser.value?.role === 'admin');
  })
  const isStaff = computed(() => currentUser.value?.is_staff || false)

  const setAuthToken = (token: string) => {
    localStorage.setItem('access_token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  const clearAuth = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete axios.defaults.headers.common['Authorization']
    currentUser.value = null
    isAuthenticated.value = false
  }

  const login = async (credentials: LoginCredentials) => {
    try {
      loading.value = true
      const response = await axios.post('/token/', credentials)

      if (response.data.access) {
        setAuthToken(response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        await refreshUserData()
        if (currentUser.value && (currentUser.value as User).status === 'Suspended') {
          clearAuth()
          error.value = 'Your account has been suspended. Please contact support.'
          return { success: false, error: error.value }
        }
        return { success: true, user: currentUser.value }
      }
      return { success: false }
    } catch (error: any) {
      error.value = error.response?.data?.error || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const refreshUserData = async () => {
    try {
      const response = await axios.get('/user/me/')
      currentUser.value = {
        id: response.data.id,
        username: `${response.data.first_name} ${response.data.last_name}`.trim(),
        email: response.data.email,
        role: response.data.is_superuser ? 'Admin' : response.data.is_staff ? 'Staff' : 'User',
        is_superuser: response.data.is_superuser,
        is_staff: response.data.is_staff,
        first_name: response.data.first_name,
        last_name: response.data.last_name,
        status: response.data.status
      }
      if ((currentUser.value as User).status === 'Suspended') {
        clearAuth()
        error.value = 'Your account has been suspended. Please contact support.'
        return false
      }
      isAuthenticated.value = true
    } catch (error) {
      clearAuth()
      throw error
    }
  }

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      clearAuth()
      return false
    }
    if (currentUser.value) {
      isAuthenticated.value = true
      if ((currentUser.value as User).status === 'Suspended') {
        clearAuth()
        error.value = 'Your account has been suspended. Please contact support.'
        return false
      }
      return true
    }
    try {
      setAuthToken(token)
      await refreshUserData()
      if (currentUser.value && (currentUser.value as User).status === 'Suspended') {
        clearAuth()
        error.value = 'Your account has been suspended. Please contact support.'
        return false
      }
      return true
    } catch (err) {
      clearAuth()
      return false
    }
  }

  const requireAuth = async (requiredRole?: 'admin' | 'staff') => {
    const isAuthed = await checkAuth()
    if (!isAuthed) {
      router.push('/auth/login')
      return false
    }
    if (requiredRole === 'admin' && !isAdmin.value) {
      router.push('/unauthorized')
      return false
    }
    if (requiredRole === 'staff' && !isStaff.value && !isAdmin.value) {
      router.push('/unauthorized')
      return false
    }
    return true
  }

  const logout = async () => {
    clearAuth()
    router.push('/auth/login')
  }

  const hasRequiredRole = (requiredRole?: 'admin' | 'staff') => {
    if (!requiredRole) return true
    if (requiredRole === 'admin') return isAdmin.value
    if (requiredRole === 'staff') return isStaff.value || isAdmin.value
    return true
  }

  return {
    login,
    logout,
    checkAuth,
    loading,
    error,
    isAuthenticated,
    currentUser,
    isAdmin,
    isStaff,
    requireAuth,
    hasRequiredRole
  }
}) 