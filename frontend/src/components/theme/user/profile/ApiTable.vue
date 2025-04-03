<template>
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">API Keys</h4>
                <div class="card-options">
                    <a class="card-options-collapse" href="#" data-bs-toggle="card-collapse">
                        <i class="fe fe-chevron-up"></i>
                    </a>
                    <a class="card-options-remove" href="#" data-bs-toggle="card-remove">
                        <i class="fe fe-x"></i>
                    </a>
                </div>
            </div>
            <div v-if="isLoading" class="text-center p-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <div v-else-if="apiKeys.length === 0" class="p-4 text-center">
                <p>No API keys available for this user. API keys are automatically generated when the account is activated.</p>
            </div>
            <div v-else class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>API Key</th>
                            <th>Name</th>
                            <th>Created At</th>
                            <th>Last Used</th>
                            <th>Expires At</th>
                            <th>User Agent</th>
                            <th>Status</th>
                         
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="key in apiKeys" :key="key.id">
                            <td>
                                <div class="api-key-container">
                                    <span>{{ maskApiKey(key.uuid) }}</span>
                                    <button 
                                        class="btn btn-sm btn-outline-secondary ms-2" 
                                        @click="copyApiKey(key.uuid)">
                                        <i class="fa fa-copy"></i>
                                    </button>
                                </div>
                            </td>
                            <td>{{ key.token_name }}</td>
                            <td>{{ formatDate(key.created_at) }}</td>
                            <td>{{ key.last_used ? formatDate(key.last_used) : 'Never' }}</td>
                            <td>{{ formatDate(key.expires_at) }}</td>
                            <td>{{ key.last_user_agent || 'Unknown' }}</td>
                            <td>
                                <button 
                                    class="status-btn status-active"
                                    v-if="!isExpired(key.expires_at)"
                                >
                                    <span class="status-dot"></span>
                                    Active
                                </button>
                                <button 
                                    class="status-btn status-inactive"
                                    v-else
                                >
                                    <span class="status-dot"></span>
                                    Inactive
                                </button>
                            </td>
                         
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { useAuth } from '@/composables/useAuth'

// Define the type explicitly to avoid the TypeScript error
const apiKeys = ref<any[]>([])
const isLoading = ref(true)
const route = useRoute()
const { currentUser } = useAuth()

// Fetch API keys on component mount
onMounted(async () => {
    await fetchApiKeys()
})

const fetchApiKeys = async () => {
    try {
        isLoading.value = true
        
        // Get profile ID from route
        const profileId = route.query.id
        console.log('Profile ID from route:', profileId)
        
        if (!profileId) {
            console.warn('No profile ID found in URL')
            apiKeys.value = []
            isLoading.value = false
            return
        }
        
        // Get auth token
        const token = localStorage.getItem('access_token')
        
        // Make the API request with explicit user_id parameter
        const response = await axios.get(`/api-keys/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            params: { user_id: profileId }
        })
        
        console.log('API Keys response:', response.data)
        
        // Get the specific user's email for filtering
        const userResponse = await axios.get('/users/', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        
        const userId = parseInt(profileId.toString())
        const user = Array.isArray(userResponse.data) ? 
            userResponse.data.find(u => u.id === userId) : null
        
        console.log('User data for filtering:', user)
        
        // Get API usage logs to fetch user agent information
        const logsResponse = await axios.get('/api-key-usage-logs/', {
            headers: { 'Authorization': `Bearer ${token}` },
            params: { user: userId }
        })
        
        // Create a map of the latest user agent for each API key
        const userAgentMap = {}
        if (Array.isArray(logsResponse.data?.results)) {
            logsResponse.data.results.forEach(log => {
                const keyId = log.api_key
                // Only update if this is a newer log entry than what we have already
                if (!userAgentMap[keyId] || new Date(log.created_at) > new Date(userAgentMap[keyId].created_at)) {
                    userAgentMap[keyId] = {
                        user_agent: log.user_agent || 'Unknown',
                        created_at: log.created_at
                    }
                }
            })
        }
        
        // Filter keys to only show those matching the user's email
        let filteredKeys = []
        if (Array.isArray(response.data) && user?.email) {
            filteredKeys = response.data.filter(key => 
                key.email === user.email || 
                key.user_email === user.email || 
                (key.token_name && key.token_name.includes(user.email))
            )
        } else {
            filteredKeys = response.data || []
        }
        
        // Add user agent information to each key
        apiKeys.value = filteredKeys.map(key => ({
            ...key,
            last_user_agent: userAgentMap[key.id]?.user_agent || 'No usage data'
        }))
        
        console.log('Filtered API keys with user agent info:', apiKeys.value)
    } catch (error) {
        console.error('Error fetching API keys:', error)
        if (axios.isAxiosError(error)) {
            console.error('Response status:', error.response?.status)
            console.error('Response data:', error.response?.data)
        }
        apiKeys.value = []
        toast.error('Failed to load API keys', {
            hideProgressBar: true,
            autoClose: 2000,
            theme: 'colored'
        })
    } finally {
        isLoading.value = false
    }
}

// Format date for display
const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

// Check if an API key is expired
const isExpired = (expiryDate) => {
    if (!expiryDate) return true
    return new Date(expiryDate) < new Date()
}

// Mask API key for display (show only last 12 characters)
const maskApiKey = (apiKey) => {
    if (!apiKey) return 'N/A'
    const str = apiKey.toString()
    return '••••••••-••••-••••-••••-' + str.substring(str.length - 12)
}

// Copy API key to clipboard
const copyApiKey = (apiKey) => {
    navigator.clipboard.writeText(apiKey)
        .then(() => {
            toast.success('API key copied to clipboard', {
                hideProgressBar: true,
                autoClose: 2000,
                theme: 'colored'
            })
        })
        .catch((error) => {
            console.error('Failed to copy API key:', error)
            toast.error('Failed to copy API key', {
                hideProgressBar: true,
                autoClose: 2000,
                theme: 'colored'
            })
        })
}
</script>

<style scoped>
.api-key-container {
    display: flex;
    align-items: center;
}

.status-btn {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    cursor: default;
    min-width: 140px;
    justify-content: flex-start;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.status-active {
    background-color: rgba(40, 167, 69, 0.1);
    color: #28a745;
}

.status-active .status-dot {
    background-color: #28a745;
}

.status-inactive {
    background-color: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.status-inactive .status-dot {
    background-color: #dc3545;
}
</style>