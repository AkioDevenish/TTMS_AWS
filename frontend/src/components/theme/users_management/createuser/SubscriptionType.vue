<template>
    <div class="row">
        <div class="col-sm-12">
            <div class="mb-3">
                <label>Package</label>
                <select 
                    class="form-select"
                    v-model="selectedPackage"
                    :class="inputClasses.package"
                    @change="emitPackageSelection">
                    <option value="">Select Package</option>
                    <option value="Weekly">Weekly</option>
                    <option value="Monthly">Monthly</option>
                    <option value="Yearly">Yearly</option>
                </select>
                <div class="invalid-feedback" v-if="!selectedPackage">
                    Please select a package
                </div>
            </div>
        </div>   
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'

const selectedPackage = ref('')
const inputClasses = reactive({
    package: ''
})

const emitPackageSelection = () => {
    inputClasses.package = selectedPackage.value ? 'is-valid' : 'is-invalid'
    emit('package-selected', selectedPackage.value)
}

const emit = defineEmits(['package-selected'])
</script>