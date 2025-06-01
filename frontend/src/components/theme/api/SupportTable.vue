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
                        <th>UUID</th>
                        <th>Name</th>
                        <th>User</th>
                        <th>Created At</th>
                        <th>Last Used</th>
                        <th>Expires At</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody v-if="isLoading">
                    <tr>
                        <td colspan="7" class="text-center">Loading...</td>
                    </tr>
                </tbody>
                <tbody v-else-if="!get_rows().length">
                    <tr class="odd">
                        <td valign="top" colspan="7" class="dataTables_empty">No matching records found</td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr v-for="(row, index) in get_rows()" :key="row.id">
                        <td>{{ row.uuid }}</td>
                        <td>{{ row.token_name }}</td>
                        <td>{{ row.user_email || row.user || '-' }}</td>
                        <td>{{ formatDate(row.created_at) }}</td>
                        <td>{{ row.last_used ? formatDate(row.last_used) : 'Never' }}</td>
                        <td>{{ formatDate(row.expires_at) }}</td>
                        <td>{{ getStatus(row) }}</td>
                    </tr>
                </tbody>
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
import axios from "axios"
let elementsPerPage = ref<number>(10)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any[]>([])
let isLoading = ref<boolean>(true)

onMounted(async () => {
    await fetchApiAccessKeys();
})

async function fetchApiAccessKeys() {
    isLoading.value = true;
    try {
        const response = await axios.get('/api-keys/');
        allData.value = response.data;
    } catch (error) {
        allData.value = [];
    } finally {
        isLoading.value = false;
    }
}

watch(filterQuery, (search: string) => {
    if (!search) {
        fetchApiAccessKeys();
        return;
    }
    const lower = search.toLowerCase();
    allData.value = allData.value.filter((row) => {
        return (
            (row.token_name && row.token_name.toLowerCase().includes(lower)) ||
            (row.uuid && row.uuid.toLowerCase().includes(lower)) ||
            (row.user_email && row.user_email.toLowerCase().includes(lower)) ||
            (row.user && row.user.toString().toLowerCase().includes(lower))
        );
    });
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
function formatDate(dateString: string) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}
function getStatus(row: any) {
    if (!row.expires_at) return 'Unknown';
    return new Date(row.expires_at) > new Date() ? 'Active' : 'Inactive';
}
</script>