<template>
    <div class="container-fluid">
        <div class="row">
            <TwoFactorAuthentication />

            <Card3 colClass="col-md-12" cardbodyClass="email-verify">
                <div class="row g-3">
                    <EmailVerification />
                    <VerificationCode />
                </div>
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const TwoFactorAuthentication = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/twofactor/TwoFactorAuthentication.vue"))
const EmailVerification = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/twofactor/EmailVerification.vue"))
const VerificationCode = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/twofactor/VerificationCode.vue"))
</script>