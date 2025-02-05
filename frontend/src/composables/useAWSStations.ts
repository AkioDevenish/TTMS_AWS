import { ref, computed, onMounted, onUnmounted } from 'vue'
import { AWSStation } from '@/core/data/aws'
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

export function useAWSStations() {
    const stations = ref<AWSStation[]>([])
    const loading = ref(true)
    const error = ref<string | null>(null)
    const { measurements, stationInfo, getLatestMeasurement, fetchStationData, getStationStatus } = useStationData()
    const connectionStatus = ref<string>('Unsuccessful')
    let refreshInterval: number

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
        try {
            console.log('Checking status for station:', station)
            const status = await getStationStatus(Number(station.id))
            console.log('Status received:', status)
            connectionStatus.value = 'Successful'
            return status
        } catch (err) {
            console.error('Error in checkStationStatus:', err)
            connectionStatus.value = 'Error processing data'
            return 'Offline'
        }
    }

    const fetchStations = async () => {
        try {
            loading.value = true
            console.log('Fetching stations...')
            const response = await axios.get('/stations/')
            console.log('All stations:', response.data)
            
            const stationsData = response.data.filter((station: any) => 
                station.brand_name === '3D_Paws' || 
                station.brand_name === 'Allmeteo' ||
                station.brand_name === 'Zentra'
            )
            console.log('Weather stations filtered:', stationsData)

            stations.value = await Promise.all(stationsData.map(async (station: any) => {
                console.log('Processing station:', station)
                const status = await checkStationStatus({
                    id: station.id.toString(),
                    name: station.name,
                    location: station.location || 'Unknown',
                    lastUpdate: null,
                    status: 'NoData',
                    parameters: {}
                })

                const stationData = {
                    id: station.serial_number,
                    name: station.name,
                    location: station.location || 'Unknown',
                    lastUpdate: station.last_updated_at,
                    status: status,
                    parameters: {}
                }
                console.log('Processed station data:', stationData)
                return stationData
            }))
            console.log('Final stations array:', stations.value)
        } catch (err) {
            console.error('Failed to fetch AWS stations:', err)
            error.value = 'Failed to fetch stations'
        } finally {
            loading.value = false
        }
    }

    // Auto refresh stations every minute
    onMounted(() => {
        fetchStations()
        refreshInterval = setInterval(() => {
            fetchStations()
        }, 60000)
    })

    onUnmounted(() => {
        clearInterval(refreshInterval)
    })

    return {
        stations,
        loading,
        error,
        stationStatus,
        fetchStations,
        connectionStatus
    }
} 