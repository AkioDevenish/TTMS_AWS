<template>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th class="px-4">Name</th>
                    <th class="px-4">Brand</th>
                    <th class="px-4">Serial Number</th>
                    <th class="px-4">Address</th>
                    <th class="px-4">Installation Date</th>
                    <th class="px-4">Decommissioned At</th>
                    <th class="px-4">Status</th>
                    <th class="px-4">Actions</th>
                </tr>
            </thead>
            <tbody v-if="loading">
                <tr>
                    <td colspan="8" class="text-center py-4">Loading...</td>
                </tr>
            </tbody>
            <tbody v-else-if="!stations || stations.length === 0">
                <tr>
                    <td colspan="8" class="text-center py-4">
                        {{ loading ? 'Loading stations...' : 'No stations found' }}
                    </td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr v-for="(station, index) in stations" :key="station?.id || station?.name || index" class="station-row">
                    <td class="px-4 py-3">{{ station?.name || '-' }}</td>
                    <td class="px-4 py-3">{{ station?.brand?.name || station?.brand_name || '-' }}</td>
                    <td class="px-4 py-3">{{ station?.serial_number || '-' }}</td>
                    <td class="px-4 py-3">{{ station?.address || '-' }}</td>
                    <td class="px-4">{{ station?.installation_date || 'Not Available' }}</td>
                    <td class="px-4 py-3">{{ formatDecommissionedDate(station?.decommissioned_at, station?.status) }}</td>
                    <td class="status-cell px-4 py-3">
                        <span 
                            :class="[
                                'status-badge',
                                `status-${(station?.status || 'Active').toLowerCase()}`
                            ]"
                        >
                            {{ station?.status || 'Active' }}
                        </span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="action-buttons">
                            <button 
                                class="decommission-btn"
                                v-if="station?.status !== 'Decommissioned'"
                                @click.stop="handleDecommissionStation(station?.id)"
                                title="Decommission station"
                                :disabled="!station?.id"
                            >
                                <i class="fa fa-trash-o"></i>
                            </button>
                            <button 
                                class="reactivate-btn"
                                v-if="station?.status === 'Decommissioned'"
                                @click.stop="handleReactivateStation(station?.id)"
                                title="Reactivate station"
                                :disabled="!station?.id"
                            >
                                <i class="fa fa-play"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { useStationStore } from '@/store/station'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const stationStore = useStationStore()
const stations = computed(() => stationStore.stations)
const loading = computed(() => stationStore.loading)

// Add debugging
console.log('StationTable - stations:', stations.value)
console.log('StationTable - loading:', loading.value)

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)
const router = useRouter()

onMounted(async () => {
    if (!currentUser.value?.is_superuser) {
        router.go(-1)
        return
    }
})

const handleDecommissionStation = async (stationId: number) => {
    try {
        const result = await Swal.fire({
            title: 'Decommission Station',
            text: 'Are you sure you want to decommission this station? The station will be marked as inactive but all data will be preserved.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, decommission',
            cancelButtonText: 'Cancel',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                try {
                    const success = await stationStore.decommissionStation(stationId)
                    if (!success) {
                        throw new Error('Failed to decommission station')
                    }
                    return success
                } catch (error) {
                    Swal.showValidationMessage(
                        `Decommission failed: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
                    )
                }
            },
            allowOutsideClick: () => !Swal.isLoading()
        })
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Decommissioned!',
                text: 'Station has been decommissioned successfully. All data is preserved.',
                icon: 'success',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
            // Don't refresh immediately - let the local state update handle it
            // The decommissionStation function already updates the local state
            
            // Notify other components that station status has changed
            window.dispatchEvent(new CustomEvent('stationStatusChanged'));
        }
    } catch (error) {
        console.error('Error in handleDecommissionStation:', error)
        Swal.fire({
            title: 'Error',
            text: 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

const handleReactivateStation = async (stationId: number) => {
    try {
        const result = await Swal.fire({
            title: 'Reactivate Station',
            text: 'Are you sure you want to reactivate this station?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, reactivate',
            cancelButtonText: 'Cancel',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                try {
                    const success = await stationStore.reactivateStation(stationId)
                    if (!success) {
                        throw new Error('Failed to reactivate station')
                    }
                    return success
                } catch (error) {
                    Swal.showValidationMessage(
                        `Reactivation failed: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
                    )
                }
            },
            allowOutsideClick: () => !Swal.isLoading()
        })
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Reactivated!',
                text: 'Station has been reactivated successfully.',
                icon: 'success',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            })
            // Don't refresh immediately - let the local state update handle it
            // The reactivateStation function already updates the local state
            
            // Notify other components that station status has changed
            window.dispatchEvent(new CustomEvent('stationStatusChanged'));
        }
    } catch (error) {
        console.error('Error in handleReactivateStation:', error)
        Swal.fire({
            title: 'Error',
            text: 'An unexpected error occurred',
            icon: 'error',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
        })
    }
}

const formatDate = (dateString: string | null): string => {
    if (!dateString) return '-'
    try {
        const date = new Date(dateString)
        return date.toLocaleDateString()
    } catch {
        return '-'
    }
}

const formatDecommissionedDate = (dateString: string | null, status: string): string => {
    if (status === 'Decommissioned') {
        if (!dateString) return 'Unknown'
        try {
            const date = new Date(dateString)
            return date.toLocaleDateString()
        } catch {
            return 'Invalid date'
        }
    } else {
        return 'N/A'
    }
}
</script>

<style scoped>
.station-row {
    transition: background-color 0.2s ease;
}

.station-row:hover {
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

.status-offline {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status-maintenance {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.status-decommissioned {
    background-color: #f8f9fa;
    color: #6c757d;
    border: 1px solid #dee2e6;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.decommission-btn {
    background-color: #dc3545;
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

.decommission-btn:hover {
    background-color: #c82333;
    transform: scale(1.1);
}

.reactivate-btn {
    background-color: #28a745;
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

.reactivate-btn:hover {
    background-color: #218838;
    transform: scale(1.1);
}

.decommission-btn i,
.reactivate-btn i {
    font-size: 14px;
}
</style> 