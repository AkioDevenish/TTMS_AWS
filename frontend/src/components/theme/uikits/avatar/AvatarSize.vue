<template>
    <Card3 colClass="col-xl-4 col-md-6" cardClass="height-equal" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Sizes" :desc="desc">
        <div class="avatar-showcase">
            <div class="avatars">
                <div class="avatar" v-for="(item, index) in size" :key="index"><img class="rounded-circle"
                        :class="item.class" :src="getImages(item.img)" alt="#">
                </div>

            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { size } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("You can change the size of avatar using <code>.img- * (70/80/90/100)</code> class.")
</script>