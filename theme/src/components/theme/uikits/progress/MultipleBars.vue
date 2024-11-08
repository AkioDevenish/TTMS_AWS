<template>
    <Card3 colClass="col-xl-6" cardbodyClass="progress-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Multiple bars" :desc="desc">
        <div class="row">
            <div class="col">
                <div class="progress">
                    <div class="progress-bar bg-primary" role="progressbar" style="width: 30%" aria-valuenow="30"
                        aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-secondary" role="progressbar" style="width: 20%" aria-valuenow="20"
                        aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-success" role="progressbar" style="width: 15%" aria-valuenow="15"
                        aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <div class="progress">
                    <div class="progress-bar " :class="item.class" v-for="(item, index) in multiple" :key="index"
                        role="progressbar" style="width: 10%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
            </div>
        </div>
    </Card3>


    <Card3 colClass="col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Progress with number steps" :desc="desc1">
        <div class="position-relative m-3 progress-number">
            <div class="progress progress-wrapper">
                <div class="progress-bar" role="progressbar" aria-label="Progress" style="width: 50%;" aria-valuenow="50"
                    aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <button class="position-absolute top-0 start-0 translate-middle font-light btn-sm btn-primary rounded-circle"
                type="button">1</button>
            <button class="position-absolute top-0 start-50 translate-middle font-light btn-sm btn-primary rounded-circle"
                type="button">2</button>
            <button class="progress-btn position-absolute top-0 start-100 translate-middle btn-sm rounded-circle"
                type="button">3</button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { multiple } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Include multiple progress bars in a progress component if you need.")
let desc1 = ref<string>(" Use the <code>.position-absolute </code>to set progress numbers steps.")
</script>