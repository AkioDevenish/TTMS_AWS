<template>
    <div class="container-fluid">
        <div class="row">
            <ClickableValue />
            <MovieRating />
            <HeartRating />
            <StarRating />
            <DisabledRating />
            <AnimationRating />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const ClickableValue = defineAsyncComponent(() => import("@/components/theme/advance/rating/ClickableValue.vue"))
const MovieRating = defineAsyncComponent(() => import("@/components/theme/advance/rating/MovieRating.vue"))
const HeartRating = defineAsyncComponent(() => import("@/components/theme/advance/rating/HeartRating.vue"))
const StarRating = defineAsyncComponent(() => import("@/components/theme/advance/rating/StarRating.vue"))
const DisabledRating = defineAsyncComponent(() => import("@/components/theme/advance/rating/DisabledRating.vue"))
const AnimationRating = defineAsyncComponent(() => import("@/components/theme/advance/rating/AnimationRating.vue"))
</script>