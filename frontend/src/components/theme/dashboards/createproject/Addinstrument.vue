<template>
    <div class="form theme-form h-100">
        <!-- Device Name and Device ID fields -->
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
                    <label>Device ID</label>
                    <input class="form-control" v-model="deviceId" @input="validated('deviceId')"
                        :class="inputClasses.deviceId" type="text" placeholder="Enter Device ID">
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

// Define form fields and their models with initial values
const name = ref<string>('');
const deviceId = ref<string>('');
const address = ref<string>('');
const latLng = ref<string>(''); // Optional field, initialized to empty string
const brandId = ref<number>(0);  // Initialize brandId with a default invalid value (0)
const installationDate = ref<Date | null>(null);
const brands = ref<Array<{ id: number, name: string }>>([]);

// Input validation
const inputClasses = ref({
    name: '',
    deviceId: '',
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

// Fetch available brands
const fetchBrands = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/brands/');
        brands.value = response.data;
    } catch (error) {
        console.error('Error fetching brands:', error);
    }
};

// Function to validate fields
function validated(field: string) {
    if (field === 'name' && name.value.length < 5) {
        inputClasses.value.name = 'is-invalid';
    } else {
        inputClasses.value.name = 'is-valid';
    }

    if (field === 'deviceId' && deviceId.value.length < 1) {
        inputClasses.value.deviceId = 'is-invalid';
    } else {
        inputClasses.value.deviceId = 'is-valid';
    }

    if (field === 'brandId' && brandId.value === 0) {  // Check if brand is not selected
        inputClasses.value.brandId = 'is-invalid';
    } else {
        inputClasses.value.brandId = 'is-valid';
    }
}

// Add method to submit form data
async function add() {
    // Validate the inputs before submitting
    validated('name');
    validated('deviceId');
    validated('brandId');
    
    if (inputClasses.value.name !== 'is-valid' || inputClasses.value.deviceId !== 'is-valid' || inputClasses.value.brandId !== 'is-valid') {
        console.error('Invalid form inputs');
        return; // Prevent form submission if validation fails
    }

    const formattedDate = format(installationDate.value);

    // Prepare data to be sent to the API
    const payload = {
        name: name.value || '',  // Ensure it's not null
        code: deviceId.value || '',  // Ensure it's not null
        brand: brandId.value || '',  
        lat_lng: latLng.value || '',  // Lat/Lng (optional)
        last_updated_at: new Date().toISOString(), // Automatically set current timestamp
        address: address.value || '', // Ensure it's not null
        installation_date: formattedDate || '', // Handle empty date
    };

    try {
        // Send POST request to the Django API to add the device data
        const response = await axios.post('http://127.0.0.1:8000/instruments/', payload, {
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        if (response.status === 201) {
            console.log('Device added successfully');
            // Redirect after adding the device
            const router = useRouter();
            router.push('/project/project_list'); // Redirect to project list page
        }
    } catch (error) {
        console.error('Error adding device:', error);
    }
}

// Function to handle cancel action
function cancel() {
    // Optionally, you can redirect the user to another page or reset form values
    const router = useRouter();
    router.push('/project/project_list');  // Navigate back to the project list
}

// Fetch brands when component is mounted
onMounted(() => {
    fetchBrands();
});
</script>
