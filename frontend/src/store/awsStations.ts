import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useStationData } from '@/composables/useStationData'
import type { AWSStation } from '@/core/data/aws'

export const useAWSStationsStore = defineStore('awsStations', () => {
  const stations = ref<AWSStation[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)
  const connectionStatus = ref<string>('Unsuccessful')
  let refreshInterval: number | undefined

  // Optionally use stationData composable for extra methods
  const { getStationStatus } = useStationData()

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
      const status = await getStationStatus(Number(station.id))
      connectionStatus.value = 'Successful'
      return status
    } catch (err) {
      connectionStatus.value = 'Error processing data'
      return 'Offline'
    }
  }

  const fetchStations = async () => {
    try {
      loading.value = true
      const [healthLogsResponse, stationsResponse] = await Promise.all([
        axios.get('/station-health-logs/', {
          params: {
            limit: 100,
            ordering: '-created_at'
          }
        }),
        axios.get('/stations/')
      ])
      const healthLogsMap = new Map<number, any>()
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
    } catch (err) {
      error.value = 'Failed to fetch stations. Please try again later.'
    } finally {
      loading.value = false
    }
  }

  // Only fetch once per app lifecycle
  let initialized = false
  let initPromise: Promise<void> | null = null
  const init = async () => {
    if (initialized) return
    if (initPromise) return initPromise
    initPromise = (async () => {
      await fetchStations()
      refreshInterval = window.setInterval(fetchStations, 300000)
      initialized = true
      initPromise = null
    })()
    return initPromise
  }

  // Optionally, clear interval on unmount (if needed in SSR or hot reload)
  const cleanup = () => {
    if (refreshInterval) clearInterval(refreshInterval)
    initialized = false
  }

  return {
    stations,
    loading,
    error,
    fetchStations,
    stationStatus,
    connectionStatus,
    checkStationStatus,
    init,
    cleanup
  }
}) 