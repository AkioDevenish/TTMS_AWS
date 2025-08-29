<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <Card3 colClass="col-sm-12" title="Create New Station" headerTitle="true" cardhaderClass="title-header" text="true" :desc="desc" :btnclass="'btn-primary'">
                    <div class="row">
                        <div class="col-md-8 mx-auto">
                            <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="name" class="form-label">Station Name *</label>
                                        <input 
                                            type="text" 
                                            class="form-control" 
                                            id="name" 
                                            v-model="formData.name" 
                                            required
                                            placeholder="Enter station name"
                                        >
                                        <div class="invalid-feedback">
                                            Please provide a station name.
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="brand" class="form-label">Brand *</label>
                                        <select 
                                            class="form-select" 
                                            id="brand" 
                                            v-model="formData.brand" 
                                            required
                                        >
                                            <option value="">Select brand</option>
                                            <option value="OTT-Hydromet">OTT-Hydromet</option>
                                            <option value="Barani">Barani</option>
                                            <option value="Zentra">Zentra</option>
                                            <option value="3D-Paws">3D-Paws</option>
                                        </select>
                                        <div class="invalid-feedback">
                                            Please select a brand.
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="serial_number" class="form-label">Serial Number *</label>
                                        <input 
                                            type="text" 
                                            class="form-control" 
                                            id="serial_number" 
                                            v-model="formData.serial_number" 
                                            required
                                            placeholder="Enter serial number"
                                        >
                                        <div class="invalid-feedback">
                                            Please provide a serial number.
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="installation_date" class="form-label">Installation Date *</label>
                                        <input 
                                            type="date" 
                                            class="form-control" 
                                            id="installation_date" 
                                            v-model="formData.installation_date" 
                                            required
                                        >
                                        <div class="invalid-feedback">
                                            Please provide an installation date.
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="latitude" class="form-label">Latitude</label>
                                        <input 
                                            type="number" 
                                            class="form-control" 
                                            id="latitude" 
                                            v-model="formData.latitude" 
                                            step="0.000001"
                                            placeholder="Enter latitude"
                                        >
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="longitude" class="form-label">Longitude</label>
                                        <input 
                                            type="number" 
                                            class="form-control" 
                                            id="longitude" 
                                            v-model="formData.longitude" 
                                            step="0.000001"
                                            placeholder="Enter longitude"
                                        >
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="address" class="form-label">Address *</label>
                                    <textarea 
                                        class="form-control" 
                                        id="address" 
                                        v-model="formData.address" 
                                        rows="3" 
                                        required
                                        placeholder="Enter station address"
                                    ></textarea>
                                    <div class="invalid-feedback">
                                        Please provide an address.
                                    </div>
                                </div>
                                
                                <div class="d-flex justify-content-between">
                                    <router-link to="/pages/station_management" class="btn btn-secondary">
                                        <i class="fa fa-arrow-left"></i> Back to Stations
                                    </router-link>
                                    <button type="submit" class="btn btn-primary" :disabled="loading">
                                        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                                        <i v-else class="fa fa-save me-2"></i>
                                        {{ loading ? 'Creating...' : 'Create Station' }}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </Card3>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useStationStore } from '@/store/station';
import { useAuthStore } from '@/store/auth';
import Swal from 'sweetalert2';

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))

const router = useRouter();
const stationStore = useStationStore();
const authStore = useAuthStore();

const loading = ref(false);
const desc = ref("Add a new weather station to the system");

const formData = ref({
    name: '',
    brand: '',
    serial_number: '',
    address: '',
    latitude: null as number | null,
    longitude: null as number | null,
    installation_date: ''
});

onMounted(() => {
    if (!authStore.isAdmin) {
        router.push('/dashboard');
        return;
    }
});

const handleSubmit = async () => {
    try {
        loading.value = true;
        
        // Validate form
        const form = document.querySelector('.needs-validation') as HTMLFormElement;
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }
        
        // Prepare data for API
        const stationData = {
            ...formData.value,
            last_updated_at: new Date().toISOString(),
            brand_name: formData.value.brand, // Map brand to brand_name for API
            status: 'Active' // Assuming new stations are always active
        };
        
        const result = await stationStore.createStation(stationData);
        
        if (result) {
            Swal.fire({
                title: 'Success!',
                text: 'Station created successfully.',
                icon: 'success',
                confirmButtonText: 'OK'
            }).then(() => {
                router.push('/pages/station_management');
            });
        } else {
            throw new Error('Failed to create station');
        }
    } catch (error) {
        console.error('Error creating station:', error);
        Swal.fire({
            title: 'Error!',
            text: error instanceof Error ? error.message : 'Failed to create station',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.form-control:focus,
.form-select:focus {
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn:disabled {
    cursor: not-allowed;
}
</style> 