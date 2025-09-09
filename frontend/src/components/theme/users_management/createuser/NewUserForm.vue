<template>
  <div v-if="isAdminUser">

    <!-- Main Form -->
    <form @submit.prevent="createUser">
      <!-- Personal Information Section -->
      <div class="form-section">
        <div class="section-header">
          <h5>Personal Information</h5>
        </div>

        <div class="row">
          <div class="col-sm-12 col-md-6">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input
                  class="form-control"
                  type="text"
                  :class="inputClasses.first_name"
                  placeholder="Enter first name"
                  v-model="formData.first_name"
                  @input="validateField('first_name')">
              <div class="invalid-feedback">First name is required</div>
            </div>
          </div>
          <div class="col-sm-12 col-md-6">
            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input
                  class="form-control"
                  type="text"
                  :class="inputClasses.last_name"
                  placeholder="Enter last name"
                  v-model="formData.last_name"
                  @input="validateField('last_name')">
              <div class="invalid-feedback">Last name is required</div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label">Organization</label>
              <input
                  class="form-control"
                  type="text"
                  :class="inputClasses.organization"
                  placeholder="Enter organization name"
                  v-model="formData.organization"
                  @input="validateField('organization')">
            </div>
          </div>
        </div>
      </div>

      <!-- Account Information Section -->
      <div class="form-section">
        <div class="section-header">
          <h5>Account Information</h5>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label">Email Address *</label>
              <input class="form-control" type="email" :class="inputClasses.email" placeholder="Enter email address"
                     v-model="formData.email" @input="validateField('email')">
              <div class="invalid-feedback">Valid email address is required</div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label">Password *</label>
              <input class="form-control" type="password" :class="inputClasses.password" placeholder="Enter password"
                     v-model="formData.password" @input="validateField('password')">
              <div class="invalid-feedback">Password is required</div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label">Role *</label>
              <select class="form-select" :class="inputClasses.role" v-model="formData.role"
                      @change="validateField('role')">
                <option value="">Select Role</option>
                <option value="admin">Admin</option>
                <option value="user">User</option>
              </select>
              <div class="invalid-feedback">Role selection is required</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Subscription Details Section -->
      <div class="form-section">
        <div class="section-header">
          <h5>Subscription Details</h5>
        </div>

        <div class="row">
          <div class="col-sm-6">
            <div class="form-group">
              <label class="form-label">Package *</label>
              <select class="form-select" v-model="formData.package" :class="inputClasses.package">
                <option value="">Select Package</option>
                <option value="Weekly">Weekly</option>
                <option value="Monthly">Monthly</option>
                <option value="Yearly">Yearly</option>
              </select>
              <div class="invalid-feedback">Package selection is required</div>
            </div>
          </div>
          <div class="col-sm-6">
            <div class="form-group">
              <label class="form-label">Price *</label>
              <select
                  class="form-select"
                  v-model="formData.subscription_price"
                  :class="inputClasses.subscription_price">
                <option value="">Select Price</option>
                <option :value="1500">$1,500</option>
                <option :value="3000">$3,000</option>
                <option :value="6000">$6,000</option>
              </select>
              <div class="invalid-feedback">Price selection is required</div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label">Expires At</label>
              <input type="text" class="form-control" :value="formData.expires_at" disabled />
              <small class="form-text text-muted">Automatically calculated based on package selection</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>

        <div class="action-buttons">
          <button type="button" class="btn btn-secondary me-3" @click="cancel" :disabled="isSubmitting">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary" @click="createUser" :disabled="isSubmitting">
            <svg v-if="isSubmitting" width="16" height="16" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg" class="me-2 spinner">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-dasharray="31.416" stroke-dashoffset="31.416">
                <animate attributeName="stroke-dasharray" dur="2s" values="0 31.416;15.708 15.708;0 31.416"
                         repeatCount="indefinite" />
                <animate attributeName="stroke-dashoffset" dur="2s" values="0;-15.708;-31.416"
                         repeatCount="indefinite" />
              </circle>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
                 class="me-2">
              <path
                  d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H4C2.93913 15 2.02172 15.4214 1.27157 16.1716C0.52143 16.9217 0 17.9391 0 19V21"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <circle cx="8" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round" />
              <path d="M20 8V6C20 4.93913 19.5786 3.92172 18.8284 3.17157C18.0783 2.42143 17.0609 2 16 2H12"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M12 2L14 4L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
            </svg>
            {{ isSubmitting ? 'Creating...' : 'Create User' }}
          </button>
        </div>
      </div>
    </form>
  </div>
  <div v-else>
    <div class="access-denied">
      <h3>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="me-2">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" />
          <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2" />
          <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2" />
        </svg>
        Access Denied
      </h3>
      <p>You don't have permission to access this page.</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import axios from 'axios';

const router = useRouter();
const authStore = useAuthStore();
const currentUser = computed(() => authStore.currentUser);

const isAdminUser = computed(() => {
  return currentUser.value?.is_superuser === true;
});

onMounted(async () => {
  if (!isAdminUser.value) {
    router.push('/dashboard/default');
  }
});

