<template>
    <div class="container-fluid">
        <div class="alert txt-primary bg-light-primary alert-dismissible fade show" role="alert"><i
                data-feather="alert-triangle"></i>
            <p>This is the Typeahead page where <strong>jQuery </strong> was utilised.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="typeahead typeahead-wrapper">
            <div class="row">
                <BasicTypeahead />
                <PrefetchTypeahead />
                <BloodhoundTyeahead />
                <RemoteTypeahead />
                <CustomTemplates />
                <MultipleSections />
                <ScrollableMenu />
                <RtlSupport />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicTypeahead = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/BasicTypeahead.vue"))
const PrefetchTypeahead = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/PrefetchTypeahead.vue"))
const BloodhoundTyeahead = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/BloodhoundTyeahead.vue"))
const RemoteTypeahead = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/RemoteTypeahead.vue"))
const CustomTemplates = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/CustomTemplates.vue"))
const MultipleSections = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/MultipleSections.vue"))
const ScrollableMenu = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/ScrollableMenu.vue"))
const RtlSupport = defineAsyncComponent(() => import("@/components/theme/forms/formwidgets/typeahead/RtlSupport.vue"))
</script>