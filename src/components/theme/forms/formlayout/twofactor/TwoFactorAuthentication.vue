<template>
    <Card3 colClass="col-md-12" cardbodyClass="authentication-body">
        <div class="authentication-wrapper">
            <h4>Two-factor authentication</h4>
            <p>Click on the authentication button below and scan the QR code</p><img src="@/assets/images/forms/qr-scan.png"
                alt="qr-scan">
        </div>

        <AuthenticationModel />

        <a class="btn btn-primary mt-5" data-bs-toggle="modal" href="#exampleModalToggle" role="button">2 factor
            authentication</a>
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const AuthenticationModel = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/twofactor/AuthenticationModel.vue"))
</script>