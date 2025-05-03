<template>
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">Billing</h4>
            </div>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Date Billed</th>
                            <th>Date Verified</th>
                            <th>Package</th>
                            <th>Amount</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bill in userBills" :key="bill.id">
                            <td>{{ formatDate(bill.created_at) }}</td>
                            <td>{{ bill.receipt_verified_at ? formatDate(bill.receipt_verified_at) : '-' }}</td>
                            <td>{{ bill.package }}</td>
                            <td>${{ bill.total }}</td>
                            <td>
                                <button 
                                    :class="[
                                        'status-btn',
                                        getStatusClass(bill)
                                    ]"
                                >
                                    <span class="status-dot"></span>
                                    {{ bill.verification_status }}
                                </button>
                            </td>
                           
                            <td>
                                <button 
                                    v-if="!bill.receipt_upload"
                                    @click="navigateToUploadReceipt(bill)"
                                    class="btn btn-sm btn-primary"
                                >
                                    Upload Receipt
                                </button>
                                <a 
                                    v-if="bill.receipt_upload"
                                    @click="viewReceipt(bill.id)"
                                    class="text-purple"
                                    style="cursor: pointer; text-decoration: none;"
                                >
                                    <i class="fa fa-eye"></i> View
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Upload Modal -->
        <div class="modal" ref="uploadModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Upload Receipt</h5>
                        <button type="button" class="close" @click="closeUploadModal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <input 
                            type="file" 
                            class="form-control" 
                            @change="handleFileUpload"
                            accept="image/*,.pdf"
                        >
                    </div>
                    <div class="modal-footer">
                        <button 
                            class="btn btn-primary" 
                            @click="submitReceipt"
                            :disabled="!selectedFile"
                        >
                            Upload
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- View Modal -->
        <div class="modal" ref="viewModal">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">View Receipt</h5>
                        <button type="button" class="close" @click="closeViewModal">&times;</button>
                    </div>
                    <div class="modal-body p-0">
                        <div class="receipt-container">
                            <iframe 
                                v-if="receiptUrl && !isImage"
                                :src="receiptUrl"
                                class="receipt-iframe"
                            ></iframe>
                            <img 
                                v-if="isImage"
                                :src="receiptUrl"
                                class="receipt-image"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import { useRoute, useRouter } from 'vue-router'

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)

interface Bill {
    id: number;
    created_at: string;
    package: string;
    total: number;
    receipt_upload: string | null;
    receipt_verified: boolean;
    verification_status: string;
    receipt_verified_at: string | null;
}

const userBills = ref<Bill[]>([])
const uploadModal = ref<HTMLElement | null>(null)
const selectedFile = ref<File | null>(null)
const currentBillId = ref(null)
const viewModal = ref<HTMLElement | null>(null)
const receiptUrl = ref<string | undefined>(undefined)
const isImage = ref(false)

const router = useRouter()
const route = useRoute()

onMounted(async () => {
    const token = localStorage.getItem('access_token')
    if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    await fetchUserBills()
})

const fetchUserBills = async () => {
    try {
        const route = useRoute();
        const profileId = route.query.id;
        
        console.log('Profile ID from route:', profileId);
        
        const token = localStorage.getItem('access_token')
        const response = await axios.get('/bills/', {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            params: profileId ? { user_id: profileId } : {}
        })
        console.log('Bills response:', response.data)
        userBills.value = response.data
    } catch (error: any) {
        console.error('Error details:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
            url: error.config?.url
        })
    }
}

const getStatusClass = (bill: Bill) => {
    if (!bill.receipt_upload) {
        return 'status-inactive'
    }
    if (bill.receipt_verified) {
        return 'status-active'
    }
    return 'status-pending'
}

const navigateToUploadReceipt = (bill: Bill) => {
    const userId = route.query.id || currentUser.value?.id
    router.push({
        path: '/users/edit',
        query: {
            id: userId,
            bill_id: bill.id
        }
    })
}

const viewReceipt = async (billId: number) => {
    try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get(`/bills/${billId}/receipt_upload/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            },
            responseType: 'blob'
        })
        
        const contentType = response.headers['content-type']
        const blob = new Blob([response.data], { type: contentType })
        
        isImage.value = contentType.startsWith('image/')
        receiptUrl.value = URL.createObjectURL(blob)
        
        if (viewModal.value) {
            viewModal.value.style.display = 'block'
        }
    } catch (error) {
        console.error('Error viewing receipt:', error)
    }
}

const handleFileUpload = (event: Event) => {
    const target = event.target as HTMLInputElement
    selectedFile.value = target.files?.[0] || null
}

const submitReceipt = async () => {
    if (!selectedFile.value || !currentBillId.value) return

    const formData = new FormData()
    formData.append('receipt_upload', selectedFile.value)

    try {
        await axios.post(`/api/bills/${currentBillId.value}/upload_receipt/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        await fetchUserBills()
        closeUploadModal()
    } catch (error) {
        console.error('Error uploading receipt:', error)
    }
}

const closeUploadModal = () => {
    if (uploadModal.value) {
        uploadModal.value.style.display = 'none'
    }
    selectedFile.value = null
    currentBillId.value = null
}

const closeViewModal = () => {
    if (viewModal.value) {
        viewModal.value.style.display = 'none'
    }
    receiptUrl.value = undefined
}

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString()
}
</script>

<style scoped>
.status-btn {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    cursor: default;
    min-width: 140px;
    justify-content: flex-start;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.status-active {
    background-color: rgba(40, 167, 69, 0.1);
    color: #28a745;
}

.status-active .status-dot {
    background-color: #28a745;
}

.status-pending {
    background-color: rgba(255, 193, 7, 0.1);
    color: #ffc107;
}

.status-pending .status-dot {
    background-color: #ffc107;
}

.status-inactive {
    background-color: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.status-inactive .status-dot {
    background-color: #dc3545;
}

.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 1000;
}

.text-purple {
    color: #7366ff;
}

.modal-body {
    max-height: 80vh;
    overflow: hidden;
}

.receipt-container {
    width: 100%;
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f8f8;
}

.receipt-iframe {
    width: 100%;
    height: 100%;
    border: none;
    transform-origin: center;
    transform: scale(0.95);
}

.receipt-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    padding: 1rem;
}
</style>