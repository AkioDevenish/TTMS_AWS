<template>
    <div class="container-fluid default-dashboard">
        <div class="row widget-grid">
         
        <ScheduledUpdates />
        <ZentraOverview />
        <BaraniOverview />
        <PawsOverview />
        <PawsOverview2 />
        <ActiveMembers /> 
        <HighestRecord/>
        <div class="col-xl-5 col-md-6 proorder-xl-3 proorder-md-1">
            <AWSstatus/>
        </div>
        </div>
    </div>
</template>
<script lang="ts" setup>

import { defineAsyncComponent } from 'vue'
const  ZentraOverview =  defineAsyncComponent(() => import('@/components/theme/dashboards/home/ZentraOverview.vue'))
const  BaraniOverview =  defineAsyncComponent(() => import('@/components/theme/dashboards/home/BaraniOverview.vue'))
const  PawsOverview =  defineAsyncComponent(() => import('@/components/theme/dashboards/home/PawsOverview.vue'))
const  PawsOverview2 = defineAsyncComponent(() => import('@/components/theme/dashboards/home/PawsOverview2.vue'))
const  AWSstatus =  defineAsyncComponent(() => import('@/components/theme/dashboards/home/AWSstatus.vue'))
const  WelcomeView = defineAsyncComponent(() => import("@/components/theme/dashboards/home/WelcomeView.vue"))
const  ActiveMembers = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ActiveMembers.vue"))
const  HighestRecord = defineAsyncComponent(() => import("@/components/theme/dashboards/home/HighestRecord.vue"))
const  ScheduledUpdates = defineAsyncComponent(() => import("@/components/theme/dashboards/home/ScheduledUpdates.vue"))
</script>

  