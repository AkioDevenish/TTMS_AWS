<template>
    <Card1 colClass="col-xl-6 col-lg-12" dropdown="true" headerTitle="true" title="Top seller of the month"
        cardhaderClass="card-no-border pb-0" titleClass="top-sellers" cardbodyClass="pt-0 seller-month px-0">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter"><label>Search:<input type="search" placeholder=""
                            v-model="filterQuery"></label></div>
                <table class="table display dataTable" id="seller-month" style="width:100%">
                    <thead>
                        <tr>
                            <th>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="">
                                    <label class="form-check-label"></label>
                                </div>
                            </th>
                            <th>Seller Name</th>
                            <th>Brand Name</th>
                            <th>Product</th>
                            <th>Sold</th>
                            <th>Price</th>
                            <th>Earnings</th>
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
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <div class="flex-shrink-0"><img :src="getImages(item.img)" alt="">
                                    </div>
                                    <div class="flex-grow-1"><router-link to="/ecommerce/details/1">
                                            <h6>{{ item.name }}</h6>
                                        </router-link></div>
                                </div>
                            </td>
                            <td>{{ item.brand }}</td>
                            <td>{{ item.product }}</td>
                            <td>{{ item.sold }} </td>
                            <td>
                                <p>${{ item.price }}</p>
                            </td>
                            <td>${{ item.earning }}</td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
        <ul class="pagination mx-2 mt-2 justify-content-end">
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
import { seller } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let data = ref()
let elementsPerPage = ref<number>(4)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any>([])
watch(filterQuery, (search: string) => {

    var filteredData = seller.filter((row) => {
        return (
            row.name.toLowerCase().includes(search.toLowerCase()) ||
            row.brand.toLowerCase().includes(search.toLowerCase()) ||
            row.product.toLowerCase().includes(search.toLowerCase()) ||
            row.sold.toLowerCase().includes(search.toLowerCase()) ||
            row.price.toLowerCase().includes(search.toLowerCase())
        );
    });
    search == "" ? allData.value = seller : allData.value = filteredData
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
    allData.value = seller;
})
</script>