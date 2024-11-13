<template>
    <div class="row">
        <div class="col-sm-4">
        <label>Device Location</label>
                <input class="form-control" type="text" placeholder="Enter project Rate">
        </div>   
        <div class="col-sm-4">
            <div class="mb-3">
                <label>Device Type</label>
                <select class="form-select">
                    <option>Zentra</option>
                    <option>Barani</option>
                    <option>3D-Paws</option>
                    <option>Sutron</option>
                    <option>OTT Hydromet</option>
                </select>
            </div>
        </div>   
        <div class="col-sm-4">
            <div class="mb-3">
                <label>Date</label>
                <datepicker class="datepicker-here form-control" v-model="date" :format="format" />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
const date = ref<Date | null>(null);
const date1 = ref<Date | null>(null);
const format = (date: Date | null): string => {
    if (date === null) {
        return '';
    }

    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();

    return ` ${day}/${month}/${year}`;
};
</script>