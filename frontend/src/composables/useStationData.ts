import { ref, computed } from 'vue';
import axios from 'axios';

interface StationInfo {
  id: number;
  name: string;
  serial_number: string;
  brand_name: string;
  [key: string]: any;
}

interface Measurement {
  date: string;
  time: string;
  value: number;
  sensor_type: string;
  status: string;
  station_id: number;
}

export function useStationData() {
  const measurements = ref<Measurement[]>([]);
  const stationInfo = ref<StationInfo | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const fetchStationData = async (stationId: number) => {
    if (!stationId) return;

    isLoading.value = true;
    error.value = null;

    try {
      const [stationResponse, measurementsResponse] = await Promise.all([
        axios.get(`/stations/${stationId}/`),
        axios.get(`/measurements/by_station/?station_id=${stationId}`),
        axios.get('/measurements/', {
          params: {
            station_id: stationId,
            page: 1
          }
        })
      ]);


      stationInfo.value = stationResponse.data;
      measurements.value = measurementsResponse.data || [];
    } catch (err: any) {
      error.value = err.message;
      measurements.value = [];
      stationInfo.value = null;
    } finally {
      isLoading.value = false;
    }
  };

  const getLast24HoursMeasurements = computed(() => {
    if (!measurements.value?.length) return [];

    const now = Date.now();
    const oneDayAgo = now - (24 * 60 * 60 * 1000);

    return measurements.value
      .filter(measurement => {
        const measurementTime = new Date(`${measurement.date}T${measurement.time}`).getTime();
        return measurementTime >= oneDayAgo;
      })
      .sort((a, b) => {
        const dateA = new Date(`${a.date}T${a.time}`).getTime();
        const dateB = new Date(`${b.date}T${b.time}`).getTime();
        return dateA - dateB;
      });
  });

  const getLatestMeasurement = computed(() => {
    if (!measurements.value?.length) return null;

    return [...measurements.value].sort((a, b) => {
      const dateA = new Date(`${a.date}T${a.time}`);
      const dateB = new Date(`${b.date}T${b.time}`);
      return dateB.getTime() - dateA.getTime();
    })[0];
  });

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

  const getStationStatus = async (stationId: number) => {
    try {
      const response = await axios.get(
        `/measurements/by_station/?station_id=${stationId}&limit=1`
      );

      const latestMeasurement = response.data[0];
      if (!latestMeasurement) return 'Offline';

      // Check for invalid measurements
      const hasInvalidValues = Object.values(latestMeasurement)
        .filter((value): value is number => typeof value === 'number')
        .every((value) => value <= -1 || value === 0);

      if (hasInvalidValues) return 'Offline';

      // Check measurement time
      const measurementTime = new Date(`${latestMeasurement.date}T${latestMeasurement.time}`);
      const timeDiff = Date.now() - measurementTime.getTime();
      if (timeDiff > 30 * 60 * 1000) return 'Offline'; // 30 minutes

      return latestMeasurement.status === 'Successful' ? 'Online' : 'Offline';
    } catch (err) {
      console.error('Error getting station status:', err);
      return 'Offline';
    }
  };

  // Add new methods for filtered data fetching
  const fetchFilteredStationData = async (stationId: number, options: {
    sensorType?: string;
    startDate?: string;
    endDate?: string;
    limit?: number;
  }) => {
    if (!stationId) return;

    isLoading.value = true;
    error.value = null;

    try {
      // Build query parameters
      const params = new URLSearchParams();
      params.append('station_id', stationId.toString());
      
      if (options.sensorType) {
        params.append('sensor_type', options.sensorType);
      }
      
      if (options.startDate) {
        params.append('start_date', options.startDate);
      }
      
      if (options.endDate) {
        params.append('end_date', options.endDate);
      }
      
      if (options.limit) {
        params.append('limit', options.limit.toString());
      }

      const [stationResponse, measurementsResponse] = await Promise.all([
        axios.get(`/stations/${stationId}/`),
        axios.get('/measurements/', {
          params: {
            station_id: stationId,
            page: 1
          }
        })
      ]);

      stationInfo.value = stationResponse.data;
      measurements.value = measurementsResponse.data || [];
    } catch (err: any) {
      error.value = err.message;
      measurements.value = [];
      stationInfo.value = null;
    } finally {
      isLoading.value = false;
    }
  };

  // Method to fetch only the last 24 hours of data for a specific sensor
  const fetchLast24HoursSensorData = async (stationId: number, sensorType: string) => {
    // Calculate date 24 hours ago
    const now = new Date();
    const yesterday = new Date(now.getTime() - (24 * 60 * 60 * 1000));
    const yesterdayStr = yesterday.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    
    await fetchFilteredStationData(stationId, {
      sensorType,
      startDate: yesterdayStr
    });
  };

  return {
    measurements,
    stationInfo,
    isLoading,
    error,
    fetchStationData,
    getLast24HoursMeasurements,
    getLatestMeasurement,
    formatDateTime,
    getStationStatus,
    fetchFilteredStationData,
    fetchLast24HoursSensorData
  };
} 