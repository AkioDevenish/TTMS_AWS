<template>
    <div class="row">
        <label class="col-xxl-3 box-col-12 text-start">Time Picker</label>
        <div class="col-xxl-9 box-col-12">
            <div class="input-group">
                <Datepicker class="" v-model="time" timePicker />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
const time = ref({
    hours: new Date().getHours(),
    minutes: new Date().getMinutes()
});
</script>