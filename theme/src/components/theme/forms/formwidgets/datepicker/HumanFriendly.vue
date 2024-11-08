<template>
    <div class="row">
        <label class="col-xxl-3 box-col-12 text-start">Human Friendly </label>
        <div class="col-xxl-9 box-col-12">
            <div class="input-group flatpicker-calender">
                <datepicker class="" v-model="month" monthPicker />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
const month = ref({
    month: new Date().getMonth(),
    year: new Date().getFullYear()
});
</script>