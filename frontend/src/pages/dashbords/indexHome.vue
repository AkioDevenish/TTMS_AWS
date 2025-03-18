<template>
    <div class="container-fluid default-dashboard">
        <div class="row widget-grid">
   
            <!-- Admin Components -->
            <template v-if="isAdmin">
                <ScheduledUpdates />
                <ActiveMembers />
                <AWSstatus/>
                <InactiveSensors/>
                <StationsOverview/>
           
            </template>

            <!-- Regular User Components -->
            <template v-else>
                <AWSstatus/>
                <HighestRecord/>
                <StationsOverview/>
          
            
            </template>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, ref } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { isAdmin, currentUser, checkAuth } = useAuth()
const showDebug = ref(true) // Set to false in production

// Admin/User components
const ScheduledUpdates = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ScheduledUpdates.vue"))
const ActiveMembers = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ActiveMembers.vue"))
const AWSstatus = defineAsyncComponent(() => import('@/components/theme/dashboards/home/AWSstatus.vue'))
const HighestRecord = defineAsyncComponent(() => import("@/components/theme/dashboards/home/HighestRecord.vue"))   
const StationsOverview = defineAsyncComponent(() => import("@/components/theme/dashboards/home/StationsOverview.vue"))
const InactiveSensors = defineAsyncComponent(() => import("@/components/theme/dashboards/home/InactiveSensors.vue"))
onMounted(async () => {
    await checkAuth()
    console.log('Is Admin:', isAdmin.value)
    console.log('Current User:', currentUser.value)
})
</script>

<style scoped>
.debug-info {
    background: #f5f5f5;
    padding: 10px;
    margin: 10px;
    border-radius: 4px;
    font-family: monospace;
}
</style>

  