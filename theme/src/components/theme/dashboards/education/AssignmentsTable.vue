<template>
    <Card1 colClass="col-xl-8 col-md-12 proorder-md-4" dropdown="true" headerTitle="true" title="Assignments"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 assignments-table px-0">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter"><label>Search:<input type="search" placeholder=""
                            v-model="filterQuery"></label></div>
                <table class="table display dataTable" id="assignments-table" style="width:100%">
                    <thead>
                        <tr>
                            <th>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="">
                                    <label class="form-check-label"></label>
                                </div>
                            </th>
                            <th>Id no </th>
                            <th>Teacher</th>
                            <th>Subject </th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Progress</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="!get_rows().length">
                        <tr class="odd">
                            <td valign="top" colspan="6" class="dataTables_empty">No matching records found</td>
                        </tr>
                    </tbody>
                    <tbody>
                        <tr v-for="(item, index) in get_rows()" :key="index">
                            <td>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="">
                                    <label class="form-check-label"></label>
                                </div>
                            </td>
                            <td> <span>{{ item.no }}</span></td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0"><img :src="getImages(item.img)" alt=""></div>
                                    <div class="flex-grow-1 ms-2"><router-link to="/ecommerce/details/1">
                                            <h6>{{ item.name }}</h6>
                                        </router-link></div>
                                    <div class="active-status active-online"></div>
                                </div>
                            </td>
                            <td>{{ item.subject }}</td>
                            <td>{{ item.start }} </td>
                            <td>{{ item.end }}</td>
                            <td>
                                <div class="progress-showcase">
                                    <div class="progress sm-progress-bar " :class="item.progressclass">
                                        <div class="progress-bar" role="progressbar" :style="{ 'width': item.width }"
                                            aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"> </div>
                                    </div>
                                </div>
                            </td>
                            <td class="text-center">
                                <div class="dropdown icon-dropdown">
                                    <button class="btn dropdown-toggle" id="userdropdown2" type="button"
                                        data-bs-toggle="dropdown" aria-expanded="false"><i
                                            class="icon-more-alt"></i></button>
                                    <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown2"><a
                                            class="dropdown-item" href="#">Weekly</a><a class="dropdown-item"
                                            href="#">Monthly</a><a class="dropdown-item" href="#">Yearly</a></div>
                                </div>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
        <ul class="pagination mx-2 mt-2 justify-content-end ">
            <li class="page-item"><a class="page-link" @click="prev()">Previous</a></li>
            <li class="page-item" v-for="i in num_pages()" :key="i" v-bind:class="[i == currentPage ? 'active' : '']"
                v-on:click="change_page(i)">
                <a class="page-link">{{ i }}</a>
            </li>
            <li class="page-item"><a class="page-link" @click="change()">Next</a></li>
        </ul>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch } from 'vue'
import { assignments } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let elementsPerPage = ref<number>(4)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any>([])
watch(filterQuery, (search: string) => {

    var filteredData = assignments.filter((row) => {
        return (
            row.no.toLowerCase().includes(search.toLowerCase()) ||
            row.name.toLowerCase().includes(search.toLowerCase()) ||
            row.subject.toLowerCase().includes(search.toLowerCase()) ||
            row.start.toLowerCase().includes(search.toLowerCase()) ||
            row.end.toLowerCase().includes(search.toLowerCase())
        );
    });
    search == "" ? allData.value = assignments : allData.value = filteredData
})
function get_rows() {
    var start = (currentPage.value - 1) * elementsPerPage.value;
    var end = start + elementsPerPage.value;
    return allData.value.slice(start, end);
}
function num_pages() {
    return Math.ceil(allData.value.length / elementsPerPage.value);
}
function change_page(page: number) {
    currentPage.value = page;
}
function change() {
    if (currentPage.value < Math.ceil(allData.value.length / elementsPerPage.value)) {
        currentPage.value++;
    }
}
function prev() {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
}

onMounted(() => {
    allData.value = assignments;
})
</script>