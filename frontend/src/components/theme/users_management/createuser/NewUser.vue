<template>
    <div class="form theme-form h-100">
        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Name</label>
                    <input 
                        class="form-control" 
                        type="text" 
                        :class="inputClasses.name"
                        placeholder="Name"
                        v-model="formData.name"
                        @input="validateField('name')">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Organization</label>
                    <input 
                        class="form-control"
                        type="text"
                        :class="inputClasses.organization"
                        placeholder="Organization"
                        v-model="formData.organization"
                        @input="validateField('organization')">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Email</label>
                    <input 
                        class="form-control"
                        type="email"
                        :class="inputClasses.email"
                        placeholder="Email"
                        v-model="formData.email"
                        @input="validateField('email')">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Password</label>
                    <input 
                        class="form-control"
                        type="password"
                        :class="inputClasses.password"
                        placeholder="Password"
                        v-model="formData.password"
                        @input="validateField('password')">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Role</label>
                    <select 
                        class="form-control"
                        :class="inputClasses.role"
                        v-model="formData.role"
                        @change="validateField('role')">
                        <option value="">Select Role</option>
                        <option value="admin">Admin</option>
                        <option value="user">User</option>
                    </select>
                </div>
            </div>
        </div>

        <SubscriptionType @package-selected="onPackageSelected" />

        <div class="row mt-3">
            <div class="col">
                <div v-if="errorMessage" class="alert alert-danger">
                    {{ errorMessage }}
                </div>
                <div v-if="successMessage" class="alert alert-success">
                    {{ successMessage }}
                </div>
                <div class="text-end">
                    <button 
                        class="btn btn-success me-3" 
                        @click="createUser"
                        :disabled="isSubmitting">
                        {{ isSubmitting ? 'Creating...' : 'Create' }}
                    </button>
                    <button 
                        class="btn btn-danger" 
                        @click="cancel"
                        :disabled="isSubmitting">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { defineAsyncComponent } from 'vue'

const SubscriptionType = defineAsyncComponent(() => import("./SubscriptionType.vue"))
const router = useRouter()

// Form data
const formData = reactive({
    name: '',
    email: '',
    password: '',
    organization: '',
    role: '',
    package: ''
})

// Form state
const inputClasses = reactive({
    name: '',
    email: '',
    password: '',
    organization: '',
    role: '',
    package: ''
})

const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Validation
const validateField = (field: string) => {
    switch (field) {
        case 'name':
            inputClasses.name = formData.name.length >= 3 ? 'is-valid' : 'is-invalid'
            break
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            inputClasses.email = emailRegex.test(formData.email) ? 'is-valid' : 'is-invalid'
            break
        case 'password':
            inputClasses.password = formData.password.length >= 6 ? 'is-valid' : 'is-invalid'
            break
        case 'organization':
            inputClasses.organization = formData.organization.length >= 2 ? 'is-valid' : 'is-invalid'
            break
        case 'role':
            inputClasses.role = formData.role ? 'is-valid' : 'is-invalid'
            break
    }
}

const validateForm = (): boolean => {
    let isValid = true
    
    // Validate all fields
    validateField('name')
    validateField('email')
    validateField('password')
    validateField('organization')
    validateField('role')
    
    // Check if any field is invalid
    Object.values(inputClasses).forEach(className => {
        if (className === 'is-invalid') isValid = false
    })
    
    // Check if package is selected
    if (!formData.package) {
        isValid = false
        errorMessage.value = 'Please select a package'
    }
    
    return isValid
}

const onPackageSelected = (packageType: string) => {
    formData.package = packageType
    inputClasses.package = packageType ? 'is-valid' : 'is-invalid'
}

// API interaction
const createUser = async () => {
    try {
        if (!validateForm()) {
            return
        }

        isSubmitting.value = true
        errorMessage.value = ''
        successMessage.value = ''

        // Configure axios
        axios.defaults.baseURL = 'http://127.0.0.1:8000'

        // Send POST request to Django API
        const response = await axios.post('/users/', formData)
        
        successMessage.value = 'User created successfully!'
        
        // Wait for 1 second to show success message
        setTimeout(() => {
            router.push('/users_management')
        }, 1000)

    } catch (error: any) {
        console.error('Error creating user:', error)
        errorMessage.value = error.response?.data?.message || 'Error creating user. Please try again.'
    } finally {
        isSubmitting.value = false
    }
}

const cancel = () => {
    router.push('/users_management')
}
</script>

<style scoped>
.alert {
    margin-bottom: 1rem;
}
</style>