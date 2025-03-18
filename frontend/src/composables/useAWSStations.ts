import { ref, computed, onMounted, onUnmounted } from 'vue'
import { AWSStation } from '@/core/data/aws'
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

interface StationHealthLog {
    station: number;
    battery_status: string;
    connectivity_status: string;
    created_at: string | null;
}

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
            console.log('Fetching AWS stations...')
            
            const [healthLogsResponse, stationsResponse] = await Promise.all([
                axios.get('/station-health-logs/'),
                axios.get('/stations/')
            ])
            
            const healthLogsMap = new Map<number, any>()
            
            // Process health logs
            if (healthLogsResponse.data && Array.isArray(healthLogsResponse.data.results)) {
                healthLogsResponse.data.results.forEach((log: any) => {
                    if (!healthLogsMap.has(log.station) || 
                        new Date(log.created_at) > new Date(healthLogsMap.get(log.station).created_at)) {
                        healthLogsMap.set(log.station, log)
                    }
                })
            }

            const stationsData = stationsResponse.data || []
            
            stations.value = stationsData.map((station: any) => {
                const healthLog = healthLogsMap.get(station.id)
                
                let status = 'Offline'
                let batteryStatus = 'Unknown'
                let connectivityStatus = 'No Data'
                
                if (healthLog) {
                    batteryStatus = healthLog.battery_status || 'Unknown'
                    connectivityStatus = healthLog.connectivity_status || 'No Data'
                    
                    // Mark as online if connectivity is Excellent
                    if (connectivityStatus === 'Excellent') {
                        status = 'Online'
                    }
                }
                
                return {
                    id: station.id.toString(),
                    name: station.name,
                    location: station.location || 'Trinidad and Tobago',
                    lastUpdate: healthLog?.created_at || null,
                    status: status,
                    latestHealth: {
                        connectivity_status: connectivityStatus,
                        battery_status: batteryStatus,
                        created_at: healthLog?.created_at || null,
                        station: station.id
                    },
                    parameters: {}
                }
            })
            
            console.log('Final AWS stations array:', stations.value)
        } catch (err) {
            console.error('Failed to fetch AWS stations:', err)
            error.value = 'Failed to fetch stations'
        } finally {
            loading.value = false
        }
    }

    onMounted(() => {
        fetchStations()
        refreshInterval = setInterval(fetchStations, 300000) as unknown as number
    })

    onUnmounted(() => {
        if (refreshInterval) clearInterval(refreshInterval)
    })

    return {
        stations,
        loading,
        error,
        fetchStations,
        stationStatus,
        connectionStatus,
        
    }
} 