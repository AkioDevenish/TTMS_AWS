<template>
    <ul>
        <li><span class="time digits" v-text="days"></span><span class="title">days</span></li>
        <li><span class="time digits" v-text="hours"></span><span class="title">Hours</span></li>
        <li><span class="time digits" v-text="minutes"></span><span class="title">Min</span></li>
        <li><span class="time digits" v-text="seconds"></span><span class="title">Sec</span></li>
    </ul>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue"
let td = ref<number>(0)
let days = ref<number>(0)
let hours = ref<number>(0)
let minutes = ref<number>(0)
let seconds = ref<number>(0)
let startTime = ref<string | number>('')
let endTime = ref<string | number>('')
function timer() {
    setInterval(() => {
        endTime.value = new Date().getTime()
        startTime.value = new Date('Jan 1, 2024 00:00:00').getTime(),
            td.value = endTime.value - startTime.value
        if (td.value >= 0) {
            seconds.value = Math.floor(td.value / 1000 % 60);
            minutes.value = Math.floor(td.value / 1000 / 60 % 60);
            hours.value = Math.floor(td.value / (1000 * 60 * 60) % 24);
            days.value = Math.floor(td.value / (1000 * 60 * 60 * 24));
        } else {
            seconds.value = minutes.value = hours.value = days.value = 0;
        }
    });

}
onMounted(() => {
    timer()
})
</script>