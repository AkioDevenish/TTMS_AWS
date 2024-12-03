<template>
    <div class="col-sm-12">
        <div class="header-faq">
            <h4 class="mb-0">Browse articles by category</h4>
        </div>
        <div class="row">

            <Card3 colClass="col-sm-12" cardhaderClass="card-no-border pb-0" title="Browse Articles" headerTitle="true">
                <div class="row browse g-sm-4 g-3">
                    <div class="col-xl-4 xl-50 col-md-6" v-for="(item, index) in category" :key="index">
                        <div class="browse-articles browse-bottom">
                            <h5><span><vue-feather type="archive"></vue-feather> </span>{{ item.articles }}</h5>
                            <ul>
                                <li><router-link to="/">
                                        <span><vue-feather type="file-text"></vue-feather></span><span> {{
                                            item.articles1
                                        }}</span>
                                    </router-link></li>
                                <li><router-link to="/">
                                        <span><vue-feather type="file-text"></vue-feather></span><span>{{
                                            item.articles2 }}
                                        </span>
                                    </router-link></li>
                                <li><router-link to="/">
                                        <span><vue-feather type="file-text"></vue-feather></span><span>{{
                                            item.articles3 }}
                                        </span>
                                    </router-link></li>
                                <li><router-link to="/">
                                        <span><vue-feather type="file-text"></vue-feather></span><span>{{
                                            item.articles4
                                        }}</span>
                                    </router-link></li>
                                <li><router-link class="f-w-600 font-primary" to="/">
                                        <span><vue-feather class="me-1" type="arrow-right"></vue-feather></span>
                                        <span>See More ({{ item.see }})</span>
                                    </router-link>
                                </li>
                            </ul>
                        </div>
                    </div>

                </div>
            </Card3>

        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
import { category } from "@/core/data/knowledgebase"
</script>