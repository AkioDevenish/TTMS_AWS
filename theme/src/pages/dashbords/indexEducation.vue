<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <StudentCard />
            <StudyStatistics />
            <AssignmentsTable />
            <LiveMeeting />
            <ActivelyHours />
            <EnrolledClasses />
            <FeaturedCourses />
            <MonthlyAttendance />
            <ScheduleData />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const StudentCard = defineAsyncComponent(() => import("@/components/common/StudentCard.vue"))
const StudyStatistics = defineAsyncComponent(() => import("@/components/theme/dashboards/education/StudyStatistics.vue"))
const AssignmentsTable = defineAsyncComponent(() => import("@/components/theme/dashboards/education/AssignmentsTable.vue"))
const LiveMeeting = defineAsyncComponent(() => import("@/components/theme/dashboards/education/LiveMeeting.vue"))
const ActivelyHours = defineAsyncComponent(() => import("@/components/theme/dashboards/education/ActivelyHours.vue"))
const EnrolledClasses = defineAsyncComponent(() => import("@/components/theme/dashboards/education/EnrolledClasses.vue"))
const FeaturedCourses = defineAsyncComponent(() => import("@/components/theme/dashboards/education/FeaturedCourses.vue"))
const MonthlyAttendance = defineAsyncComponent(() => import("@/components/theme/dashboards/education/MonthlyAttendance.vue"))
const ScheduleData = defineAsyncComponent(() => import("@/components/theme/dashboards/education/ScheduleData.vue"))
</script>