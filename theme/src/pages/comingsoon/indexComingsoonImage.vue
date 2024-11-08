<template>
    <div class="container-fluid p-0 m-0">
        <div class="comingsoon comingsoon-bgimg">
            <div class="comingsoon-inner text-center"><img src="@/assets/images/other-images/logo-login.png" alt="">
                <h5>WE ARE COMING SOON</h5>
                <div class="countdown" id="clock-arrival" data-hours="1" data-minutes="2" data-seconds="3">
                    <ComingsoonTimer />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const ComingsoonTimer = defineAsyncComponent(() => import("@/components/common/ComingsoonTimer.vue"))
</script>