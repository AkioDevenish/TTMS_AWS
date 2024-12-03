<template>
    <Card1 colClass="col-xl-6 proorder-xl-5 box-col-7 proorder-md-5"  headerTitle="true" title="Highest Records"
        cardhaderClass="card-no-border" cardbodyClass="projects px-0 pt-1">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter"><label>Search:<input type="search" placeholder=""
                            v-model="filterQuery"></label></div>
                <table class="table display dataTable no-footer" id="information" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Date</th>
                            <th>Unit</th>
                            <th>Unit Type</th>
                            <th>Value</th>
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
                                <div class="d-flex align-items-center">
                                            <h6>{{ row.title }}</h6>
                                      </div>
                            </td>
                            <td class="project-dot">
                                <div class="d-flex">
                                    <div class="flex-shrink-0"><span :class="row.bgclass"></span></div>
                                    <div class="flex-grow-1">
                                        <h6>{{ row.file }}</h6>
                                    </div>
                                </div>
                            </td>   
                            <td>{{ row.date }}</td>
                            <td>{{ row.value }}</td>
                            <td>{{ row.unit }}</td>
                            <td>{{ row.type }}</td>
                     
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
import { project } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let elementsPerPage = ref<number>(4)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any>([])
watch(filterQuery, (search: string) => {

    var filteredData = project.filter((row) => {
        return (
            row.title.toLowerCase().includes(search.toLowerCase()) ||
            row.date.toLowerCase().includes(search.toLowerCase()) ||
            row.file.toLowerCase().includes(search.toLowerCase()) ||
            row.value.toLowerCase().includes(search.toLowerCase())
        );
    });
    search == "" ? allData.value = project : allData.value = filteredData
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
    allData.value = project;
})
</script>