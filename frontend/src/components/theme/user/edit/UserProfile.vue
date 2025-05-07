<template>
    <div class="col-xl-8 mx-auto">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">Receipt Verification</h4>
            </div>
            <div class="card-body">
                <form class="p-4" @submit.prevent="uploadReceipt">
                    <div class="mb-4">
                        <label class="form-label h5">Upload Receipt</label>
                        <div class="dropzone-container">
                            <div class="dropzone">
                                <div class="dz-message needsclick">
                                    <input 
                                        type="file" 
                                        id="receipt-upload"
                                        class="hidden-input"
                                        @change="handleFileChange"
                                        accept=".jpg,.jpeg,.png,.pdf"
                                    />
                                    <label for="receipt-upload" class="upload-label">
                                        <i class="fa fa-cloud-upload"></i>
                                        <span>Drop files here or click to upload</span>
                                        <div v-if="selectedFile" class="selected-file">
                                            Selected: {{ selectedFile.name }}
                                        </div>
                                    </label>
                                </div>
                            </div>
                            <div class="file-info">
                                <p>Accepted file types: .jpg, .jpeg, .png, .pdf</p>
                                <p>Maximum file size: 60MB</p>
                            </div>
                        </div>
                    </div>
                    <div v-if="successMessage" class="alert alert-success">
                        {{ successMessage }}
                    </div>
                    <div v-if="errorMessage" class="alert alert-danger">
                        {{ errorMessage }}
                    </div>
                    <div class="form-footer">
                        <button 
                            type="submit"
                            class="btn btn-primary btn-lg w-100" 
                            :disabled="!selectedFile || isUploading"
                        >
                            {{ isUploading ? 'Uploading...' : 'Upload Receipt' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)
const route = useRoute()
const isUploading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const selectedFile = ref<File | null>(null)

const userData = ref({
    package: '',
    expires_at: null as string | null,
    receipt_verification_status: ''
})

// Add validation computed property
const isFormValid = computed(() => {
    return selectedFile.value !== null
})

const formatDate = (date: string | null) => {
    if (!date) return 'N/A'
    return new Date(date).toLocaleDateString()
}

const fetchUserData = async () => {
    try {
        const token = localStorage.getItem('access_token')
        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
        
        const userId = route.query.id
        // Match the endpoint used in useUserManagement
        const response = await axios.get('/users/', { headers })
        
        if (Array.isArray(response.data)) {
            const user = response.data.find((u: any) => u.id === parseInt(userId as string))
            if (user) {
                userData.value = {
                    package: user.package || 'No Package',
                    expires_at: user.expires_at,
                    receipt_verification_status: user.receipt_verification_status
                }
                console.log('Fetched user data:', user)
            }
        }
    } catch (error) {
        console.error('Error fetching user data:', error)
        errorMessage.value = 'Failed to fetch user data'
    }
}

const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement
    if (input.files && input.files[0]) {
        const file = input.files[0]
        if (file.size > 60000000) {
            errorMessage.value = 'File size exceeds 60MB limit'
            input.value = ''
            return
        }
        selectedFile.value = file
        errorMessage.value = ''
    }
}

const uploadReceipt = async () => {
    if (!selectedFile.value) return

    const formData = new FormData()
    formData.append('receipt_upload', selectedFile.value)
    
    try {
        isUploading.value = true
        errorMessage.value = ''
        successMessage.value = ''
        
        const token = localStorage.getItem('access_token')
        const billId = route.query.bill_id
        
        const response = await axios.post(`/bills/${billId}/upload_receipt/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data'
            }
        })
        
        if (response.data) {
            successMessage.value = 'Receipt uploaded successfully'
            selectedFile.value = null
        }
    } catch (error: any) {
        errorMessage.value = error.response?.data?.error || 'Failed to upload receipt'
    } finally {
        isUploading.value = false
    }
}

onMounted(() => {
    fetchUserData()
})
</script>

<style scoped>
.info-row {
    padding: 1rem 0;
}

.info-value {
    color: #2c323f;
    font-size: 1rem;
}

.form-label {
    font-weight: 600;
    color: #2c323f;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}

.package-info-container {
    background: #ffffff;
    padding: 1rem;
}

.ttl-info {
    padding: 1rem;
    border: 1px solid #efefef;
    border-radius: 0.25rem;
}

.ttl-info h6 {
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
    color: #2c323f;
}

.ttl-info h6 i {
    margin-right: 0.5rem;
    color: #7366ff;
}

.ttl-info span {
    color: #898989;
    font-size: 0.875rem;
}

.avatar-upload {
    position: relative;
    max-width: 205px;
}

.avatar-edit {
    position: absolute;
    right: 12px;
    z-index: 1;
    top: 10px;
}

.avatar-edit input {
    display: none;
}

.avatar-edit label {
    display: inline-block;
    width: 34px;
    height: 34px;
    margin-bottom: 0;
    border-radius: 100%;
    background: #FFFFFF;
    border: 1px solid transparent;
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
    cursor: pointer;
    font-weight: normal;
    transition: all .2s ease-in-out;
}

.avatar-edit label:hover {
    background: #f1f1f1;
    border-color: #d6d6d6;
}

.avatar-edit label:after {
    content: "\f040";
    font-family: 'FontAwesome';
    color: #757575;
    position: absolute;
    top: 10px;
    left: 0;
    right: 0;
    text-align: center;
    margin: auto;
}

.dropzone-container {
    border: 2px dashed #e0e0e0;
    border-radius: 12px;
    background: #f8f8f8;
    padding: 30px;
    min-height: 400px;
    display: flex;
    flex-direction: column;
}

:deep(.dropzone) {
    flex: 1;
    min-height: 350px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    margin-bottom: 20px;
}

:deep(.dropzone .dz-message) {
    margin: 0;
    font-size: 1.1em;
    color: #666;
}

:deep(.dropzone .dz-preview .dz-progress) {
    display: none !important;
}

:deep(.dropzone .dz-preview) {
    margin: 10px;
}

.file-info {
    text-align: center;
    color: #666;
    font-size: 1rem;
    border-top: 1px solid #e0e0e0;
    padding-top: 20px;
}

.file-info p {
    margin: 8px 0;
}

.form-footer {
    margin-top: 2rem;
}

.hidden-input {
    display: none;
}

.upload-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 350px;
    cursor: pointer;
    color: #666;
}

.upload-label i {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #7366ff;
}

.upload-label span {
    font-size: 1.1em;
}

.selected-file {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #f0f0f0;
    border-radius: 4px;
    font-size: 0.9em;
}
</style>