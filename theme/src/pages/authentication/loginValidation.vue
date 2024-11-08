<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-xl-7 order-1 b-center bg-size"
                :style="{ backgroundImage: 'url(' + require('@/assets/images/login/1.jpg') + ')', }"><img
                    class="bg-img-cover bg-center d-none" src="@/assets/images/login/1.jpg" alt="looginpage"></div>
            <div class="col-xl-5 p-0">
                <div class="login-card login-dark">
                    <div>
                        <div><a class="logo "> <router-link to="/"><img class="img-fluid for-light"
                                        src="@/assets/images/logo/logo.png" alt="looginpage"><img class="img-fluid for-dark"
                                        src="@/assets/images/logo/logo_dark.png" alt="looginpage"></router-link></a></div>
                        <div class="login-main">
                            <form class="theme-form" novalidate @submit.prevent="validate">
                                <h4>Sign in to account</h4>
                                <p>Enter your email & password to login</p>
                                <div class="form-group">
                                    <label class="col-form-label">Email Address</label>
                                    <input class="form-control"
                                        v-bind:class="formSubmitted ? emailError ? 'is-invalid' : 'is-valid' : ''"
                                        id="email" v-model="email" type="email" required placeholder="Test@gmail.com">
                                </div>
                                <div class="form-group">
                                    <label class="col-form-label">Password</label>
                                    <div class="form-input position-relative">
                                        <input class="form-control" :type="type" name="login[password]"
                                            v-bind:class="formSubmitted ? passwordError ? 'is-invalid' : 'is-valid' : ''"
                                            required placeholder="*********" v-model="password">
                                        <div class="show-hide"><span class="show" @click="showPassword"> </span></div>
                                    </div>
                                </div>
                                <div class="form-group mb-0">
                                    <div class="checkbox p-0">
                                        <input id="checkbox1" type="checkbox">
                                        <label class="text-muted" for="checkbox1">Remember password</label>
                                    </div><a class="link"><router-link to="/authentication/forget_password"> Forgot
                                            password?</router-link></a>
                                    <div class="text-end mt-3">
                                        <button class="btn btn-primary btn-block w-100" type="submit">Sign in</button>
                                    </div>
                                </div>
                                <h6 class="text-muted mt-4 or">Or Sign in with</h6>
                                <div class="social mt-4">
                                    <div class="btn-showcase"><a class="btn btn-light" href="https://www.linkedin.com/login"
                                            target="_blank"><vue-feather class="txt-linkedin" type="linkedin"></vue-feather>
                                            LinkedIn
                                        </a><a class="btn btn-light" href="https://twitter.com/login?lang=en"
                                            target="_blank"><vue-feather class="txt-twitter"
                                                type="twitter"></vue-feather>twitter</a><a class="btn btn-light"
                                            href="https://www.facebook.com/" target="_blank"><vue-feather class="txt-fb"
                                                type="facebook"></vue-feather>facebook</a></div>
                                </div>
                                <p class="mt-4 mb-0 text-center">Don't have account?<router-link class="ms-2"
                                        to="/auth/register">Create Account</router-link></p>
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
let email = ref<string>("")
let formSubmitted = ref<boolean>(false)
let emailError = ref<boolean>(false)
let emailFieldClasses = ref<string>("")
let errors = ref([])
let password = ref<string>("")
let passwordError = ref<boolean>(false)
let type = ref<string>('password')
function validate() {
    formSubmitted.value = true;
    errors.value = [];
    if (email.value.length < 10 || email.value.search("@") == -1) {
        emailError.value = true;
        errors.value.push();
    } else {
        emailError.value = false;
        errors.value.push();
    }
    if (password.value.length < 7) {
        passwordError.value = true;

    } else {
        passwordError.value = false;
    }
}
function showPassword() {
    if (type.value === 'password') {
        type.value = 'text';
    } else {
        type.value = 'password';
    }
}
</script>