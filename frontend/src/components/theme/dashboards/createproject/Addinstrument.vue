<template>
	<div class="create-aws-container">
		<!-- Header Section -->
		<div class="form-header">
			<div class="header-content">
				<div class="header-icon">
					<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</div>
				<div class="header-text">
					<h2>Create New AWS Station</h2>
					<p>Add a new weather monitoring station to the system</p>
				</div>
			</div>
		</div>

		<!-- Main Form -->
		<form @submit.prevent="add" class="aws-form">
			<!-- Station Information Section -->
			<div class="form-section">
				<div class="section-header">
					<div class="section-icon">
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<h5>Station Information</h5>
				</div>
				
				<div class="row">
					<div class="col-sm-6">
						<div class="form-group">
							<label for="name" class="form-label">
								Station Name <span class="required">*</span>
							</label>
							<input 
								id="name"
								type="text" 
								class="form-control" 
								:class="inputClasses.name"
								v-model="name" 
								@input="validated('name')"
								placeholder="Enter station name (min. 5 characters)"
								required
								autocomplete="name"
							>
							<div class="invalid-feedback" v-if="inputClasses.name === 'is-invalid'">
								Station name must be at least 5 characters long
							</div>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group">
							<label for="deviceCode" class="form-label">
								Device Code <span class="required">*</span>
							</label>
							<input 
								id="deviceCode"
								type="text" 
								class="form-control" 
								:class="inputClasses.deviceCode"
								v-model="deviceCode" 
								@input="validated('deviceCode')"
								placeholder="Enter unique device code"
								required
								autocomplete="username"
							>
							<div class="invalid-feedback" v-if="inputClasses.deviceCode === 'is-invalid'">
								Device code is required
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Brand & Location Section -->
			<div class="form-section">
				<div class="section-header">
					<div class="section-icon">
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.3639 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<h5>Brand & Location</h5>
				</div>
				
				<div class="row">
					<div class="col-sm-6">
						<div class="form-group">
							<label for="brand" class="form-label">
								Brand <span class="required">*</span>
							</label>
							<select 
								id="brand"
								class="form-select" 
								:class="inputClasses.brandId"
								v-model="brandId" 
								@change="validated('brandId')"
								required
								autocomplete="organization"
							>
								<option value="0" disabled>Select device brand</option>
								<option v-for="brand in brands" :key="brand.id" :value="brand.id">
									{{ brand.name }}
								</option>
							</select>
							<div class="invalid-feedback" v-if="inputClasses.brandId === 'is-invalid'">
								Please select a brand
							</div>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group">
							<label for="address" class="form-label">
								Device Location <span class="required">*</span>
							</label>
							<input 
								id="address"
								type="text" 
								class="form-control" 
								:class="inputClasses.address"
								v-model="address" 
								@input="validated('address')"
								placeholder="Enter physical location address"
								required
								autocomplete="street-address"
							>
							<div class="invalid-feedback" v-if="inputClasses.address === 'is-invalid'">
								Address must be at least 3 characters long
							</div>
						</div>
					</div>
				</div>

				<div class="row">
					<div class="col-sm-6">
						<div class="form-group">
							<label for="latitude" class="form-label">
								Latitude <span class="required">*</span>
							</label>
							<input 
								id="latitude"
								type="number" 
								step="0.000001"
								class="form-control" 
								:class="inputClasses.latitude"
								v-model="latitude" 
								@input="validated('latitude')"
								placeholder="e.g., 12.3456"
								required
								autocomplete="latitude"
							>
							<div class="invalid-feedback" v-if="inputClasses.latitude === 'is-invalid'">
								Latitude must be between -90 and 90
							</div>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group">
							<label for="longitude" class="form-label">
								Longitude <span class="required">*</span>
							</label>
							<input 
								id="longitude"
								type="number"
								step="0.000001"
								class="form-control" 
								:class="inputClasses.longitude"
								v-model="longitude" 
								@input="validated('longitude')"
								placeholder="e.g., -78.9012"
								required
								autocomplete="longitude"
							>
							<div class="invalid-feedback" v-if="inputClasses.longitude === 'is-invalid'">
								Longitude must be between -180 and 180
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Installation Details Section -->
			<div class="form-section">
				<div class="section-header">
					<div class="section-icon">
						<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<h5>Installation Details</h5>
				</div>
				
				<div class="row">
					<div class="col">
						<div class="form-group">
							<label for="installationDate" class="form-label">
								Installation Date <span class="required">*</span>
							</label>
							<datepicker 
								id="installationDate"
								class="form-datepicker" 
								v-model="installationDate" 
								:format="format" 
								placeholder="Select installation date"
								required
								autocomplete="date"
							></datepicker>
							<div class="invalid-feedback" v-if="!installationDate">
								Please select an installation date
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Form Actions -->
			<div class="form-actions">
				<div v-if="statusMessage" :class="['alert', statusType === 'success' ? 'alert-success' : 'alert-danger']">
					<svg v-if="statusType === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="me-2">
						<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
					<svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="me-2">
						<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<line x1="12" y1="17" x2="12.01" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
					{{ statusMessage }}
				</div>
				
				<div class="action-buttons">
					<button type="submit" class="btn btn-primary" :disabled="loading">
						<svg v-if="loading" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="me-2 spinner">
							<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-dasharray="31.416" stroke-dashoffset="31.416">
								<animate attributeName="stroke-dasharray" dur="2s" values="0 31.416;15.708 15.708;0 31.416" repeatCount="indefinite"/>
								<animate attributeName="stroke-dashoffset" dur="2s" values="0;-15.708;-31.416" repeatCount="indefinite"/>
							</circle>
						</svg>
						<svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="me-2">
							<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
						{{ loading ? 'Creating...' : 'Create Station' }}
					</button>
				</div>
			</div>
		</form>
	</div>
