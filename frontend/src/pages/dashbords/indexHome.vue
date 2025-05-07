<template>
    <div class="container-fluid default-dashboard">
        <div class="row widget-grid">
   
            <!-- Admin Components -->
            <template v-if="isAdmin">
                <ScheduledUpdates />
                <ActiveMembers :users="users" :loading="loading" />
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
import { defineAsyncComponent, onMounted, ref, computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUserStore } from '@/store/user'

const authStore = useAuthStore()
const { isAdmin, currentUser } = authStore
const userStore = useUserStore()
const users = computed(() => userStore.users)
const loading = computed(() => userStore.loading)
const showDebug = ref(true) // Set to false in production

// Admin/User components
const ScheduledUpdates = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ScheduledUpdates.vue"))
const ActiveMembers = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ActiveMembers.vue"))
const AWSstatus = defineAsyncComponent(() => import('@/components/theme/dashboards/home/AWSstatus.vue'))
const HighestRecord = defineAsyncComponent(() => import("@/components/theme/dashboards/home/HighestRecord.vue"))   
const StationsOverview = defineAsyncComponent(() => import("@/components/theme/dashboards/home/StationsOverview.vue"))
const InactiveSensors = defineAsyncComponent(() => import("@/components/theme/dashboards/home/InactiveSensors.vue"))
onMounted(() => {
    console.log('Is Admin:', isAdmin)
    console.log('Current User:', currentUser)
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

  