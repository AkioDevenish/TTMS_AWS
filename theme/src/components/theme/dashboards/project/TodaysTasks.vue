<template>
    <Card1 colClass="col-xl-3 col-xl-40 col-md-6 proorder-md-11" dropdown="true" headerTitle="true" title="Today’s Tasks"
        cardhaderClass="card-no-border pb-0">

        <ul class="task-box">
            <li class="bg-light" v-for="(item, index) in task" :key="index">
                <div class="d-flex align-items-center justify-content-between">
                    <h6 class=" f-w-500" :class="item.class">{{ item.title }}</h6>
                    <div class="dropdown icon-dropdown">
                        <button class="btn dropdown-toggle" id="userdropdown25" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false"><i class="icon-more-alt"></i></button>
                        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown25"><a
                                class="dropdown-item" href="#">Weekly</a><a class="dropdown-item" href="#">Monthly</a><a
                                class="dropdown-item" href="#">Yearly </a></div>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-2">

                    <div class="flex-shrink-0" v-if="item.image">
                        <div class="customers social-group">
                            <ul>
                                <li class="d-inline-block"><img class="rounded-circle border-0" :src="getImages(item.img)"
                                        alt=""></li>
                                <li class="d-inline-block"><img class="rounded-circle" :src="getImages(item.img2)" alt="">
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="flex-shrink-0" v-else><img :src="getImages(item.img)" alt="user"></div>
                    <div class="flex-grow-1">
                        <p class="mb-0">Assigned to</p><router-link to="/ecommerce/details/1">
                            <h5>{{ item.desc }} </h5>
                        </router-link>
                    </div>
                </div>
            </li>

        </ul>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { task } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>