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
                            <div class="dropdown status-dropdown">
                                <button 
                                    class="btn status-btn dropdown-toggle" 
                                    :class="getStatusClass(row.status)"
                                    type="button" 
                                    data-bs-toggle="dropdown" 
                                    aria-expanded="false"
                                >
                                    <span class="status-dot" :class="getStatusDotClass(row.status)"></span>
                                    {{ row.status }}
                                </button>
                                <ul class="dropdown-menu status-menu">
                                    <li v-for="status in getAvailableStatuses(row.status)" :key="status">
                                        <a 
                                            class="dropdown-item status-item" 
                                            href="#" 
                                            @click.prevent="updateUserStatus(row.id, status)"
                                            :class="{ 
                                                'active': row.status === status,
                                                [`status-${status.toLowerCase()}`]: true
                                            }"
                                        >
                                            <span class="status-dot" :class="getStatusDotClass(status)"></span>
                                            {{ status }}
                                        </a>
                                    </li>
                                </ul>
                            </div>
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
    status: string;
}

const elementsPerPage = ref<number>(10)
const currentPage = ref<number>(1)
const filterQuery = ref<string>("")
const allData = ref<User[]>([])
const loading = ref<boolean>(true)

// Fetch users from API
const fetchUsers = async () => {
    try {
        loading.value = true;
        const response = await axios.get('http://127.0.0.1:8000/users/');
        // Map the response data to ensure new users are set to Pending
        allData.value = response.data.map((user: any) => ({
            ...user,
            status: user.status || 'Pending' // Default to Pending if no status
        }));
    } catch (error) {
        console.error('Error fetching users:', error);
    } finally {
        loading.value = false;
    }
};

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

const getStatusDotClass = (status: string): string => {
    const classes = {
        'Active': 'dot-success',
        'Pending': 'dot-warning',
        'Inactive': 'dot-danger'
    };
    return classes[status as keyof typeof classes] || 'dot-warning'; // Default to warning for Pending
};

const getStatusClass = (status: string): string => {
    const classes = {
        'Active': 'status-btn-success',
        'Pending': 'status-btn-warning',
        'Inactive': 'status-btn-danger'
    };
    return classes[status as keyof typeof classes] || 'status-btn-warning'; // Default to warning style for Pending
};

const updateUserStatus = async (userId: number, newStatus: string) => {
    try {
        const response = await axios.patch(`http://127.0.0.1:8000/users/${userId}/`, {
            status: newStatus
        });
        
        if (response.status === 200) {
            // Update the local data
            const userIndex = allData.value.findIndex(user => user.id === userId);
            if (userIndex !== -1) {
                allData.value[userIndex].status = newStatus;
            }
        }
    } catch (error) {
        console.error('Error updating user status:', error);
    }
};

const getAvailableStatuses = (currentStatus: string): string[] => {
    if (currentStatus === 'Pending') {
        return ['Active', 'Inactive'];
    }
    return ['Active', 'Inactive'];
};
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

.dropdown-toggle::after {
    margin-left: 0.5em;
}

.dropdown-menu {
    min-width: 8rem;
}

.dropdown-item.active {
    background-color: #7A70BA;
    color: white;
}

.btn-success {
    background-color: #28a745;
    color: white;
}

.btn-warning {
    background-color: #ffc107;
    color: #212529;
}

.btn-danger {
    background-color: #dc3545;
    color: white;
}

.btn-secondary {
    background-color: #6c757d;
    color: white;
}

.dropdown-toggle:hover {
    opacity: 0.9;
}

.status-dropdown {
    position: relative;
}

.status-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    min-width: 120px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

.dot-success { background-color: #28a745; }
.dot-warning { background-color: #ffc107; }
.dot-danger { background-color: #dc3545; }
.dot-secondary { background-color: #6c757d; }

.status-btn-success {
    background-color: rgba(40, 167, 69, 0.1);
    color: #28a745;
}

.status-btn-warning {
    background-color: rgba(255, 193, 7, 0.1);
    color: #856404;
    border: 1px solid rgba(255, 193, 7, 0.2);
}

.status-btn-danger {
    background-color: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.status-btn-secondary {
    background-color: rgba(108, 117, 125, 0.1);
    color: #6c757d;
}

.status-menu {
    min-width: 140px;
    padding: 0.5rem;
    border: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    border-radius: 6px;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 4px;
    margin: 2px 0;
}

.status-item:hover {
    background-color: #f8f9fa;
}

.status-item.active {
    background-color: #f8f9fa;
    font-weight: 500;
}

.dropdown-toggle::after {
    margin-left: auto;
}

/* Status-specific hover effects */
.status-Active:hover {
    color: #28a745;
    background-color: rgba(40, 167, 69, 0.1);
}

.status-Pending:hover {
    color: #856404;
    background-color: rgba(255, 193, 7, 0.1);
}

.status-Inactive:hover {
    color: #dc3545;
    background-color: rgba(220, 53, 69, 0.1);
}

.status-Pending {
    color: #856404 !important;
    background-color: rgba(255, 193, 7, 0.1) !important;
}
</style>