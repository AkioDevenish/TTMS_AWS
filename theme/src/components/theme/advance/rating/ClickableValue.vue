<template>
    <Card3 colClass="col-xxl-4 col-md-6" cardhaderClass="rating-header" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Clickable Value" :desc="desc">
        <div class="rating-container">
            <star-rating :show-rating="false" :star-size="20" :max-rating="10"
                @update:rating="rating = $event"></star-rating>
            <pre class="mb-0 rating-pre px-2">Rating {{ rating }}</pre>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import StarRating from 'vue-star-rating';
import { ref, defineAsyncComponent } from "vue"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Clickable Value is displayed using <code>#u-rating-Clickable</code> id using javascript.")
const rating = ref<string>("0")
</script>