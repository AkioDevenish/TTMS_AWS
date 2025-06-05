<template>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th class="px-4">Timestamp</th>
                    <th class="px-4">Request Path</th>
                    <th class="px-4">Method</th>
                    <th class="px-4">Status Code</th>
                    <th class="px-4">User</th>
                    <th class="px-4">API Key UUID</th>
                    <th class="px-4">Query Params</th>
                    <th class="px-4">Response Format</th>
                    <!-- Add more columns as needed -->
                </tr>
            </thead>
            <tbody v-if="loading">
                <tr>
                    <td colspan="8" class="text-center py-4">Loading...</td>
                </tr>
            </tbody>
            <tbody>
                <tr v-for="log in usageLogs" :key="log.id">
                    <td class="px-4">{{ formatDateTime(log.created_at) }}</td>
                    <td class="px-4">{{ log.request_path }}</td>
                    <td class="px-4">{{ log.request_method }}</td>
                    <td class="px-4">{{ log.status_code }}</td>
                    <td class="px-4">{{ log.user?.email || '-' }}</td>
                    <td class="px-4">{{ log.api_key?.uuid || '-' }}</td>
                    <td class="px-4">{{ formatQueryParams(log.query_params) }}</td>
                    <td class="px-4">{{ log.response_format || '-' }}</td>
                    <!-- Display more log data -->
                </tr>
            </tbody>
        </table>
        <!-- Add pagination controls here later if needed -->
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch, onMounted, defineProps } from 'vue';
import axios from 'axios';

const props = defineProps({
    apiKeyUuid: {
        type: [String, Array],
        required: true
    }
});

const usageLogs = ref<any[]>([]); // Define a proper type for usage logs later
const loading = ref(false);
const error = ref<string | null>(null);

const fetchUsageLogs = async (uuid: string) => {
    loading.value = true;
    error.value = null;
    try {
        const response = await axios.get(`/api-key-usage-logs/`, {
            params: {
                api_key: uuid // Filter by API key UUID
            }
        });
        if (response.data && Array.isArray(response.data.results)) { // Assuming pagination returns results in .results
            usageLogs.value = response.data.results;
        } else if (response.data && Array.isArray(response.data)) { // Handle non-paginated response just in case
             usageLogs.value = response.data;
        }
    } catch (err: any) {
        error.value = err.message;
        usageLogs.value = [];
        console.error('Error fetching API key usage logs:', err);
    } finally {
        loading.value = false;
    }
};

// Watch for apiKeyUuid changes to fetch logs
watch(() => props.apiKeyUuid, (newUuid) => {
    if (newUuid && typeof newUuid === 'string') {
        fetchUsageLogs(newUuid);
    } else {
        usageLogs.value = []; // Clear logs if no valid UUID
    }
}, { immediate: true }); // Fetch logs initially

// Helper function to format timestamp
const formatDateTime = (timestamp: string) => {
    if (!timestamp) return '-';
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) return '-';
    return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
};

// Helper function to format query parameters (simple JSON stringify for now)
const formatQueryParams = (params: any) => {
    if (!params) return '-';
    return JSON.stringify(params, null, 2);
};

</script>

<style scoped>
/* Add your table specific styles here */
</style> 