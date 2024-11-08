<template>
    <div class="container-fluid dashboard-2">
        <div class="row">
            <ProjectStatus />
            <RecentProjects />
            <TotalProject />
            <ProjectsOverview />
            <ClientsActivit />
            <ProjectCard />
            <TodaysTasks />
            <RunningEvents />
            <OnlineTimeline />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const ProjectStatus = defineAsyncComponent(() => import("@/components/theme/dashboards/project/ProjectStatus.vue"))
const TotalProject = defineAsyncComponent(() => import("@/components/theme/dashboards/project/TotalProject.vue"))
const ProjectsOverview = defineAsyncComponent(() => import("@/components/theme/dashboards/project/ProjectsOverview.vue"))
const ProjectCard = defineAsyncComponent(() => import("@/components/theme/dashboards/project/ProjectCard.vue"))
const TodaysTasks = defineAsyncComponent(() => import("@/components/theme/dashboards/project/TodaysTasks.vue"))
const RunningEvents = defineAsyncComponent(() => import("@/components/theme/dashboards/project/RunningEvents.vue"))
const RecentProjects = defineAsyncComponent(() => import("@/components/theme/dashboards/project/RecentProjects.vue"))
const ClientsActivit = defineAsyncComponent(() => import("@/components/theme/dashboards/project/ClientsActivit.vue"))
const OnlineTimeline = defineAsyncComponent(() => import("@/components/theme/dashboards/project/OnlineTimeline.vue"))
</script>