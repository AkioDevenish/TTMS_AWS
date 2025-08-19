<template>
    <Card1 colClass="col-xl-6 col-lg-6 col-md-6 order-5" 
        headerTitle="true"
        title="Task Execution Status" 
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="active-members px-0 pb-0">
        <div class="table-responsive theme-scrollbar">
            <table class="table table-sm display mb-0" style="width:100%">
                <thead>
                    <tr>
                        <th class="py-2">Task</th>
                        <th class="py-2">Last Run</th>
                        <th class="text-center py-2">Status</th>
                    </tr>
                </thead>
                <tbody v-if="loading">
                    <tr>
                        <td colspan="3" class="text-center">Loading tasks...</td>
                    </tr>
                </tbody>
                <tbody v-else-if="tasks.length">
                    <tr v-for="(task, index) in tasks" :key="index" class="task-row">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="task-icon me-3">
                                    <i class="icon" :class="getTaskIcon(task.name)"></i>
                                </div>
                                <div class="flex-grow-1">
                                    <h6 class="mb-0 task-name">{{ task.name }}</h6>
                                    <span class="text-muted task-description">{{ task.description || 'No description' }}</span>
                                </div>
                            </div>
                        </td>
                        <td>
                            <span class="last-run-time">{{ formatDateTime(task.last_run) }}</span>
                        </td>
                        <td class="text-center">
                            <span class="status-badge" :class="getStatusClass(task.status)">
                                {{ task.status }}
                            </span>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="3" class="text-center">No tasks found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, onUnmounted, ref } from 'vue'
import axios from '@/plugins/axios'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const tasks = ref<any[]>([])
const loading = ref(false)

let refreshInterval: number;

const fetchTasks = async () => {
    try {
        loading.value = true
        const response = await axios.get('/api/task-execution-status/')
        tasks.value = response.data || []
    } catch (error) {
        console.error('Error fetching tasks:', error)
        tasks.value = []
    } finally {
        loading.value = false
    }
}

const formatDateTime = (dateString: string) => {
    if (!dateString) return 'No Updates Scheduled'
    try {
        const date = new Date(dateString)
        return date.toLocaleString()
    } catch {
        return 'Invalid date'
    }
}

const getTaskIcon = (taskName: string) => {
    const iconMap: { [key: string]: string } = {
        'check_station_health': 'icon-health',
        'data_fetcher': 'icon-data',
        'default': 'icon-task'
    }
    return iconMap[taskName] || iconMap['default']
}

const getStatusClass = (status: string) => {
    const statusMap: { [key: string]: string } = {
        'Success': 'status-success',
        'Running': 'status-running',
        'Failed': 'status-failed',
        'Not Started': 'status-not-started',
        'default': 'status-default'
    }
    return statusMap[status] || statusMap['default']
}

onMounted(async () => {
    await fetchTasks()
    refreshInterval = window.setInterval(fetchTasks, 300000) // Refresh every 5 minutes
})

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval)
    }
})
</script>

<style scoped>
.task-row {
    transition: background-color 0.2s ease;
}

.task-row:hover {
    background-color: #f8f9fa;
}

.task-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 18px;
}

.task-icon .icon {
    width: 20px;
    height: 20px;
    display: inline-block;
}

.icon-health {
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>') no-repeat center;
    background-size: contain;
}

.icon-data {
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>') no-repeat center;
    background-size: contain;
}

.icon-task {
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>') no-repeat center;
    background-size: contain;
}

.task-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #333;
}

.task-description {
    font-size: 0.8rem;
    color: #6c757d;
}

.last-run-time {
    font-size: 0.85rem;
    color: #495057;
}

.status-badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-align: center;
    min-width: 100px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    margin: 0 auto;
}

/* Ensure the status column content is centered */
td.text-center {
    text-align: center !important;
}

/* Ensure the status column header is also centered */
th.text-center {
    text-align: center !important;
}

.status-success {
    background-color: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

.status-running {
    background-color: #cce7ff;
    color: #004085;
    border-color: #b3d9ff;
}

.status-failed {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.status-not-started {
    background-color: #f8f9fa;
    color: #6c757d;
    border-color: #dee2e6;
}

.status-default {
    background-color: #e2e3e5;
    color: #383d41;
    border-color: #d6d8db;
}

/* Dark mode styles for better visibility */
body.dark-only .status-badge {
    &.status-not-started {
        background-color: #6c757d !important;
        color: white !important;
        border-color: #6c757d !important;
    }
    
    &.status-running {
        background-color: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
    }
    
    &.status-success {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    
    &.status-failed {
        background-color: #dc3545 !important;
        color: white !important;
        border-color: #dc3545 !important;
    }
    
    &.status-default {
        background-color: #6c757d !important;
        color: white !important;
        border-color: #6c757d !important;
    }
}

/* Additional dark mode overrides */
:deep(.dark-mode) .status-badge {
    &.status-not-started {
        background-color: #6c757d !important;
        color: white !important;
        border-color: #6c757d !important;
    }
    
    &.status-running {
        background-color: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
    }
    
    &.status-success {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    
    &.status-failed {
        background-color: #dc3545 !important;
        color: white !important;
        border-color: #dc3545 !important;
    }
    
    &.status-default {
        background-color: #6c757d !important;
        color: white !important;
        border-color: #6c757d !important;
    }
}

/* Dark mode table styles */
body.dark-only .table {
    background-color: #2a2b36 !important;
    color: white !important;
}

body.dark-only .table thead th {
    background-color: #1d1e26 !important;
    color: white !important;
    border-color: #3a3b46 !important;
}

body.dark-only .table tbody td {
    background-color: #2a2b36 !important;
    color: white !important;
    border-color: #3a3b46 !important;
}

body.dark-only .table tbody tr:hover {
    background-color: #1d1e26 !important;
}

body.dark-only .table tbody tr:hover td {
    background-color: #1d1e26 !important;
}

/* Dark mode text colors */
body.dark-only .task-name {
    color: white !important;
}

body.dark-only .task-description {
    color: rgba(255, 255, 255, 0.7) !important;
}

body.dark-only .last-run-time {
    color: rgba(255, 255, 255, 0.8) !important;
}

/* Dark mode card styles */
body.dark-only .card {
    background-color: #2a2b36 !important;
    border-color: #3a3b46 !important;
}

body.dark-only .card-header {
    background-color: #2a2b36 !important;
    border-bottom-color: #3a3b46 !important;
}

body.dark-only .card-body {
    background-color: #2a2b36 !important;
    color: white !important;
}
</style> 