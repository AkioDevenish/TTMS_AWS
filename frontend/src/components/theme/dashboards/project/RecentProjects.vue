<template>
    <Card1 colClass="col-xl-5 col-xl-70 col-md-12 proorder-md-3" dropdown="true" headerTitle="true" title="Recent Projects"
        cardhaderClass="card-no-border pb-0" cardbodyClass="p-0 projects">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter"><label>Search:<input type="search" placeholder=""
                            v-model="filterQuery"></label></div>
                <table class="table display dataTable  overflow-hidden" id="recent-product" style="width:100%">
                    <thead>
                        <tr>
                            <th>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="">
                                    <label class="form-check-label"></label>
                                </div>
                            </th>
                            <th>Name</th>
                            <th class="px-0">Team</th>
                            <th>started </th>
                            <th>finished</th>
                            <th>Progress </th>
                            <th class="px-2">Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="!get_rows().length">
                        <tr class="odd">
                            <td valign="top" colspan="6" class="dataTables_empty">No matching records found</td>
                        </tr>
                    </tbody>
                    <tbody v-if="get_rows().length">
                        <tr v-for="(row, index) in get_rows()" :key="index">
                            <td>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="">
                                    <label class="form-check-label"></label>
                                </div>
                            </td>
                            <td class="px-0"> <router-link to="/ecommerce/order_history">{{ row.name }}</router-link></td>
                            <td class="customers text-center social-group">
                                <ul>
                                    <li class="d-inline-block" v-for="(items, index) in row.children" :key="index">
                                        <img class="img-30 rounded-circle" :src="getImages(items.img)" alt="">
                                    </li>

                                    <li class="d-inline-block" v-if="row.more">
                                        <p class="bg-light rounded-circle">5+</p>
                                    </li>
                                </ul>
                            </td>
                            <td>{{ row.start }}</td>
                            <td> {{ row.finish }}</td>
                            <td class="radial-chart-wrap p-0">
                                <apexchart type="radialBar" height="70" ref="chart" :options="row.chart"
                                    :series="row.series">
                                </apexchart>
                            </td>
                            <td>
                                <div class="dropdown icon-dropdown">
                                    <button class="btn dropdown-toggle" id="userdropdown3" type="button"
                                        data-bs-toggle="dropdown" aria-expanded="false"><i
                                            class="icon-more-alt"></i></button>
                                    <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown3"><a
                                            class="dropdown-item" href="#">Weekly </a><a class="dropdown-item"
                                            href="#">Monthly</a><a class="dropdown-item" href="#">Yearly</a></div>
                                </div>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch } from 'vue'
import { recentdata } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let elementsPerPage = ref<number>(4)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any>([])
watch(filterQuery, (search: string) => {
    var filteredData = recentdata.filter((row) => {
        return (
            row.name.toLowerCase().includes(search.toLowerCase()) ||
            row.start.toLowerCase().includes(search.toLowerCase()) ||
            row.finish.toLowerCase().includes(search.toLowerCase())
        );
    });
    search == "" ? allData.value = recentdata : allData.value = filteredData
})
function get_rows() {
    var start = (currentPage.value - 1) * elementsPerPage.value;
    var end = start + elementsPerPage.value;
    return allData.value.slice(start, end);
}
onMounted(() => {
    allData.value = recentdata;
})
</script>