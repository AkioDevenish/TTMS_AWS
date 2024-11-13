<template>
    <div class="table-responsive theme-scrollbar">
        <form>
            <div class="mb-3 row justify-content-end">
                <label for="table-complete-search" class="col-xs-3 col-sm-auto col-form-label">Search:</label>
                <div class="col-xs-3 col-sm-auto">
                    <input id="table-complete-search" type="text" class="form-control" v-model="filterQuery">
                </div>
            </div>
            <table class="table display dataTable" id="basic-6">
                <thead>
                    <tr>
                        <th colspan="4"></th>
                        <th colspan="4"></th>
                    </tr>
                    <tr>
                        <th>User Account</th>
                        <th>Key</th>
                        <th>First Used</th>
                        <th>Last Used</th>
                        <th>Status</th>
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
                            <div class="d-flex"><img class="rounded-circle img-30 me-3" :src="getImages(row.img)"
                                    alt="Generic placeholder image">
                                <div class="flex-grow-1 align-self-center">
                                    <div>{{ row.name }}</div>
                                </div>
                            </div>
                        </td>
                        <td>{{ row.key }}</td>
                        <td>{{ row.first_used }}</td>
                        <td>{{ row.last_used }}</td>
                        <td>{{ row.status }}</td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <th>User Account</th>
                        <th>Key</th>
                        <th>First Used</th>
                        <th>Last Used</th>
                        <th>Status</th>
                    </tr>
                </tfoot>
            </table>
            <ul class="pagination m-2 justify-content-end pagination-primary">
                <li class="page-item"><a class="page-link" @click="prev()">Previous</a></li>
                <li class="page-item" v-for="i in num_pages()" :key="i" v-bind:class="[i == currentPage ? 'active' : '']"
                    v-on:click="change_page(i)">
                    <a class="page-link">{{ i }}</a>
                </li>
                <li class="page-item"><a class="page-link" @click="change()">Next</a></li>
            </ul>
        </form>
    </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, watch } from "vue"
import { items } from "@/core/data/support"
import { getImages } from "@/composables/common/getImages"
let elementsPerPage = ref<number>(10)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any[]>([])
onMounted(() => {
    allData.value = items;
})
watch(filterQuery, (search: string) => {

    var filteredData = items.filter((row) => {
        return (
            row.name.toLowerCase().includes(search.toLowerCase()) || row.first_used.toLowerCase().includes(search.toLowerCase()) || row.last_used.toLowerCase().includes(search.toLowerCase()) || row.status.toLowerCase().includes(search.toLowerCase())
        );
    });
    search == "" ? allData.value = items : allData.value = filteredData
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
function removeProduct(index: any) {
    items.splice(index, 1)
}
</script>