<template>
    <Card1 colClass="col-xxl-3 col-xl-5 box-col-5 col-md-6 proorder-md-6" dropdown="true" headerTitle="true"
        title="Enrolled Classes" cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 pb-1">
        <ul class="enrolled-class">
            <li class="d-flex align-items-center gap-2" v-for="(item, index) in enrolled" :key="index"><span
                    :class="item.class"></span>
                <div class="flex-grow-1"> <a href="">
                        <h5 class="text-truncate">{{ item.title }}</h5>
                    </a>
                    <p>{{ item.time }}</p>
                </div>
                <div class="flex-shrink-0">
                    <div class="dropdown icon-dropdown">
                        <button class="btn dropdown-toggle" id="userdropdown12" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false"><i class="icon-angle-right"></i></button>
                        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown12"><a
                                class="dropdown-item" href="#">Weekly</a><a class="dropdown-item" href="#">Monthly</a><a
                                class="dropdown-item" href="#">Yearly</a></div>
                    </div>
                </div>
            </li>
        </ul>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { enrolled } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let data = ref()
</script>