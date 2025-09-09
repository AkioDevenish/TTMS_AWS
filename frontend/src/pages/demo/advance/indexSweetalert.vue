<template>
    <div class="container-fluid">
        <div class="row">
            <BasicAlert />
            <TextUnder />
            <InfoAlert />
            <WarningAlert />
            <PikachuAlert />
            <QuestionsAlert />
            <UsernameAlert />
            <SuccessMessage />
            <DangerAlert />
            <WarningMode />
            <AutoClose />
            <RequestMovie />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/BasicAlert.vue"))
const TextUnder = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/TextUnder.vue"))
const InfoAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/InfoAlert.vue"))
const WarningAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/WarningAlert.vue"))
const PikachuAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/PikachuAlert.vue"))
const QuestionsAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/QuestionsAlert.vue"))
const UsernameAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/UsernameAlert.vue"))
const SuccessMessage = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/SuccessMessage.vue"))
const DangerAlert = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/DangerAlert.vue"))
const WarningMode = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/WarningMode.vue"))
const AutoClose = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/AutoClose.vue"))
const RequestMovie = defineAsyncComponent(() => import("@/components/theme/advance/sweealert/RequestMovie.vue"))
</script>