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
                        <th>Name</th>
                        <th>Organization</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Package</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody v-if="!get_rows().length">
                    <tr class="odd">
                        <td valign="top" colspan="6" class="dataTables_empty">
                            {{ loading ? 'Loading...' : 'No matching records found' }}
                        </td>
                    </tr>
                </tbody>
                <tbody v-if="get_rows().length">
                    <tr v-for="(row, index) in get_rows()" :key="index">
                        <td>{{ row.name }}</td>
                        <td>{{ row.organization }}</td>
                        <td>{{ row.email }}</td>
                        <td>{{ row.role }}</td>
                        <td>{{ row.package }}</td>
                        <td>
                            <span :class="['badge', row.is_active ? 'bg-success' : 'bg-danger']">
                                {{ row.is_active ? 'Active' : 'Inactive' }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
            <ul class="pagination m-2 justify-content-end pagination-primary">
                <li class="page-item"><a class="page-link" @click="prev()">Previous</a></li>
                <li class="page-item" 
                    v-for="i in num_pages()" 
                    :key="i" 
                    :class="{ active: i === currentPage }"
                    @click="change_page(i)">
                    <a class="page-link">{{ i }}</a>
                </li>
                <li class="page-item"><a class="page-link" @click="change()">Next</a></li>
            </ul>
        </form>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from "vue"
import axios from 'axios'

interface User {
    id: number;
    name: string;
    email: string;
    organization: string;
    role: string;
    package: string;
    is_active: boolean;
}

const elementsPerPage = ref<number>(10)
const currentPage = ref<number>(1)
const filterQuery = ref<string>("")
const allData = ref<User[]>([])
const loading = ref<boolean>(true)

// Fetch users from API
const fetchUsers = async () => {
    try {
        loading.value = true
        const response = await axios.get('http://127.0.0.1:8000/users/')
        allData.value = response.data
    } catch (error) {
        console.error('Error fetching users:', error)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchUsers()
})

// Search functionality
watch(filterQuery, (search: string) => {
    if (!search) {
        fetchUsers()
        return
    }

    const searchLower = search.toLowerCase()
    allData.value = allData.value.filter((user) => {
        return (
            user.name?.toLowerCase().includes(searchLower) ||
            user.email?.toLowerCase().includes(searchLower) ||
            user.organization?.toLowerCase().includes(searchLower) ||
            user.role?.toLowerCase().includes(searchLower)
        )
    })
})

// Pagination functions
function get_rows() {
    const start = (currentPage.value - 1) * elementsPerPage.value
    const end = start + elementsPerPage.value
    return allData.value.slice(start, end)
}

function num_pages() {
    return Math.ceil(allData.value.length / elementsPerPage.value)
}

function change_page(page: number) {
    currentPage.value = page
}

function change() {
    if (currentPage.value < num_pages()) {
        currentPage.value++
    }
}

function prev() {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}
</script>

<style scoped>
.badge {
    padding: 0.5em 1em;
    border-radius: 0.25rem;
    font-weight: 500;
}

.table th, .table td {
    vertical-align: middle;
}

.page-item {
    cursor: pointer;
}

.page-item.active .page-link {
    background-color: #7A70BA;
    border-color: #7A70BA;
}
</style>