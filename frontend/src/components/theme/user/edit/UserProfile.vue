<template>
    <div class="col-xl-4">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">Package Information</h4>
                <div class="card-options">
                    <a class="card-options-collapse" href="#" data-bs-toggle="card-collapse">
                        <i class="fe fe-chevron-up"></i>
                    </a>
                    <a class="card-options-remove" href="#" data-bs-toggle="card-remove">
                        <i class="fe fe-x"></i>
                    </a>
                </div>
            </div>
            <div class="card-body">
                <form>
                    <div class="mb-4">
                        <label class="form-label">Package Details</label>
                        <div class="info-row">
                            <span class="info-value">{{ userData.package || 'No Package' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-value">Expires: {{ currentDate }}</span>
                        </div>
                    </div>
                    <div class="mb-4">
                        <label class="form-label">Upload Image</label>
                        <div class="dropzone-container">
                            <DropZone 
                                :maxFileSize="Number(60000000)" 
                                class="show-preview" 
                                :uploadOnDrop="true"
                                :multipleUpload="false"
                                :maxFiles="1"
                                @file-added="handleFileAdded"
                            />
                            <div class="file-info">
                                <p>Accepted file types: .jpg, .jpeg, .png</p>
                                <p>Maximum file size: 60MB</p>
                            </div>
                        </div>
                    </div>
                    <div class="form-footer">
                        <button class="btn btn-primary btn-block" @click.prevent="saveProfile">Save</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import DropZone from "dropzone-vue"
import 'dropzone-vue/dist/dropzone-vue.common.css'

const currentDate = ref(new Date().toLocaleDateString())
const userData = ref({
    package: '',
    imageFile: null as File | null
})

// Simulating fetching user data - replace with actual API call
const fetchUserPackage = async () => {
    // Replace this with actual API call
    userData.value.package = 'Monthly' // This would come from the API
}

onMounted(() => {
    fetchUserPackage()
})

const handleFileAdded = (file: File) => {
    userData.value.imageFile = file
}

const saveProfile = () => {
    console.log('Saving profile:', {
        imageFile: userData.value.imageFile
    })
}
</script>

<style scoped>
.info-row {
    padding: 0.5rem 0;
}

.info-value {
    color: #6c757d;
    font-size: 0.875rem;
}

.form-label {
    font-weight: 600;
    color: #2c323f;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
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
    border-radius: 8px;
    background: #f8f8f8;
    padding: 20px;
    min-height: 300px;
    display: flex;
    flex-direction: column;
}

:deep(.dropzone) {
    flex: 1;
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    margin-bottom: 15px;
}

:deep(.dropzone .dz-message) {
    margin: 0;
    font-size: 1.1em;
    color: #666;
}

:deep(.dropzone .dz-preview) {
    margin: 10px;
}

.file-info {
    text-align: center;
    color: #666;
    font-size: 0.9em;
    border-top: 1px solid #e0e0e0;
    padding-top: 15px;
}

.file-info p {
    margin: 5px 0;
}
</style>