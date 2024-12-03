<template>
      <div class="container-fluid">
        <div class="row">
            <DefaultBreadcrumb />
            <DividersBreadcrumbs />
            <IconsBreadcrumb />
            <NavBreadcrumb />
            <ColoredNavigation />
        </div>
        </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const DefaultBreadcrumb = defineAsyncComponent(() => import("@/components/theme/advance/breadcrumb/DefaultBreadcrumb.vue"))
const DividersBreadcrumbs = defineAsyncComponent(() => import("@/components/theme/advance/breadcrumb/DividersBreadcrumbs.vue"))
const IconsBreadcrumb = defineAsyncComponent(() => import("@/components/theme/advance/breadcrumb/IconsBreadcrumb.vue"))
const NavBreadcrumb = defineAsyncComponent(() => import("@/components/theme/advance/breadcrumb/NavBreadcrumb.vue"))
const ColoredNavigation = defineAsyncComponent(() => import("@/components/theme/advance/breadcrumb/ColoredNavigation.vue"))
</script>