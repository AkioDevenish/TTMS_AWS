<template>
    <div class="row">
        <div class="col-sm-4">
        <label>Password</label>
            <input class="form-control" type="Password" placeholder="Password">
        </div>   
        <div class="col-sm-12">
            <div class="mb-3">
                <label>Package</label>
                <select class="form-select">
                    <option>Weekly</option>
                    <option>Monthly</option>
                    <option>Yearly</option>
                </select>
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