<template>
    <div class="container-fluid default-dashboard">
        <div class="row widget-grid">
            <WelcomeView />
            <OpeningLeaflets doller="$" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <ShiftsOverview />
            <ProjectData />
            <CustomerTransaction />
            <SalesStatistic />
            <ActiveMembers />
            <AtmosTemp doller="°C" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <AtmosDuepoint doller="°C" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <AtmosHumid doller="%" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <AtmosIrradiation doller="W/m2" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <AtmosRai doller="mm" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            <AtmosPress doller="hPa" col="col-xl-3 col-md-6 proorder-xl-2 proorder-md-2" />
            
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import AtmosHumid from '@/components/common/AtmosHumid.vue';
import AtmosTemp from '@/components/common/AtmosTemp.vue';
import AtmosRai from '@/components/common/AtmosRai.vue';
import AtmosDuepoint from '@/components/common/AtmosDuepoint.vue';
import AtmosIrradiation from '@/components/common/AtmosIrradiation.vue';
import AtmosPress from '@/components/common/AtmosPress.vue';
const WelcomeView = defineAsyncComponent(() => import("@/components/theme/dashboards/default/WelcomeView.vue"))
const OpeningLeaflets = defineAsyncComponent(() => import("@/components/common/OpeningLeaflets.vue"))
const ShiftsOverview = defineAsyncComponent(() => import("@/components/theme/dashboards/default/ShiftsOverview.vue"))
const CustomerTransaction = defineAsyncComponent(() => import("@/components/theme/dashboards/default/CustomerTransaction.vue"))
const SalesStatistic = defineAsyncComponent(() => import("@/components/theme/dashboards/default/SalesStatistic.vue"))
const ProjectData = defineAsyncComponent(() => import("@/components/theme/dashboards/default/ProjectData.vue"))
//const NotificationsData = defineAsyncComponent(() => import("@/components/theme/dashboards/default/NotificationsData.vue"))
//const AppointmentsData = defineAsyncComponent(() => import("@/components/common/AppointmentsData.vue"))
const ActiveMembers = defineAsyncComponent(() => import("@/components/theme/dashboards/default/ActiveMembers.vue"))
//const SaleProduct = defineAsyncComponent(() => import("@/components/theme/dashboards/default/SaleProduct.vue"))
</script>

  