<template>
	<div v-if="isAdminUser">
		<div class="form theme-form h-100">
			<div class="row">
				<div class="col-sm-6">
					<div class="mb-3">
						<label>First Name</label>
						<input class="form-control" type="text" :class="inputClasses.first_name" placeholder="First Name" v-model="formData.first_name" @input="validateField('first_name')">
					</div>
				</div>
				<div class="col-sm-6">
					<div class="mb-3">
						<label>Last Name</label>
						<input class="form-control" type="text" :class="inputClasses.last_name" placeholder="Last Name" v-model="formData.last_name" @input="validateField('last_name')">
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<div class="mb-3">
						<label>Organization</label>
						<input class="form-control" type="text" :class="inputClasses.organization" placeholder="Organization" v-model="formData.organization" @input="validateField('organization')">
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<div class="mb-3">
						<label>Email</label>
						<input class="form-control" type="email" :class="inputClasses.email" placeholder="Email" v-model="formData.email" @input="validateField('email')">
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<div class="mb-3">
						<label>Password</label>
						<input class="form-control" type="password" :class="inputClasses.password" placeholder="Password" v-model="formData.password" @input="validateField('password')">
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col">
					<div class="mb-3">
						<label>Role</label>
						<select class="form-control" :class="inputClasses.role" v-model="formData.role" @change="validateField('role')">
							<option value="">Select Role</option>
							<option value="admin">Admin</option>
							<option value="user">User</option>
						</select>
					</div>
				</div>
			</div>

			<div class="row">
				<div class="col-sm-12">
					<div class="mb-3">
						<label>Package</label>
						<select class="form-select" v-model="formData.package" :class="inputClasses.package" @change="onPackageSelected(($event.target as HTMLSelectElement).value)">
							<option value="">Select Package</option>
							<option value="Weekly">Weekly</option>
							<option value="Monthly">Monthly</option>
							<option value="Yearly">Yearly</option>
						</select>
						<div class="invalid-feedback" v-if="!formData.package">
							Please select a package
						</div>
					</div>
				</div>
				<div class="col-sm-12">
					<div class="mb-3">
						<label>Expires At</label>
						<input type="text" class="form-control" :value="formData.expires_at" disabled />
					</div>
				</div>
			</div>

			<div class="row mt-3">
				<div class="col">
					<div v-if="errorMessage" class="alert alert-danger">
						{{ errorMessage }}
					</div>
					<div v-if="successMessage" class="alert alert-success">
						{{ successMessage }}
					</div>
					<div class="text-end">
						<button class="btn btn-success me-3" @click="createUser" :disabled="isSubmitting">
							{{ isSubmitting ? 'Creating...' : 'Create' }}
						</button>
						<button class="btn btn-danger" @click="cancel" :disabled="isSubmitting">
							Cancel
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div v-else>
		<h3>Access Denied</h3>
		<p>You don't have permission to access this page.</p>
	</div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

const router = useRouter()
const { currentUser, checkAuth } = useAuth()

const isAdminUser = computed(() => {
	return currentUser.value?.is_superuser === true
})

onMounted(async () => {
	await checkAuth()
	if (!isAdminUser.value) {
		router.push('/dashboard/default')
	}
})

// Form data
const formData = reactive({
	first_name: '',
	last_name: '',
	email: '',
	password: '',
	organization: '',
	role: '',
	package: '',
	expires_at: ''
})

// Form state
const inputClasses = reactive({
	first_name: '',
	last_name: '',
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
	if (formData[field as keyof typeof formData]) {
		inputClasses[field as keyof typeof inputClasses] = 'is-valid'
	} else {
		inputClasses[field as keyof typeof inputClasses] = 'is-invalid'
	}
}

const validateForm = (): boolean => {
	let isValid = true

	// Validate all fields
	validateField('first_name')
	validateField('last_name')
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

const calculateExpiryDate = (packageType: string): string => {
	const today = new Date()
	let expiryDate = new Date(today)

	switch (packageType.toLowerCase()) {
		case 'weekly':
			expiryDate.setDate(today.getDate() + 7)
			break
		case 'monthly':
			expiryDate.setMonth(today.getMonth() + 1)
			break
		case 'yearly':
			expiryDate.setFullYear(today.getFullYear() + 1)
			break
		default:
			return ''
	}

	// Format date as YYYY-MM-DD
	return expiryDate.toISOString().split('T')[0]
}

// Update formData when package changes
watch(() => formData.package, (newPackage) => {
	if (newPackage) {
		formData.expires_at = calculateExpiryDate(newPackage)
	}
})

const onPackageSelected = (packageType: string) => {
	if (!packageType) return

	const expiryDate = calculateExpiryDate(packageType)
	formData.package = packageType
	formData.expires_at = expiryDate

	console.log('Package selected:', packageType)
	console.log('Expiry date set to:', expiryDate)

	inputClasses.package = 'is-valid'
}

// API interaction
const createUser = async () => {
	try {
		if (!validateForm()) return

		isSubmitting.value = true
		errorMessage.value = ''
		successMessage.value = ''

		const token = localStorage.getItem('access_token')

		const userData = {
			first_name: formData.first_name,
			last_name: formData.last_name,
			email: formData.email,
			password: formData.password,
			organization: formData.organization,
			role: formData.role,
			package: formData.package,
			status: 'Active',
			expires_at: formData.expires_at || calculateExpiryDate(formData.package)
		}

		console.log('Sending user data:', userData)

		const response = await axios.post('/users/', userData, {
			headers: {
				'Authorization': `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		})

		successMessage.value = 'User created successfully!'

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