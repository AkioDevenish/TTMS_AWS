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

  /**
   * Fetch measurements for one or more stations using the /measurements/history/ endpoint.
   * @param stationIds - A single station ID or an array of station IDs
   * @param sensorType - The sensor type to fetch (e.g., 'bt1')
   * @param hours - How many hours back to fetch (default 12)
   */
  const fetchStationData = async (stationIds: number | number[], sensorType: string = '', hours: number = 12) => {
    if (!stationIds || (Array.isArray(stationIds) && stationIds.length === 0)) {
      console.warn('No station IDs provided to fetchStationData');
      return;
    }
    if (!sensorType) {
      console.warn('No sensor type provided to fetchStationData');
      return;
    }
    console.log('Fetching station data with params:', { stationIds, sensorType, hours });
    isLoading.value = true;
    error.value = null;
    try {
      let idsParam = Array.isArray(stationIds) ? stationIds.join(',') : stationIds.toString();
      let allMeasurements: any[] = [];
      // If sensorType is a comma-separated list, fetch each and merge
      const sensorTypes = sensorType.split(',').map(s => s.trim()).filter(Boolean);
      console.log('Processing sensor types:', sensorTypes);
      
      for (const sType of sensorTypes) {
        const params: any = {
          station_ids: idsParam,
          hours,
          sensor_type: sType
        };
        console.log('Fetching measurements for sensor type:', sType, 'with params:', params);
        const response = await axios.get('/measurements/history/', { params });
        console.log('Raw API response for sensor type', sType, ':', response.data);
        
        if (response.data && Array.isArray(response.data.measurements)) {
          const processedMeasurements = response.data.measurements.map((m: any) => ({
            ...m,
            value: parseFloat(m.value),
            date: m.date,
            time: m.time,
            sensor_type: m.sensor_type,
            station_id: m.station_id
          }));
          console.log('Processed measurements for sensor type', sType, ':', processedMeasurements);
          allMeasurements.push(...processedMeasurements);
        }
      }
      console.log('All merged measurements:', allMeasurements);
      measurements.value = allMeasurements;
      
      // Optionally, fetch station info for the first station (if single)
      if (!Array.isArray(stationIds) || stationIds.length === 1) {
        const id = Array.isArray(stationIds) ? stationIds[0] : stationIds;
        console.log('Fetching station info for ID:', id);
        const stationResponse = await axios.get(`/stations/${id}/`);
        console.log('Station info response:', stationResponse.data);
        stationInfo.value = stationResponse.data;
      } else {
        stationInfo.value = null;
      }
    } catch (err: any) {
      console.error('Error fetching station data:', err);
      error.value = err.message;
      measurements.value = [];
      stationInfo.value = null;
    } finally {
      isLoading.value = false;
    }
  };

  const getLast24HoursMeasurements = computed(() => {
    if (!measurements.value?.length) {
      console.log('No measurements available for last 24 hours calculation');
      return [];
    }

    const now = Date.now();
    const oneDayAgo = now - (24 * 60 * 60 * 1000);

    const filteredMeasurements = measurements.value
      .filter(measurement => {
        const measurementTime = new Date(`${measurement.date}T${measurement.time}`).getTime();
        return measurementTime >= oneDayAgo;
      })
      .sort((a, b) => {
        const dateA = new Date(`${a.date}T${a.time}`).getTime();
        const dateB = new Date(`${b.date}T${b.time}`).getTime();
        return dateA - dateB;
      });

    console.log('Filtered 24h measurements:', filteredMeasurements);
    return filteredMeasurements;
  });

  const getLatestMeasurement = computed(() => {
    if (!measurements.value?.length) {
      console.log('No measurements available for latest measurement calculation');
      return null;
    }

    const latest = [...measurements.value].sort((a, b) => {
      const dateA = new Date(`${a.date}T${a.time}`);
      const dateB = new Date(`${b.date}T${b.time}`);
      return dateB.getTime() - dateA.getTime();
    })[0];
    console.log('Latest measurement:', latest);
    return latest;
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