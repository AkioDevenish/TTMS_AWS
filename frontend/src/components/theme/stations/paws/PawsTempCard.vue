<template>
    <div>
        <div class="row g-2">
            <div class="col-xl-3 col-md-6 proorder-xl-3 proorder-md-3" v-for="(item, index) in localPawsData" :key="index">
                <Card1 :cardbodyClass="item.cardclass">
                    <div class="d-flex gap-2 align-items-end">
                        <div class="flex-grow-1">
                            <h2>{{ item.number }}</h2>
                            <p class="mb-0 text-truncate">{{ item.text }}</p>
                            <div class="d-flex student-arrow text-truncate">
                                <p class="mb-0 up-arrow " :class="item.iconclass"><i :class="item.icon"></i></p>
                                <span class="f-w-500 " :class="item.fontclass">{{ item.total }}%</span>{{ item.month }}
                            </div>
                        </div>
                        <div class="flex-shrink-0"><img :src="getImages(item.img)" alt="">
                        </div>
                    </div>
                </Card1>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import axios from 'axios'
import { getImages } from "@/composables/common/getImages"

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

// Reactive reference to modify paws_data
const localPawsData = ref([])

// Helper function to get unit
const getUnit = (measurementName: string) => {
   switch(measurementName) {
       case 'BMX280 Pressure': return 'hPa'
       case 'Air Temperature': return '°C'
       case 'Rain Gauge': return 'mm'
       case 'MCP9808 Temperature': return '°C'
       case 'Wind Direction': return '°'
       case 'Wind Speed': return 'm/s'
       default: return ''
   }
}

// Helper function to get image
const getImage = (measurementName: string) => {
   switch(measurementName) {
       case 'BMX280 Pressure': return 'dashboard-4/icon/student.png'
       case 'Air Temperature': return 'dashboard-4/icon/student.png'
       case 'Rain Gauge': return 'dashboard-4/icon/student.png'
       case 'MCP9808 Temperature': return 'dashboard-4/icon/student.png'
       case 'Wind Direction': return 'dashboard-4/icon/student.png'
       case 'Wind Speed': return 'dashboard-4/icon/student.png'
       default: return 'dashboard-4/icon/student.png'
   }
}

// Function to transform API data, filter for Instrument 1, and get latest data for each measurement type
const transformApiData = (apiData: any[]) => {
    // Filter for Instrument 1 data
    const instrument1Data = apiData.filter(item => item.name === "Instrument 1")
    
    const measurementMap = new Map()

    instrument1Data.forEach(item => {
        // For each measurement, check if we already have a more recent timestamp
        if (!measurementMap.has(item.measurement_name) || new Date(measurementMap.get(item.measurement_name).timestamp) < new Date(item.timestamp)) {
            measurementMap.set(item.measurement_name, {
                number: `${item.value} ${getUnit(item.measurement_name)}`,
                text: item.measurement_name,
                iconclass: item.value > 0 ? "bg-light-success" : "bg-light-danger",
                icon: item.value > 0 
                    ? "icon-arrow-up font-success" 
                    : "icon-arrow-down font-danger",
                img: getImage(item.measurement_name),
                cardclass: "student",
                fontclass: item.value > 0 ? "font-success" : "font-danger",
                total: Math.abs(item.value).toFixed(1),
                month: new Date(item.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
                timestamp: item.timestamp // Store the timestamp for comparison
            })
        }
    })

    return Array.from(measurementMap.values())
}

// Fetch data on component mount
onMounted(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/instrument_measurements/')
        const transformedData = transformApiData(response.data)
        
        // Update localPawsData if transformed data exists
        if (transformedData.length > 0) {
            localPawsData.value = transformedData
        }
    } catch (error) {
        console.error('Error fetching instrument measurements:', error)
    }
})
</script>
