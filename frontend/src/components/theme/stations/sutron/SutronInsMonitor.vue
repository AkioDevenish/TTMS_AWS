<template>
    <Card1 colClass="col-xl-12 col-md-12 proorder-md-1" headerTitle="true" title="Sutron Monitor "
        cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 assignments-table px-0">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <table class="table display dataTable" id="assignments-table" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>ID</th>
                            <th>Last Updated</th>
                            <th>Time</th>
                            <th>Status</th>
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
                                <div class="d-flex align-items-center">
                                <div class="d-flex align-items-center"><router-link to="/dashboards/dashboard_education">
                                            <h6>{{ item.name }}</h6>
                                        </router-link></div>
                                    <div class="active-status active-online"></div>
                                </div>
                            </td>
                        
                            <td>{{ item.id }}</td>
                            <td>{{ item.date }} </td>
                            <td>{{ item.time }} </td>
                            <td>{{ item.status }} </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
      
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch } from 'vue'
import { sutronmonitor } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let elementsPerPage = ref<number>(4)
let currentPage = ref<number>(1)
let allData = ref<any>([])

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
    allData.value = sutronmonitor;
})
</script>