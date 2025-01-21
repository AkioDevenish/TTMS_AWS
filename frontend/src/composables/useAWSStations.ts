import { ref, computed } from 'vue'
import { AWSStation } from '@/core/data/aws'
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

export function useAWSStations() {
    const stations = ref<AWSStation[]>([])
    const loading = ref(true)
    const error = ref<string | null>(null)
    const { measurements, stationInfo, getLatestMeasurement, fetchStationData, getStationStatus } = useStationData()

    const stationStatus = computed(() => {
        const total = stations.value.length
        const offline = stations.value.filter(s => s.status === 'Offline').length
        const maintenance = stations.value.filter(s => s.status === 'Maintenance').length
        const online = total - offline - maintenance
        
        return {
            total,
            online,
            offline,
            maintenance,
            uptime: total ? ((online / total) * 100).toFixed(1) : '0'
        }
    })

    const checkStationStatus = async (station: AWSStation) => {
        return await getStationStatus(Number(station.id));
    }

    const fetchStations = async () => {
        try {
            loading.value = true
            const response = await axios.get('http://127.0.0.1:8000/stations/')
            const stationsData = response.data.filter((station: any) => 
                station.brand_name.toLowerCase() === 'aws'
            )

            stations.value = await Promise.all(stationsData.map(async (station: any) => ({
                id: station.serial_number,
                name: station.name,
                location: station.location || 'Unknown',
                lastUpdate: null,
                status: await checkStationStatus(station),
                parameters: {}
            })))
        } catch (err) {
            console.error('Failed to fetch AWS stations:', err)
            error.value = 'Failed to fetch stations'
        } finally {
            loading.value = false
        }
    }

    return {
        stations,
        loading,
        error,
        stationStatus,
        fetchStations
    }
} 