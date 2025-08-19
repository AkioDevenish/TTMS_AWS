<template>
    <Card1 colClass="col-xl-12 col-md-12 proorder-md-1" headerTitle="true" :title="monitorTitle"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 assignments-table px-0">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <table class="table display dataTable" id="assignments-table" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>ID</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody v-if="!latestData.length">
                        <tr class="odd">
                            <td valign="top" colspan="6" class="dataTables_empty">{{ connectionStatus }}</td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr v-for="(item, index) in latestData" :key="index">
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center">  
                                        <h6>{{ item.name }}</h6>
                                        <div class="status-indicator-container">
                                            <div 
                                                class="status-indicator" 
                                                :class="getStatusClass(item.status)"
                                                :title="getStatusTooltip(item.status)"
                                            ></div>
                                        </div>
                                    </div>
                                    <div v-if="item.dataQuality" class="data-quality-info ms-2">
                                        <small class="text-muted">
                                            {{ item.dataQuality.validCount }}/{{ item.dataQuality.totalCount }} valid
                                            ({{ item.dataQuality.validPercentage }}%)
                                        </small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ item.id }}</td>
                            <td>{{ formatDateTime.date(item.lastUpdated) }}</td>
                            <td>{{ formatDateTime.time(item.lastUpdated) }}</td>
                            <td>{{ item.status }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, watch, defineProps } from 'vue'
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const props = defineProps({
    selectedStation: {
        type: Number,
        required: true
    },
    measurements: {
        type: Array,
        default: () => []
    },
    stationInfo: {
        type: Object,
        default: () => ({})
    }
});
const latestData = ref<any[]>([])
const connectionStatus = ref<string>('Unsuccessful')
const monitorTitle = ref<string>('Zentra Monitor')

// Helper methods for status display
const getStatusClass = (status: string) => {
    if (status === 'Online') return 'status-online'
    if (status === 'Online Erroneous Data') return 'status-online-erroneous-data'
    if (status === 'Offline') return 'status-offline'
    return 'status-unknown'
}

const getStatusTooltip = (status: string) => {
    if (status === 'Online') return 'Station is online and reporting valid data within expected parameters'
    if (status === 'Online Erroneous Data') return 'Station is transmitting but data fails validation'
    if (status === 'Offline') return 'Station is offline or not reporting data (no recent transmissions)'
    return 'Station status unknown'
}