// Form data
const formData = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  organization: '',
  role: '',
  package: '',
  expires_at: '',
  subscription_price: 0
});

// Form state
const inputClasses = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  organization: '',
  role: '',
  package: '',
  subscription_price: ''
});

const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// Validation
const validateField = (field: string) => {
  if (formData[field as keyof typeof formData]) {
    inputClasses[field as keyof typeof inputClasses] = 'is-valid';
  } else {
    inputClasses[field as keyof typeof inputClasses] = 'is-invalid';
  }
};

const validateForm = (): boolean => {
  let isValid = true;

  // Validate all fields
  validateField('first_name');
  validateField('last_name');
  validateField('email');
  validateField('password');
  validateField('organization');
  validateField('role');

  // Check if any field is invalid
  Object.values(inputClasses).forEach(className => {
    if (className === 'is-invalid') isValid = false;
  });

  // Check if package is selected
  if (!formData.package) {
    isValid = false;
    errorMessage.value = 'Please select a package';
  }

  // Check if price is selected
  if (!formData.subscription_price) {
    isValid = false;
    errorMessage.value = 'Please select a price';
  }

  return isValid;
};

const calculateExpiryDate = (packageType: string): string => {
  const today = new Date();
  let expiryDate = new Date(today);

  switch (packageType.toLowerCase()) {
    case 'weekly':
      expiryDate.setDate(today.getDate() + 7);
      break;
    case 'monthly':
      expiryDate.setMonth(today.getMonth() + 1);
      break;
    case 'yearly':
      expiryDate.setFullYear(today.getFullYear() + 1);
      break;
    default:
      return '';
  }

  // Format date as YYYY-MM-DD
  return expiryDate.toISOString().split('T')[0];
};

// Update formData when package changes
watch(() => formData.package, (newPackage) => {
  if (newPackage) {
    formData.expires_at = calculateExpiryDate(newPackage);
  }
});

// API interaction
const createUser = async () => {
  try {
    if (!validateForm()) return;

    const token = localStorage.getItem('access_token');
    if (!token) {
      errorMessage.value = 'Not authorized. Please log in again.';
      router.push('/auth/login');
      return;
    }

    isSubmitting.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    const userData = {
      first_name: formData.first_name.trim(),
      last_name: formData.last_name.trim(),
      email: formData.email.trim(),
      password: formData.password,
      organization: formData.organization?.trim() || '',
      role: formData.role.toLowerCase(),
      package: formData.package,
      status: 'Active',
      expires_at: formData.expires_at || calculateExpiryDate(formData.package),
      subscription_price: formData.subscription_price,
    };

    console.log('Sending user data:', userData);

    const response = await axios.post('/api/users/', userData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('Server response:', response.data);
    successMessage.value = 'User created successfully!';

    setTimeout(() => {
      router.push('/users_management');
    }, 1000);

  } catch (error: any) {
    console.error('Error creating user:', error.response || error);

    if (error.response?.data) {
      const errorData = error.response.data;
      if (typeof errorData === 'object') {
        if (errorData.error) {
          errorMessage.value = errorData.error;
        } else if (errorData.detail) {
          errorMessage.value = errorData.detail;
        } else {
          // Handle field-specific errors
          const firstError = Object.entries(errorData)[0];
          if (firstError) {
            const [field, messages] = firstError;
            errorMessage.value = Array.isArray(messages)
                ? (messages as string[])[0]
                : String(messages);
          }
        }
      } else {
        errorMessage.value = errorData.toString();
      }
    } else {
      errorMessage.value = 'Error creating user. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
};

const cancel = () => {
  router.push('/users');
};
</script>

<style scoped>
/* Main Container */

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
.user-form {
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

.form-control,
.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: white;
}

.form-control:focus,
.form-select:focus {
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

/* Form Text */
.form-text {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.25rem;
  font-style: italic;
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

.btn-secondary {
  background: #6c757d;
  border-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  border-color: #5a6268;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Access Denied */
.access-denied {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
}

.access-denied h3 {
  color: #dc3545;
  margin-bottom: 1rem;
  font-weight: 600;
}

.access-denied p {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {

  .form-header {
    padding: 1.5rem;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .user-form {
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
body.dark-only .user-form {
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
body.dark-only .form-select {
  background: #1d1e26 !important;
  border-color: #3a3b46 !important;
  color: white !important;
}

body.dark-only .section-header h5 {
  color: #e9ecef !important;
}

body.dark-only .access-denied {
  background: #2a2b36 !important;
  border-color: #3a3b46 !important;
  color: white !important;
}

body.dark-only .access-denied h3 {
  color: #ff6b6b !important;
}

body.dark-only .access-denied p {
  color: #adb5bd !important;
}

/* Light Mode - Ensure white backgrounds (default) */
.user-form {
  background: white !important;
}

.form-section {
  background: #f8f9fa !important;
}

.form-label {
  color: #495057 !important;
}

.form-control,
.form-select {
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
.form-section:nth-child(1) {
  animation-delay: 0.1s;
}

.form-section:nth-child(2) {
  animation-delay: 0.2s;
}

.form-section:nth-child(3) {
  animation-delay: 0.3s;
}

/* Spinner animation */
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
