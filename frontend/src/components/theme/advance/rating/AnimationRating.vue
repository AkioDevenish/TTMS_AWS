<template>
    <Card3 colClass="col-xxl-4 col-md-6" cardhaderClass="height-equal" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Animated Rating Bar" :desc="desc">
        <div class="rating-container">
            <ul class="feedback">
                <li class=" me-0" v-for="(item, index) in data" :key="index"
                    :class="[{ active: item.isActive }, item.class]" @click="handleClick(item)">
                    <div v-if="item.eye">
                        <svg class="eye left">
                            <use xlink:href="@/assets/svg/icon-sprite.svg#eye"></use>
                        </svg>
                        <svg class="eye right">
                            <use xlink:href="@/assets/svg/icon-sprite.svg#eye"></use>
                        </svg>
                        <svg class="mouth">
                            <use xlink:href="@/assets/svg/icon-sprite.svg#mouth"></use>
                        </svg>
                    </div>
                    <div v-if="item.eyes"></div>
                    <div v-if="item.happy">
                        <svg class="eye left">
                            <use xlink:href="@/assets/svg/icon-sprite.svg#eye"></use>
                        </svg>
                        <svg class="eye right">
                            <use xlink:href="@/assets/svg/icon-sprite.svg#eye"></use>
                        </svg>
                    </div>
                </li>


            </ul>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { animationrating } from "@/core/data/advance"
import { useAdvanceStore } from "@/store/advance"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Star rating is displayed using <code>#u-rating-fontawesome-o </code> id using javascript.")
const store = useAdvanceStore()
const data = store.data
const handleClick = (clickedEntry) => {
    if (!clickedEntry.isActive) {
        const previousActive = data.find((item) => item.isActive);
        if (previousActive) {
            previousActive.isActive = false;
        }
        clickedEntry.isActive = true;
    }
};

</script>