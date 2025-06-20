<template>
	<div class="form theme-form h-100">
		<!-- Device Name and Code fields -->
		<div class="row">
			<div class="col">
				<div class="mb-3">
					<label>AWS Name <span class="txt-danger">*</span></label>
					<input class="form-control" type="text" :class="inputClasses.name" placeholder="Enter AWS device name (min. 5 characters)" v-model="name" @input="validated('name')">
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col">
				<div class="mb-3">
					<label>Device Code <span class="txt-danger">*</span></label>
					<input class="form-control" v-model="deviceCode" @input="validated('deviceCode')" :class="inputClasses.deviceCode" type="text" placeholder="Enter unique device identification code">
				</div>
			</div>
		</div>

		<!-- Brand, Lat/Lng, and Device Location fields -->
		<div class="row">
			<div class="col-sm-4">
				<label>Brand <span class="txt-danger">*</span></label>
				<select class="form-select" v-model="brandId" @change="validated('brandId')" :class="inputClasses.brandId">
					<option value="0" disabled>Select device brand</option>
					<option v-for="brand in brands" :key="brand.id" :value="brand.id">
						{{ brand.name }}
					</option>
				</select>
			</div>
			<div class="col-sm-4">
				<div class="mb-3">
					<label>Latitude <span class="txt-danger">*</span></label>
					<input 
						class="form-control" 
						type="number" 
						step="0.000001"
						v-model="latitude" 
						:class="inputClasses.latitude"
						@input="validated('latitude')"
						placeholder="e.g., 12.3456">
				</div>
			</div>
			<div class="col-sm-4">
				<div class="mb-3">
					<label>Longitude <span class="txt-danger">*</span></label>
					<input 
						class="form-control" 
						type="number"
						step="0.000001"
						v-model="longitude" 
						:class="inputClasses.longitude"
						@input="validated('longitude')"
						placeholder="e.g., -78.9012">
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col">
				<label>Device Location <span class="txt-danger">*</span></label>
				<input 
					class="form-control" 
					type="text" 
					v-model="address" 
					:class="inputClasses.address"
					@input="validated('address')"
					placeholder="Enter physical location">
			</div>
		</div>

		<!-- Date fields -->
		<div class="row">
			<div class="col-sm-4">
				<div class="mb-3">
					<label>Installation Date <span class="txt-danger">*</span></label>
					<datepicker class="datepicker-here form-control" v-model="installationDate" :format="format" placeholder="Select installation date" />
				</div>
			</div>
		</div>

		<!-- Status Message and Buttons -->
		<div class="row">
			<div class="col">
				<div class="text-end">
					<div v-if="statusMessage" :class="['status-message', statusType]">
						{{ statusMessage }}
					</div>
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
const latitude = ref<number | null>(null);
const longitude = ref<number | null>(null);
const brandId = ref<number>(0);
const installationDate = ref<Date | null>(null);
const brands = ref<Array<{ id: number, name: string }>>([]);
const statusMessage = ref<string>('');
const statusType = ref<string>('');

// Input validation
const inputClasses = ref({
	name: '',
	deviceCode: '',
	brandId: '',
	latitude: '',
	longitude: '',
	address: ''
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
		const response = await axios.get('/brands/');
		brands.value = response.data;
	} catch (error) {
		console.error('Error fetching brands:', error);
		alert('Error loading brands. Please try refreshing the page.');
	}
};

// Function to validate fields
function validated(field: string) {
	// Only validate the field that was changed
	if (field === 'name') {
		if (name.value.length < 5) {
			inputClasses.value.name = 'is-invalid';
		} else {
			inputClasses.value.name = 'is-valid';
		}
	}

	if (field === 'deviceCode') {
		if (deviceCode.value.length < 1) {
			inputClasses.value.deviceCode = 'is-invalid';
		} else {
			inputClasses.value.deviceCode = 'is-valid';
		}
	}

	if (field === 'brandId') {
		if (brandId.value === 0) {
			inputClasses.value.brandId = 'is-invalid';
		} else {
			inputClasses.value.brandId = 'is-valid';
		}
	}

	if (field === 'latitude') {
		if (latitude.value !== null && (latitude.value < -90 || latitude.value > 90)) {
			inputClasses.value.latitude = 'is-invalid';
		} else {
			inputClasses.value.latitude = 'is-valid';
		}
	}

	if (field === 'longitude') {
		if (longitude.value !== null && (longitude.value < -180 || longitude.value > 180)) {
			inputClasses.value.longitude = 'is-invalid';
		} else {
			inputClasses.value.longitude = 'is-valid';
		}
	}

	if (field === 'address') {
		if (!address.value || address.value.length < 3) {
			inputClasses.value.address = 'is-invalid';
		} else {
			inputClasses.value.address = 'is-valid';
		}
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

// Add this function before the add() function
const getBrandRoute = (brandId: number): string => {
	// Map brand IDs to their respective routes
	const brandRoutes: { [key: number]: string } = {
		1: '/stations/AWS_Barani',
		2: '/stations/AWS_3D_Paws',
		3: '/stations/AWS_OTT_Hyrdomet',
		4: '/stations/AWS_Zentra'
	};

	return brandRoutes[brandId] || '/stations';
};

// Add method to submit form data
async function add() {
	try {
		// Validate all required inputs
		validated('name');
		validated('deviceCode');
		validated('brandId');
		validated('latitude');
		validated('longitude');
		validated('address');

		if (inputClasses.value.name !== 'is-valid' ||
			inputClasses.value.deviceCode !== 'is-valid' ||
			inputClasses.value.brandId !== 'is-valid' ||
			inputClasses.value.latitude !== 'is-valid' ||
			inputClasses.value.longitude !== 'is-valid' ||
			inputClasses.value.address !== 'is-valid') {
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
			latitude: latitude.value,
			longitude: longitude.value,
			address: address.value?.trim() || '',
			installation_date: formattedDate,
			last_updated_at: new Date().toISOString()
		};
		console.log('Sending payload:', JSON.stringify(payload, null, 2));

		// Send POST request to the Django API
		const response = await axios.post('/stations/', payload);
		console.log('Success Response:', response.data);

		if (response.status === 201) {
			statusMessage.value = 'Device added successfully!';
			statusType.value = 'success';
			setTimeout(() => {
				const brandRoute = getBrandRoute(brandId.value);
				router.push(brandRoute);
			}, 2000);
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

		statusMessage.value = 'Error adding device: ' + errorMessage;
		statusType.value = 'error';
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

<style scoped>
.status-message {
	margin-bottom: 1rem;
	padding: 0.5rem 1rem;
	border-radius: 4px;
	font-weight: 500;
}

.success {
	color: #155724;
	background-color: #d4edda;
	border: 1px solid #c3e6cb;
}

.error {
	color: #721c24;
	background-color: #f8d7da;
	border: 1px solid #f5c6cb;
}
</style>