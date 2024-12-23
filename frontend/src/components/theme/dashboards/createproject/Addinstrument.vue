<template>
    <div class="form theme-form h-100">
        <!-- Device Name and Code fields -->
        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>AWS Name</label>
                    <input class="form-control" type="text" :class="inputClasses.name" placeholder="Enter Device Name"
                        v-model="name" @input="validated('name')">
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <div class="mb-3">
                    <label>Device Code</label> <!-- Changed label to Device Code -->
                    <input class="form-control" v-model="deviceCode" @input="validated('deviceCode')" 
                        :class="inputClasses.deviceCode" type="text" placeholder="Enter Device Code">
                </div>
            </div>
        </div>

        <!-- Brand, Lat/Lng, and Device Location fields -->
        <div class="row">
            <div class="col-sm-4">
                <label>Brand</label>
                <select class="form-select" v-model="brandId" @change="validated('brandId')">
                    <option value="0" disabled>Select a Brand</option> <!-- Default value -->
                    <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                        {{ brand.name }}
                    </option>
                </select>
            </div>
            <div class="col-sm-4">
                <div class="mb-3">
                    <label>Lat/Lng</label>
                    <input class="form-control" type="text" v-model="latLng" placeholder="Enter Lat/Lng (optional)">
                </div>
            </div>
            <div class="col-sm-4">
                <label>Device Location</label>
                <input class="form-control" type="text" v-model="address" placeholder="Enter Device Location">
            </div>
        </div>

        <!-- Date fields -->
        <div class="row">
            <div class="col-sm-4">
                <div class="mb-3">
                    <label>Installation Date</label>
                    <datepicker class="datepicker-here form-control" v-model="installationDate" :format="format" />
                </div>
            </div>
        </div>

        <!-- Buttons to submit the form or cancel -->
        <div class="row">
            <div class="col">
                <div class="text-end">
                    <a class="btn btn-success me-3" @click="add">Add</a>
                    <a class="btn btn-danger" @click="cancel">Cancel</a>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

// Initialize router at the top level
const router = useRouter();

// Define form fields and their models with initial values
const name = ref<string>('');
const deviceCode = ref<string>('');
const address = ref<string>('');
const latLng = ref<string>('');
const brandId = ref<number>(0);
const installationDate = ref<Date | null>(null);
const brands = ref<Array<{ id: number, name: string }>>([]);

// Input validation
const inputClasses = ref({
    name: '',
    deviceCode: '', // Changed to deviceCode validation
    brandId: ''
});

// Date format function for submission
const format = (date: Date | null): string => {
    if (date === null) {
        return '';
    }

    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();

    return `${day}/${month}/${year}`;
};

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000';

// Fetch available brands
const fetchBrands = async () => {
    try {
        const response = await axios.get('/brands/');
        brands.value = response.data;
    } catch (error) {
        console.error('Error fetching brands:', error);
        alert('Error loading brands. Please try refreshing the page.');
    }
};

// Function to validate fields
function validated(field: string) {
    if (field === 'name' && name.value.length < 5) {
        inputClasses.value.name = 'is-invalid';
    } else {
        inputClasses.value.name = 'is-valid';
    }

    if (field === 'deviceCode' && deviceCode.value.length < 1) { 
        inputClasses.value.deviceCode = 'is-invalid';
    } else {
        inputClasses.value.deviceCode = 'is-valid';
    }

    if (field === 'brandId' && brandId.value === 0) { 
        inputClasses.value.brandId = 'is-invalid';
    } else {
        inputClasses.value.brandId = 'is-valid';
    }
}

// Function to format date in DD/MM/YYYY format
const formatDate = (date: Date | null): string => {
    if (!date) return '';
    
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${year}-${month}-${day}`;
};

// Add method to submit form data
async function add() {
    try {
        // Validate the inputs before submitting
        validated('name');
        validated('deviceCode');
        validated('brandId');
        
        if (inputClasses.value.name !== 'is-valid' || 
            inputClasses.value.deviceCode !== 'is-valid' || 
            inputClasses.value.brandId !== 'is-valid') {
            alert('Please fill in all required fields correctly.');
            return;
        }

        if (!installationDate.value) {
            alert('Please select an installation date.');
            return;
        }

        const formattedDate = formatDate(installationDate.value);
        console.log('Formatted date:', formattedDate); // Debug log

        // Prepare data to be sent to the API
        const payload = {
            name: name.value.trim(),
            serial_number: deviceCode.value.trim(),
            brand: brandId.value,
            lat_lng: latLng.value?.trim() || null,
            address: address.value?.trim() || '',
            installation_date: formattedDate,
            last_updated_at: new Date().toISOString()
        };
        console.log('Sending payload:', JSON.stringify(payload, null, 2));

        // Send POST request to the Django API
        const response = await axios.post('/stations/', payload);
        console.log('Success Response:', response.data);

        if (response.status === 201) {
            alert('Device added successfully!');
            router.push('/project/project_list');
        }
    } catch (error: any) {
        console.error('Full error:', error);
        
        let errorMessage = 'An error occurred while adding the device.';
        
        if (error?.response?.data) {
            console.error('Error response data:', error.response.data);
            
            if (error.response.data.error) {
                if (typeof error.response.data.error === 'object') {
                    errorMessage = Object.entries(error.response.data.error)
                        .map(([key, value]) => `${key}: ${value}`)
                        .join('\n');
                } else {
                    errorMessage = error.response.data.error;
                }
            } else if (typeof error.response.data === 'object') {
                errorMessage = Object.entries(error.response.data)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join('\n');
            }
        }
        
        alert('Error adding device:\n' + errorMessage);
    }
}

// Function to handle cancel action
function cancel() {
    // Use the router instance we initialized at the top
    router.push('/project/project_list');
}

// Fetch brands when component is mounted
onMounted(() => {
    fetchBrands();
});
</script>
