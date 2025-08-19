import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '../plugins/axios'

export const useStationStore = defineStore('station', () => {
  const stations = ref<any[]>([])
  const loading = ref(false)
  const error = ref<any>(null)

  // Fetch all stations
  const fetchStations = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/stations/?include_decommissioned=true')
      stations.value = response.data || []
    } catch (err: any) {
      console.error('Error fetching stations:', err)
      error.value = err
    } finally {
      loading.value = false
    }
  }

  // Fetch a single station
  const fetchStation = async (stationId: number | string) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`/api/stations/${stationId}/`)
      return response.data
    } catch (err: any) {
      error.value = err
      console.error('Error fetching station:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  // Create a new station
  const createStation = async (stationData: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/api/stations/', stationData)
      if (response.status === 201) {
        stations.value.push(response.data)
        return response.data
      }
      return null
    } catch (err: any) {
      error.value = err
      console.error('Error creating station:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  // Update station
  const updateStation = async (stationId: number, stationData: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch(`/api/stations/${stationId}/`, stationData)
      if (response.status === 200) {
        const index = stations.value.findIndex(station => station.id === stationId)
        if (index !== -1) {
          stations.value[index] = { ...stations.value[index], ...response.data }
        }
        return response.data
      }
      return null
    } catch (err: any) {
      error.value = err
      console.error('Error updating station:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  // Decommission station
  const decommissionStation = async (stationId: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post(`/api/stations/${stationId}/decommission/`)
      if (response.status === 200) {
        const index = stations.value.findIndex(station => station.id === stationId)
        if (index !== -1) {
          // Update the station in the local array
          stations.value[index] = { ...stations.value[index], ...response.data.station }
          // Force reactivity update
          stations.value = [...stations.value]
        }
        return true
      }
      return false
    } catch (err: any) {
      error.value = err
      console.error('Error decommissioning station:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Reactivate station
  const reactivateStation = async (stationId: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post(`/api/stations/${stationId}/reactivate/`)
      if (response.status === 200) {
        const index = stations.value.findIndex(station => station.id === stationId)
        if (index !== -1) {
          // Update the station in the local array
          stations.value[index] = { ...stations.value[index], ...response.data.station }
          // Force reactivity update
          stations.value = [...stations.value]
        }
        return true
      }
      return false
    } catch (err: any) {
      error.value = err
      console.error('Error reactivating station:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Get stations by brand
  const getStationsByBrand = computed(() => {
    return (brandName: string) => {
      return stations.value.filter(station => 
        station.brand?.name === brandName || station.brand_name === brandName
      )
    }
  })

  // Get station by ID
  const getStationById = computed(() => {
    return (id: number) => {
      return stations.value.find(station => station.id === id)
    }
  })

  return {
    stations,
    loading,
    error,
    fetchStations,
    fetchStation,
    createStation,
    updateStation,
    decommissionStation,
    reactivateStation,
    getStationsByBrand,
    getStationById
  }
}) 