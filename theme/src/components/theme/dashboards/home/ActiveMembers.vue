<template>
    <Card1 colClass="col-xl-7 col-md-6 box-col-5 proorder-xl-3 proorder-md-2" headerTitle="true"
        title="Recent Memembers " cardhaderClass="card-no-border pb-0" cardbodyClass="active-members px-0 pb-0 ">

        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>Member Profile</th>
                        <th></th>
                        <th class="text-center">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in membersbox" :key="index">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="flex-shrink-0"><img :src="getImages(item.img)" alt="">
                                </div>
                                <div class="flex-grow-1"><router-link to="/ecommerce/product">
                                        <h5>{{ item.name }}</h5>
                                    </router-link><span>{{ item.desc }}</span></div>
                            </div>
                        </td>
                        <td></td>
                        <td>
                            <p class="members-box text-center " :class="item.statusclass">
                                {{ item.status }}</p>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { membersbox } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>