<template>
    <div class="container-fluid">
        <div class="user-profile">
            <div class="row">
                <AvatarSize />
                <AvatarStatus />
                <AvatarShapes />
                <AvatarRatio />
                <AvatarGrouping />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const AvatarSize = defineAsyncComponent(() => import("@/components/theme/uikits/avatar/AvatarSize.vue"))
const AvatarStatus = defineAsyncComponent(() => import("@/components/theme/uikits/avatar/AvatarStatus.vue"))
const AvatarShapes = defineAsyncComponent(() => import("@/components/theme/uikits/avatar/AvatarShapes.vue"))
const AvatarRatio = defineAsyncComponent(() => import("@/components/theme/uikits/avatar/AvatarRatio.vue"))
const AvatarGrouping = defineAsyncComponent(() => import("@/components/theme/uikits/avatar/AvatarGrouping.vue"))
</script>