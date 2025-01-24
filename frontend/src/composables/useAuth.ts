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
  name: string
  email: string
  role: string
  is_superuser: boolean
  is_staff: boolean
}

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const error = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)

  // Computed properties for role checks
  const isAdmin = computed(() => currentUser.value?.is_superuser || false)
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
      const response = await axios.post('http://127.0.0.1:8000/api/token/', credentials)
      
      if (response.data.access) {
        setAuthToken(response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        
        await refreshUserData()
        return { success: true, user: currentUser.value }
      }
      return { success: false }
    } catch (error: any) {
      console.error('Login error:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const refreshUserData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/user/me/')
      
      // Create a reactive user object with proper role handling
      currentUser.value = {
        id: response.data.id,
        name: response.data.name,
        email: response.data.email,
        role: response.data.is_superuser ? 'Admin' : response.data.is_staff ? 'Staff' : 'User',
        is_superuser: response.data.is_superuser,
        is_staff: response.data.is_staff
      }
      isAuthenticated.value = true
    } catch (error) {
      console.error('Error fetching user data:', error)
      clearAuth()
      throw error
    }
  }

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token')
    console.log('Checking auth, token:', token ? 'exists' : 'not found')
    
    if (!token) {
      clearAuth()
      return false
    }

    try {
      setAuthToken(token)
      await refreshUserData()
      return true
    } catch (err) {
      console.error('Auth check failed:', err)
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
    requireAuth
  }
}