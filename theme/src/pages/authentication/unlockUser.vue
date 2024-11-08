<template>
    <div class="container-fluid p-0">
        <div class="authentication-main mt-0">
            <div class="row">
                <div class="col-12">
                    <div class="login-card login-dark">
                        <div>
                            <div><a class="logo"><router-link to="/"><img class="img-fluid for-light"
                                            src="@/assets/images/logo/logo.png" alt="looginpage"><img
                                            class="img-fluid for-dark" src="@/assets/images/logo/logo_dark.png"
                                            alt="looginpage"></router-link></a></div>
                            <div class="login-main">
                                <form class="theme-form">
                                    <h4>Unlock </h4>
                                    <div class="form-group">
                                        <label class="col-form-label">Enter your Password</label>
                                        <div class="form-input position-relative">
                                            <input class="form-control" :type="type" name="login[password]" required
                                                placeholder="*********">
                                            <div class="show-hide"><span class="show" @click="showPassword"> </span></div>
                                        </div>
                                    </div>
                                    <div class="form-group mb-0">
                                        <div class="checkbox p-0">
                                            <input id="checkbox1" type="checkbox">
                                            <label class="text-muted" for="checkbox1">Remember password</label>
                                        </div>
                                        <button class="btn btn-primary btn-block w-100" type="submit">Unlock</button>
                                    </div>
                                    <p class="mt-4 mb-0">Already Have an account?<router-link class="ms-2"
                                            to="/auth/login">Sign in</router-link></p>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
const type = ref<string>('password')
function showPassword() {
    if (type.value === 'password') {
        type.value = 'text';
    } else {
        type.value = 'password';
    }
}
</script>