<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <AssignmentsTable />
            <StudyStatistics />
            <StudentCard />
       
  
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const StudentCard = defineAsyncComponent(() => import("@/components/common/StudentCard.vue"))
const StudyStatistics = defineAsyncComponent(() => import("@/components/theme/dashboards/education/StudyStatistics.vue"))
const AssignmentsTable = defineAsyncComponent(() => import("@/components/theme/dashboards/education/AssignmentsTable.vue"))
</script>