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
            console.log('Fetching stations...')
            
            const [stationsResponse, healthLogsResponse] = await Promise.all([
                axios.get('/stations/'),
                axios.get('/station-health-logs/')
            ])

            const stationsData = (stationsResponse.data || []).filter((station: any) => 
                station.brand_name === '3D_Paws' || 
                station.brand_name === 'Allmeteo' ||
                station.brand_name === 'Zentra'
            )

            // Create a map of latest health logs by station ID
            const healthLogsMap = new Map<number, StationHealthLog>(
                ((healthLogsResponse.data || []) as StationHealthLog[]).map(log => {
                    // Ensure battery status is properly formatted
                    let batteryStatus = log.battery_status
                    
                    // Handle different battery status formats
                    if (typeof batteryStatus === 'number') {
                        batteryStatus = `${batteryStatus}%`
                    } else if (typeof batteryStatus === 'string') {
                        // If it's already a string but doesn't end with %, add it
                        if (!batteryStatus.endsWith('%') && batteryStatus !== 'Unknown') {
                            batteryStatus = `${batteryStatus}%`
                        }
                    }
                    
                    return [
                        log.station, // Use station instead of id
                        { 
                            ...log,
                            battery_status: batteryStatus || 'Unknown'
                        }
                    ]
                })
            )

            stations.value = await Promise.all(stationsData.map(async (station: any) => {
                const healthLog = healthLogsMap.get(station.id)
                
                // Determine status based on battery status and format
                let status = 'Offline'
                let batteryStatus = healthLog?.battery_status || 'Unknown'
                
                // Ensure consistent battery status format
                if (batteryStatus !== 'Unknown' && !batteryStatus.endsWith('%')) {
                    batteryStatus = `${batteryStatus}%`
                }
                
                // Check if battery status is valid and not zero or very low
                if (batteryStatus && 
                    batteryStatus !== 'Unknown' && 
                    batteryStatus !== '0%' && 
                    batteryStatus !== '0.0%' &&
                    !batteryStatus.startsWith('0.')) {
                    status = 'Online'
                }

                return {
                    id: station.serial_number || station.id.toString(),
                    name: station.name,
                    location: station.location || 'Unknown',
                    lastUpdate: station.last_updated_at,
                    status: status,
                    latestHealth: {
                        connectivity_status: healthLog?.connectivity_status || 'No Data',
                        battery_status: batteryStatus,
                        created_at: healthLog?.created_at || null,
                        station: station.id
                    },
                    parameters: {}
                }
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