// Function to check for stuck sensor (always reading the same value)
const checkStuckSensor = (measurements: any[], sensorType: string) => {
    if (measurements.length < 5) return false; // Need at least 5 measurements to determine if stuck
    
    const firstValue = parseFloat(measurements[0].value);
    if (isNaN(firstValue)) return false; // Cannot determine if stuck if value is NaN
    
    const tolerance = 0.1; // Tolerance for considering values "the same"
    
    // Check if all subsequent values are within tolerance of the first value
    const isStuck = measurements.every(m => {
        const value = parseFloat(m.value);
        return !isNaN(value) && Math.abs(value - firstValue) <= tolerance;
    });
    
    if (!isStuck) return false;
    
    // Additional check: Don't flag sensors where zero values are normal
    const zeroValueSensors = ['rg', 'Precipitation', 'rain_counter', 'rain_intensity_max'];
    
    if (zeroValueSensors.includes(sensorType) && Math.abs(firstValue) < 0.1) {
        return false; // Precipitation sensors reading 0.0mm is normal (no rain)
    }
    
    return true;
}
// Local date/time formatter
const formatDateTime = {
    date: (timestamp: string) => {
        try {
            if (!timestamp) return 'Invalid Date';
            const date = new Date(timestamp);
            if (isNaN(date.getTime())) return 'Invalid Date';
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            });
        } catch {
            return 'Invalid Date';
        }
    },
    time: (timestamp: string) => {
        try {
            const date = new Date(timestamp);
            if (isNaN(date.getTime())) return 'Invalid Time';
            return date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            });
        } catch {
            return 'Invalid Time';
        }
    }
};
watch([
    () => props.measurements,
    () => props.stationInfo
], ([newMeasurements, newStationInfo]) => {
    if (!newMeasurements?.length || !newStationInfo) {
        latestData.value = [];
        connectionStatus.value = 'Unsuccessful';
        return;
    }
    try {
        // Sort by date/time descending
        const sorted = [...newMeasurements].sort((a: any, b: any) => {
            const dateA = new Date(`${a.date}T${a.time}`);
            const dateB = new Date(`${b.date}T${b.time}`);
            return dateB.getTime() - dateA.getTime();
        });
        const now = Date.now();
        // Find any measurement in the last 60 minutes
        const onlineThresholdMinutes = 60;
        const recentMeasurement = (sorted as any[]).find((m: any) => {
            const measurementTime = new Date(`${m.date}T${m.time}`).getTime();
            const diffMinutes = (now - measurementTime) / (1000 * 60);
            return diffMinutes <= onlineThresholdMinutes;
        });
        
        // Check data quality for recent measurements (last 100)
        let dataQualityStatus = 'unknown';
        let invalidDataCount = 0;
        let totalDataCount = 0;
        
        if (sorted.length > 0) {
            const recentMeasurements = sorted.slice(0, 100); // Last 100 measurements
            totalDataCount = recentMeasurements.length;
            
            // Count measurements with validation flags and known invalid values
            invalidDataCount = recentMeasurements.filter((m: any) => {
                // Check the flag field first
                if (m.flag === false) return true;
                
                // Also check for known invalid values that indicate sensor errors
                const value = parseFloat(m.value);
                if (isNaN(value)) return true;
                
                // Common invalid values that indicate sensor issues
                if (value === -999 || value === -999.0 || value === 999 || value === 999.0) return true;
                if (value === -9999 || value === -9999.0 || value === 9999 || value === 9999.0) return true;
                if (value === -32768 || value === -32768.0) return true; // Common sensor error code
                
                return false;
            }).length;
            
            // Check for stuck sensor (always reading same value)
            const isStuckSensor = checkStuckSensor(recentMeasurements, 'temperature'); // Assuming temperature for Zentra
            
            if (totalDataCount > 0) {
                const invalidPercentage = (invalidDataCount / totalDataCount) * 100;
                if (invalidPercentage > 50 || isStuckSensor) {
                    dataQualityStatus = 'erroneous';
                } else if (invalidPercentage > 10) {
                    dataQualityStatus = 'warning';
                } else {
                    dataQualityStatus = 'good';
                }
            }
        }
        
        // Determine status based on three-tier system
        let status = 'Offline';
        let lastUpdated = '';
        if (recentMeasurement) {
            if (dataQualityStatus === 'erroneous') {
                status = 'Online Erroneous Data'; // Station transmitting but data fails validation
            } else {
                status = 'Online'; // Station reporting valid data
            }
            lastUpdated = `${recentMeasurement.date}T${recentMeasurement.time}`;
        } else if ((sorted as any[])[0]) {
            lastUpdated = `${(sorted as any[])[0].date}T${(sorted as any[])[0].time}`;
        } else {
            status = 'Unknown';
        }
        latestData.value = [{
            id: newStationInfo.serial_number,
            name: newStationInfo.name,
            status,
            lastUpdated,
            dataQuality: totalDataCount > 0 ? {
                validCount: totalDataCount - invalidDataCount,
                totalCount: totalDataCount,
                validPercentage: Math.round(((totalDataCount - invalidDataCount) / totalDataCount) * 100)
            } : undefined
        }];
        connectionStatus.value = 'Successful';
    } catch (error) {
        console.error('Error processing measurements:', error);
        latestData.value = [];
        connectionStatus.value = 'Error processing data';
    }
}, { immediate: true });
</script>

<style scoped>
.status-indicator-container {
    margin-left: 8px;
    flex: none;
}

.status-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    min-width: 12px;
    min-height: 12px;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-online {
    background-color: #28a745;
}

.status-online-erroneous-data {
    background-color: #ffc107;
}

.status-offline {
    background-color: #dc2626;
}

.status-unknown {
    background-color: #6c757d;
}
</style>