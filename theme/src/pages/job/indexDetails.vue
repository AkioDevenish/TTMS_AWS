<template>
    <div class="container-fluid">
        <div class="row">
            <JobSidebar />
            <JobDetails />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const JobSidebar = defineAsyncComponent(() => import("@/components/common/JobSidebar.vue"))
const JobDetails = defineAsyncComponent(() => import("@/components/theme/job/details/JobDetails.vue"))
</script>