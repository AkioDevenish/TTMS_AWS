<template>
	<div class="container-fluid p-0">
		<div class="row m-0">
			<div class="col-12 p-0">
				<div class="overlay"></div>
				<div class="login-card login-dark">
					<div>
						<div><router-link class="logo" to="/"><img class="img-fluid for-light" src="@/assets/images/logo/logo.png" alt="looginpage"><img class="img-fluid for-dark" src="@/assets/images/logo/logo_dark.png" alt="looginpage"></router-link></div>
						<div class="login-main">
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
									<div class="checkbox p-0">
										<input id="checkbox1" type="checkbox" v-model="rememberMe">
										<label class="text-muted" for="checkbox1">Remember password</label>
									</div>
									<router-link class="link" to="/authentication/forget_password">
										Forgot password?
									</router-link>
									<div class="text-end mt-3">
										<button class="btn btn-primary btn-block w-100" type="submit" :disabled="loading">
											{{ loading ? 'Signing in...' : 'Sign in' }}
										</button>
									</div>
								</div>
								<!-- <h6 class="text-muted mt-4 or">Or Sign in with </h6>
								<div class="social mt-4">
									<div class="btn-showcase">
										<a class="btn btn-light" href="https://www.linkedin.com/login" target="_blank">
											<vue-feather class="txt-linkedin" type="linkedin"></vue-feather>
											LinkedIn
										</a>
										<a class="btn btn-light" href="https://twitter.com/login?lang=en" target="_blank">
											<vue-feather class="txt-twitter" type="twitter"></vue-feather>
											twitter
										</a>
										<a class="btn btn-light" href="https://www.facebook.com/" target="_blank">
											<vue-feather class="txt-fb" type="facebook"></vue-feather>
											facebook
										</a>
									</div>
								</div> -->
								<!-- <p class="mt-4 mb-0 text-center">Don't have account?<router-link class="ms-2" to="/auth/register">Create Account</router-link></p> -->
							</form>
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
const rememberMe = ref<boolean>(false)

function showPassword() {
	type.value = type.value === 'password' ? 'text' : 'password'
}

async function doLogin() {
	try {
		if (!email.value || !password.value) {
			toast.error('Please enter email and password')
			return
		}

		const response = await authStore.login({
			email: email.value,
			password: password.value,
			remember_me: rememberMe.value
		})

		if (response.success) {
			console.log('Login successful:', response.user)
			if (rememberMe.value) {
				localStorage.setItem('rememberedEmail', email.value)
			}
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
	}
}
</script>