<template>
    <div class="container-fluid dashboard-3">
        <div class="row">
            <TotalSells />
            <RecentOrders />
            <SalesOverview />
            <RecentCustomers />
            <RevenueCategory />
            <UserContinent />
            <ProductDetail />
            <TopSeller />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const TotalSells = defineAsyncComponent(() => import("@/components/common/TotalSells.vue"))
const RecentOrders = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/RecentOrders.vue"))
const SalesOverview = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/SalesOverview.vue"))
const RecentCustomers = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/RecentCustomers.vue"))
const RevenueCategory = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/RevenueCategory.vue"))
const UserContinent = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/UserContinent.vue"))
const ProductDetail = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/ProductDetail.vue"))
const TopSeller = defineAsyncComponent(() => import("@/components/theme/dashboards/ecommerce/TopSeller.vue"))
</script>