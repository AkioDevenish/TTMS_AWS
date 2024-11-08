<template>
    <div class="container-fluid">
        <div class="row">
            <BasicForm />
            <FloatingForm />
            <SelectSizing />
            <FileInput />
            <FlatInput />
            <HtmlInput />
            <FloatingInput />
            <EdgesInput />
            <RaiseInput />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicForm = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/BasicForm.vue"))
const FloatingForm = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/FloatingForm.vue"))
const SelectSizing = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/SelectSizing.vue"))
const FileInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/FileInput.vue"))
const FlatInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/FlatInput.vue"))
const HtmlInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/HtmlInput.vue"))
const FloatingInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/FloatingInput.vue"))
const EdgesInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/EdgesInput.vue"))
const RaiseInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/input/RaiseInput.vue"))
</script>