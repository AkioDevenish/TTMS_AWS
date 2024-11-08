<template>
    <Card1 colClass="col-xxl-5 col-xl-6 box-col-6 proorder-4-xl-1 proorder-md-7" dropdown="true" headerTitle="true"
        title="Featured Courses" cardhaderClass="card-no-border pb-0" cardbodyClass="p-0 featured-table">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <table class="table display dataTable" id="featured-table" style="width:100%">
                    <thead>
                        <tr>
                            <th>Course Name</th>
                            <th>Start</th>
                            <th>Rate</th>
                            <th>Type</th>
                            <th>Save</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in featured" :key="index">
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <div class="flex-shrink-0"> <img :src="getImages(item.img)" alt=""></div>
                                    <div class="flex-grow-1"><router-link to="/ecommerce/details/1">
                                            <h5>{{ item.name }}</h5>
                                        </router-link><span>{{ item.subname }}</span></div>
                                </div>
                            </td>
                            <td>{{ item.start }}</td>
                            <td> <span class="d-flex align-item-center gap-2 font-primary"> <vue-feather
                                        class="font-primary" type="star"></vue-feather>{{ item.rate }}</span></td>
                            <td>{{ item.type }}</td>
                            <td :class="item.isActive ? 'clicked-color' : 'initial-color'" id="colorChangeButton"
                                @click="bookmarkClick(item)">
                                <vue-feather :type="item.icon"></vue-feather>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { useCommonStore } from "@/store/common"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let store = useCommonStore()
let featured = store.featureds
function bookmarkClick(index: any) {
    index.isActive = !index.isActive;
}
</script>