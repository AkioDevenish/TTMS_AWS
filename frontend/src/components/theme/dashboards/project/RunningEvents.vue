<template>
    <Card1 colClass="col-xl-5 col-xl-70 proorder-md-13" dropdown="true" headerTitle="true" title="Running Events"
        cardhaderClass="card-no-border pb-0" cardbodyClass="rinning-col">

        <div class="row">
            <div class="col-6">
                <div class="running-box">
                    <div class="d-flex align-items-center justify-content-between gap-2">
                        <div class="flex-grow-1"><router-link to="/ecommerce/details/1">
                                <h5>Brooklyn Simmons</h5>
                            </router-link>
                            <p>Web Manager </p>
                        </div>
                        <div class="flex-shrink-0">
                            <div class="customers social-group">
                                <ul>
                                    <li class="d-inline-block" v-for="(item, index) in event" :key="index"><img
                                            class="rounded-circle" :src="getImages(item.img)" alt=""></li>

                                    <li class="d-inline-block">
                                        <p class="bg-light rounded-circle">5+</p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <p>With Asana, you can bring your teams, work, and apps from everywhere in one tool. Workflows
                        can be modified.</p>
                    <ul class="d-flex align-items-center gap-3">
                        <li class="bg-light">
                            <h5>$34,930</h5>
                            <p>Disbursed Budget</p>
                        </li>
                        <li class="bg-light">
                            <h5>$65,789</h5>
                            <p>Planned</p>
                        </li>
                    </ul>
                    <div>
                        <button class="btn bg-primary me-1">Upgrade Plan</button>
                        <button class="btn bg-secondary">View Project</button>
                    </div>
                </div>
            </div>
            <div class="col-6 running-events"><img src="@/assets/images/dashboard-2/round.png" alt="">
                <div> <img class="running-events-image" src="@/assets/images/dashboard-2/events-bg.png" alt="">
                </div>
            </div>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { event } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>