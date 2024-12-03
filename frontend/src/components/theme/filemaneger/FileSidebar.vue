<template>
    <div class="col-xl-3">
        <div class="md-sidebar job-sidebar"><a class="btn btn-primary md-sidebar-toggle" href="javascript:void(0)"
                @click="collapseFilter()">file
                filter</a>
            <div class="md-sidebar-aside custom-scrollbar" :class="filtered ? 'open' : ''">
                <div class="file-sidebar">
                    <div class="card">
                        <div class="card-body">
                            <ul>
                                <li v-for="(item, index) in filebtn" :key="index">
                                    <div class="btn " :class="item.btnclass"><vue-feather :type="item.icon"></vue-feather>{{
                                        item.title }} </div>
                                </li>

                            </ul>
                            <hr>
                            <ul>
                                <li>
                                    <div class="btn btn-outline-primary"><vue-feather type="database"></vue-feather> Storage
                                    </div>
                                    <div class="m-t-15">
                                        <div class="progress sm-progress-bar mb-3">
                                            <div class="progress-bar bg-primary" role="progressbar" style="width: 25%"
                                                aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                        <h6 class="f-w-500">25 GB of 100 GB used</h6>
                                    </div>
                                </li>
                            </ul>
                            <hr>
                            <ul>
                                <li>
                                    <div class="btn btn-outline-primary"><vue-feather type="grid"></vue-feather> Pricing
                                        plan</div>
                                </li>
                                <li> </li>
                                <div class="pricing-plan">
                                    <h6>Trial Version </h6>
                                    <h5>FREE</h5>
                                    <p>100 GB Space</p>
                                    <div class="btn btn-outline-primary btn-xs">Selected</div><img class="bg-img"
                                        src="@/assets/images/dashboard/folder.png" alt="">
                                </div>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { filebtn } from "@/core/data/filemaneger"
let data = ref()
let filtered = ref<boolean>(false)

function collapseFilter() {
    filtered.value = !filtered.value;
}

</script>