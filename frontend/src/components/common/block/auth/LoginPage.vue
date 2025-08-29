<template>
	<div class="container-fluid p-0">
		<div class="row m-0">
			<div class="col-12 p-0">
				<div class="login-card login-dark">
					<div class="login-container">
						<div class="login-left">
							<div class="program-title">
								<h2>Meteorological Data Processing System</h2>
								<p class="subtitle">Trinidad and Tobago Meteorological Service</p>
							</div>
							<form class="theme-form" @submit.prevent="doLogin">
								<h4>Sign in to account</h4>
								<p>Enter your email & password to login</p>
								<div class="form-group">
									<label class="col-form-label">Email Address</label>
									<input v-model="email" class="form-control" type="email" placeholder="Test@gmail.com" :disabled="loading"></input>
								</div>
								<div class="form-group">
									<label class="col-form-label">Password</label>
									<div class="form-input position-relative">
										<input v-model="password" :type="type" class="form-control" name="login[password]" placeholder="*********" :disabled="loading"></input>
										<div class="show-hide"><span class="show" @click="showPassword"> </span></div>
									</div>
								</div>
								<div class="form-group mb-0">
									<div class="text-center mt-4">
										<button class="btn btn-primary btn-block w-100" type="submit" :disabled="loading">
											{{ loading ? 'Signing in...' : 'Sign in' }}
										</button>
									</div>
								</div>
								<div class="contact-info mt-4">
									<p class="text-center mb-2">Forgot your password?</p>
									<p class="text-center contact-number">
										<span>Contact Support:</span>
										<a href="tel:+1234567890" class="phone-link">+1 (234) 567-890</a>
									</p>
								</div>
							</form>
						</div>
						<div class="login-right">
							<div class="logo-section">
								<router-link class="logo" to="/">
									<img class="img-fluid for-light" src="@/assets/images/logo/logo.png" alt="logo">
									<img class="img-fluid for-dark" src="@/assets/images/logo/logo_dark.png" alt="logo">
								</router-link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const router = useRouter()
const authStore = useAuthStore()

const type = ref<string>('password')
const email = ref<string>("")
const password = ref<string>("")
const loading = ref<boolean>(false)

function showPassword() {
	type.value = type.value === 'password' ? 'text' : 'password'
}

async function doLogin() {
	try {
		loading.value = true
		if (!email.value || !password.value) {
			toast.error('Please enter email and password')
			return
		}

		const response = await authStore.login({
			email: email.value,
			password: password.value,
			remember_me: false
		})

		if (response.success) {
			console.log('Login successful:', response.user)
			router.push('/dashboard')
		} else if (response.error) {
			toast.error(response.error)
			return
		}
	} catch (error: any) {
		console.error('Login error:', error)
		const errorMessage = error.response?.data?.error || 
							error.response?.data?.detail || 
							'Invalid credentials'
		toast.error(errorMessage)
	} finally {
		loading.value = false
	}
}
</script>