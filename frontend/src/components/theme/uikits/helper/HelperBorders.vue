<template>
    <Card3 colClass="col-12" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Styles in borders" :desc="desc">
        <div class="row g-3">
            <div class="col-xxl-3 col-sm-6" v-for="(items, index) in borders" :key="index">
                <div class="border-wrapper h-100 alert-light-light dark-helper">
                    <h5 class="f-w-600 mb-3">{{ items.title }}</h5>
                    <div class="helper-common-box" v-for="(item, index) in items.children" :key="index">
                        <div class="helper-box" :class="item.class"></div><span>{{ item.title }}</span>
                    </div>

                </div>
            </div>
            <div class="col-xxl-3 col-sm-6" v-for="(items, index) in color" :key="index">
                <div class="border-wrapper alert-light-light h-100 dark-helper">
                    <h5 class="f-w-600 mb-3">{{ items.title }}</h5>
                    <div class="helper-common-box" v-for="(item, index) in items.children" :key="index">
                        <div class="helper-box helper-text border" :class="item.class">C </div>
                        <span>{{ item.title }}</span>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { color, borders } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the different styles of borders like: <code>border radius/border-color/border-width</code>. Use of any components.")
</script>