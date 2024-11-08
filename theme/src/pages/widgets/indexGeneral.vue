<template>
    <div class="container-fluid">
        <div class="row">
            <TotalSells doller="$ " />
            <WebsiteDesign />
            <OpeningLeaflets doller="$" col="col-xxl-3 col-xl-4 col-sm-6" />
            <VisitorsChart />
            <SocialWidget />
            <StudentCard />
            <AppointmentsData col="col-xxl-6 col-xl-6 box-col-6 proorder-xl-7 proorder-md-8"
                bodyclass="appointments relative pb-0" />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const TotalSells = defineAsyncComponent(() => import("@/components/common/TotalSells.vue"))
const WebsiteDesign = defineAsyncComponent(() => import("@/components/theme/widgets/general/WebsiteDesign.vue"))
const OpeningLeaflets = defineAsyncComponent(() => import("@/components/common/OpeningLeaflets.vue"))
const VisitorsChart = defineAsyncComponent(() => import("@/components/theme/widgets/general/VisitorsChart.vue"))
const SocialWidget = defineAsyncComponent(() => import("@/components/theme/widgets/general/SocialWidget.vue"))
const StudentCard = defineAsyncComponent(() => import("@/components/common/StudentCard.vue"))
const AppointmentsData = defineAsyncComponent(() => import("@/components/common/AppointmentsData.vue"))
</script>                     