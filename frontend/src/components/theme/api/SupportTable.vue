<template>
    <div v-if="isAdmin" class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th class="px-4">UUID</th>
                    <th class="px-4">Name</th>
                    <th class="px-4">User</th>
                    <th class="px-4">Created At</th>
                    <th class="px-4">Last Used</th>
                    <th class="px-4">Expires At</th>
                    <th class="px-4">Status</th>
                    <th class="px-4">Actions</th>
                </tr>
            </thead>
            <tbody v-if="isLoading">
                <tr>
                    <td colspan="8" class="text-center py-4">Loading...</td>
                </tr>
            </tbody>
            <tbody v-else-if="!get_rows().length">
                <tr>
                    <td colspan="8" class="text-center py-4">No API keys found</td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr v-for="(row, index) in get_rows()" :key="row.id" class="api-key-row">
                    <td class="px-4 py-3">{{ formatUUID(row.uuid) }}</td>
                    <td class="px-4 py-3">{{ row.token_name }}</td>
                    <td class="px-4 py-3">{{ row.user_email || row.user || '-' }}</td>
                    <td class="px-4 py-3">{{ formatDate(row.created_at) }}</td>
                    <td class="px-4 py-3">{{ row.last_used ? formatDate(row.last_used) : 'No Recent Usage' }}</td>
                    <td class="px-4 py-3">{{ formatDate(row.expires_at) }}</td>
                    <td class="status-cell px-4 py-3">
                        <span 
                            :class="[
                                'status-badge',
                                `status-${getStatus(row).toLowerCase()}`
                            ]"
                        >
                            {{ getStatus(row) }}
                        </span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="action-buttons">
                            <button 
                                class="view-btn"
                                @click="navigateToUsageLogs(row.uuid)"
                                title="View usage logs"
                            >
                                <i class="fa fa-eye"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <!-- Simple Pagination -->
        <div class="mt-3 text-center" v-if="num_pages() > 1">
            <button class="btn btn-outline-primary me-2" @click="prev()" :disabled="currentPage === 1">Previous</button>
            <span class="mx-3">Page {{ currentPage }} of {{ num_pages() }}</span>
            <button class="btn btn-outline-primary ms-2" @click="change()" :disabled="currentPage === num_pages()">Next</button>
        </div>
    </div>
    <div v-else class="alert alert-warning mt-4">You do not have permission to view API key management.</div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from "vue"
import axios from '@/plugins/axios'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'

let elementsPerPage = ref<number>(10)
let currentPage = ref<number>(1)
let filterQuery = ref<string>("")
let allData = ref<any[]>([])
let isLoading = ref<boolean>(true)
const authStore = useAuthStore()
const { isAdmin } = authStore
const router = useRouter();

onMounted(async () => {
    console.log('SupportTable mounted, isAdmin:', isAdmin);
    if (isAdmin) {
        await fetchApiAccessKeys();
    } else {
        console.log('User is not admin, cannot fetch API keys');
    }
})

async function fetchApiAccessKeys() {
    isLoading.value = true;
    try {
        console.log('Fetching API access keys...');
        const response = await axios.get('/api/api-keys/');
        console.log('API response:', response.data);
        allData.value = response.data || [];
    } catch (error: any) {
        console.error('Error fetching API keys:', error);
        allData.value = [];
        // Show more specific error message
        if (error.response?.status === 403) {
            console.error('Access forbidden - user may not have permission');
        } else if (error.response?.status === 404) {
            console.error('API endpoint not found');
        } else {
            console.error('Network or server error:', error.message);
        }
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
    if (!dateString) return 'Not Available';
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

function formatUUID(uuid: string) {
    if (!uuid) return 'N/A';
    return uuid.substring(0, 8) + '...' + uuid.substring(uuid.length - 8);
}

function getStatus(row: any) {
    if (!row.expires_at) return 'Unknown';
    return new Date(row.expires_at) > new Date() ? 'Active' : 'Inactive';
}

const navigateToUsageLogs = (uuid: string) => {
    router.push({ name: 'apiKeyUsageLogs', params: { uuid } });
};


</script>

<style scoped>
.api-key-row {
    transition: background-color 0.2s ease;
}

.api-key-row:hover {
    background-color: #f8f9fa;
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-align: center;
    min-width: 80px;
}

.status-active {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-inactive {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status-unknown {
    background-color: #f8f9fa;
    color: #6c757d;
    border: 1px solid #dee2e6;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.view-btn {
    background-color: #17a2b8;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.view-btn:hover {
    background-color: #138496;
    transform: scale(1.1);
}



.view-btn i {
    font-size: 14px;
}

/* Dark Mode Styles */
:deep(.dark-mode) {
    .api-key-row {
        background-color: #1d1e26 !important;
        color: white !important;
    }
    
    .api-key-row:hover {
        background-color: #2a2b36 !important;
    }
    
    .table {
        background-color: #1d1e26 !important;
        color: white !important;
    }
    
    .table thead th {
        background-color: #2a2b36 !important;
        color: white !important;
        border-color: #3a3b46 !important;
    }
    
    .table tbody td {
        background-color: #1d1e26 !important;
        color: white !important;
        border-color: #3a3b46 !important;
    }
    
    .card {
        background-color: #1d1e26 !important;
        border-color: #3a3b46 !important;
    }
    
    .card-header {
        background-color: #1d1e26 !important;
        border-bottom-color: #3a3b36 !important;
    }
    
    .card-header h5,
    .card-header p {
        color: white !important;
    }
    
    .card-body {
        background-color: #1d1e26 !important;
        color: white !important;
    }
    
    .status-badge {
        &.status-active {
            background-color: #28a745 !important;
            color: white !important;
            border-color: #28a745 !important;
        }
        
        &.status-inactive {
            background-color: #dc3545 !important;
            color: white !important;
            border-color: #dc3545 !important;
        }
        
        &.status-unknown {
            background-color: #ffc107 !important;
            color: #212529 !important;
            border-color: #ffc107 !important;
        }
    }
    
    .btn-outline-primary {
        color: white !important;
        border-color: #007bff !important;
    }
    
    .btn-outline-primary:hover {
        background-color: #007bff !important;
        color: white !important;
    }
}

/* Additional dark mode overrides for better visibility */
body.dark-only {
    .api-accounts-overview {
        .card {
            background-color: #2a2b36 !important;
            border-color: #3a3b46 !important;
            
            .card-header {
                background-color: #2a2b36 !important;
                border-bottom-color: #3a3b46 !important;
                
                h5, p {
                    color: white !important;
                }
            }
            
            .card-body {
                background-color: #2a2b36 !important;
                color: white !important;
            }
        }
        
        .table {
            background-color: #2a2b36 !important;
            
            thead {
                background-color: #1d1e26 !important;
                
                th {
                    background-color: #1d1e26 !important;
                    color: white !important;
                    border-color: #3a3b46 !important;
                }
            }
            
            tbody {
                background-color: #2a2b36 !important;
                
                td {
                    background-color: #2a2b36 !important;
                    color: white !important;
                    border-color: #3a3b46 !important;
                }
                
                tr:hover {
                    background-color: #1d1e26 !important;
                    
                    td {
                        background-color: #1d1e26 !important;
                    }
                }
            }
        }
    }
}
</style>