</template>


<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from '@/plugins/axios'
import { useRouter } from 'vue-router'
import Datepicker from '@vuepic/vue-datepicker'

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
const loading = ref<boolean>(false);

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

// Initialize brands with hardcoded values for consistency
const fetchBrands = async () => {
	try {
		// Use hardcoded brands for consistency with createstation.vue
		brands.value = [
			{ id: 1, name: 'Allmeteo' },
			{ id: 2, name: '3D_Paws' },
			{ id: 3, name: 'OTT' },
			{ id: 4, name: 'Zentra' },
			{ id: 5, name: 'Sutron' }
		];
	} catch (error) {
		console.error('Error initializing brands:', error);
		// Fallback to basic brands if there's an error
		brands.value = [
			{ id: 1, name: 'Allmeteo' },
			{ id: 2, name: '3D_Paws' },
			{ id: 3, name: 'OTT' },
			{ id: 4, name: 'Zentra' }
		];
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
		1: '/stations/AWS_Allmeteo',
		2: '/stations/AWS_3D_Paws',
		3: '/stations/AWS_OTT_Hyrdomet',
		4: '/stations/AWS_Zentra',
		5: '/stations/AWS_Sutron'
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
		const response = await axios.post('/api/stations/', payload);
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



// Fetch brands when component is mounted
onMounted(() => {
	fetchBrands();
});
</script>

<style scoped>
/* Main Container */
.create-aws-container {
	max-width: 800px;
	margin: 0 auto;
	padding: 0;
}

/* Header Section */
.form-header {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	padding: 2rem;
	border-radius: 12px 12px 0 0;
	margin-bottom: 0;
	box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.header-content {
	display: flex;
	align-items: center;
	gap: 1rem;
}

.header-icon {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 50%;
	padding: 1rem;
	display: flex;
	align-items: center;
	justify-content: center;
	backdrop-filter: blur(10px);
}

.header-icon svg {
	color: white;
}

.header-text h2 {
	margin: 0;
	font-size: 1.75rem;
	font-weight: 600;
	color: white;
}

.header-text p {
	margin: 0.5rem 0 0 0;
	opacity: 0.9;
	font-size: 1rem;
}

/* Main Form */
.aws-form {
	background: white;
	border-radius: 0 0 12px 12px;
	padding: 2rem;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
	border: 1px solid #e9ecef;
}

/* Form Sections */
.form-section {
	margin-bottom: 2.5rem;
	padding: 1.5rem;
	background: #f8f9fa;
	border-radius: 8px;
	border: 1px solid #e9ecef;
	transition: all 0.3s ease;
}

.form-section:hover {
	background: white;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
	transform: translateY(-2px);
}

.section-header {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	margin-bottom: 1.5rem;
	padding-bottom: 1rem;
	border-bottom: 2px solid #e9ecef;
}

.section-icon {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-radius: 50%;
	padding: 0.5rem;
	display: flex;
	align-items: center;
	justify-content: center;
}

.section-icon svg {
	color: white;
	width: 16px;
	height: 16px;
}

.section-header h5 {
	margin: 0;
	font-size: 1.1rem;
	font-weight: 600;
	color: #495057;
}

/* Form Groups */
.form-group {
	margin-bottom: 1.5rem;
}

.form-label {
	display: block;
	margin-bottom: 0.5rem;
	font-weight: 600;
	color: #495057;
	font-size: 0.9rem;
	text-transform: uppercase;
	letter-spacing: 0.5px;
}

.required {
	color: #dc3545;
	font-weight: 700;
}

.form-control,
.form-select,
.form-datepicker {
	border: 2px solid #e9ecef;
	border-radius: 8px;
	padding: 0.75rem 1rem;
	font-size: 0.95rem;
	transition: all 0.3s ease;
	background: white;
	width: 100%;
}

.form-control:focus,
.form-select:focus,
.form-datepicker:focus {
	border-color: #667eea;
	box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
	outline: none;
}

.form-control::placeholder {
	color: #adb5bd;
	font-style: italic;
}

/* Validation States */
.form-control.is-valid,
.form-select.is-valid {
	border-color: #28a745;
	background-color: #f8fff9;
}

.form-control.is-invalid,
.form-select.is-invalid {
	border-color: #dc3545;
	background-color: #fff8f8;
}

.invalid-feedback {
	display: block;
	width: 100%;
	margin-top: 0.25rem;
	font-size: 0.875rem;
	color: #dc3545;
	font-weight: 500;
}

/* Form Actions */
.form-actions {
	margin-top: 2rem;
	padding-top: 2rem;
	border-top: 2px solid #e9ecef;
}

.alert {
	border-radius: 8px;
	border: none;
	padding: 1rem 1.25rem;
	margin-bottom: 1.5rem;
	font-weight: 500;
}

.alert-danger {
	background-color: #f8d7da;
	color: #721c24;
	border-left: 4px solid #dc3545;
}

.alert-success {
	background-color: #d4edda;
	color: #155724;
	border-left: 4px solid #28a745;
}

.action-buttons {
	display: flex;
	justify-content: flex-end;
	gap: 1rem;
	align-items: center;
}

.btn {
	padding: 0.75rem 1.5rem;
	border-radius: 8px;
	font-weight: 600;
	font-size: 0.9rem;
	text-transform: uppercase;
	letter-spacing: 0.5px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
}

.btn:hover {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-color: #667eea;
	color: white;
}

.btn-primary:hover {
	background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
	border-color: #5a6fd8;
}

.btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
	transform: none;
	box-shadow: none;
}

/* Responsive Design */
@media (max-width: 768px) {
	.create-aws-container {
		max-width: 100%;
		margin: 0 1rem;
	}
	
	.form-header {
		padding: 1.5rem;
	}
	
	.header-content {
		flex-direction: column;
		text-align: center;
		gap: 1rem;
	}
	
	.aws-form {
		padding: 1.5rem;
	}
	
	.form-section {
		padding: 1rem;
	}
	
	.action-buttons {
		flex-direction: column;
		align-items: stretch;
	}
	
	.btn {
		justify-content: center;
	}
}

/* Dark Mode Support - Override global dark mode */
body.dark-only .aws-form {
	background: #2a2b36 !important;
	border-color: #3a3b46 !important;
	color: white !important;
}

body.dark-only .form-section {
	background: #1d1e26 !important;
	border-color: #3a3b46 !important;
	color: white !important;
}

body.dark-only .form-section:hover {
	background: #2a2b36 !important;
}

body.dark-only .form-label {
	color: #e9ecef !important;
}

body.dark-only .form-control,
body.dark-only .form-select,
body.dark-only .form-datepicker {
	background: #1d1e26 !important;
	border-color: #3a3b46 !important;
	color: white !important;
}

body.dark-only .section-header h5 {
	color: #e9ecef !important;
}

/* Light Mode - Ensure white backgrounds (default) */
.aws-form {
	background: white !important;
}

.form-section {
	background: #f8f9fa !important;
}

.form-section:hover {
	background: white !important;
}

.form-label {
	color: #495057 !important;
}

.form-control,
.form-select,
.form-datepicker {
	background: white !important;
	color: #495057 !important;
}

.section-header h5 {
	color: #495057 !important;
}

/* Animation for form sections */
.form-section {
	animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
	from {
		opacity: 0;
		transform: translateY(20px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

/* Stagger animation for form sections */
.form-section:nth-child(1) { animation-delay: 0.1s; }
.form-section:nth-child(2) { animation-delay: 0.2s; }
.form-section:nth-child(3) { animation-delay: 0.3s; }

/* Datepicker Overlap Fix */
:deep(.vuepic__datepicker) {
	z-index: 1000 !important;
}

:deep(.vuepic__datepicker__container) {
	z-index: 1000 !important;
}

:deep(.vuepic__datepicker__calendar) {
	z-index: 1000 !important;
}

/* Select dropdown arrow */
.form-select {
	appearance: none;
	background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
	background-position: right 0.75rem center;
	background-repeat: no-repeat;
	background-size: 1.5em 1.5em;
	padding-right: 2.5rem;
}

/* Spinner animation */
.spinner {
	animation: spin 1s linear infinite;
}

@keyframes spin {
	from { transform: rotate(0deg); }
	to { transform: rotate(360deg); }
}
</style>