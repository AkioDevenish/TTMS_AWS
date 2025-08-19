import { defineStore } from 'pinia';
import axios from '../plugins/axios';

interface StationMeasurement {
  value: number;
  date: string;
  time: string;
  status: string;
}

interface Station {
  id: number;
  name: string;
  location: string;
  brand: string;
  sensor_unit: string;
  latest_measurement: StationMeasurement | null;
  chartData?: any[];
}

interface StationOverviewState {
  stations: Station[];
  isLoading: boolean;
  error: string | null;
  currentPage: number;
  totalPages: number;
  selectedBrand: string;
  selectedSensorType: string;
  pageSize: number;
}

interface HistoricalData {
  [key: number]: Array<{
    x: number;
    y: number;
  }>;
}

interface SensorConfig {
  [key: string]: {
    [key: string]: string;
  };
}

export const useStationOverviewStore = defineStore('stationOverview', {
  state: (): StationOverviewState => ({
    stations: [],
    isLoading: false,
    error: null,
    currentPage: 1,
    totalPages: 1,
    selectedBrand: '3D_Paws',
    selectedSensorType: 'bt1',
    pageSize: 6,
  }),

  actions: {
    // Helper function to check if a value is invalid
    isInvalidValue(value: any): boolean {
      const numValue = parseFloat(value);
      return isNaN(numValue) || 
        numValue === -999 || numValue === -999.0 || numValue === 999 || numValue === 999.0 ||
        numValue === -9999 || numValue === -9999.0 || numValue === 9999 || numValue === 9999.0 ||
        numValue === -32768 || numValue === -32768.0 ||
        numValue === 0; // 0.0°C is suspicious for temperature readings
    },

    // Helper function to determine station status priority
    getStationStatusPriority(station: any): number {
      // FIRST: Check if sensor is actually communicating (not offline)
      if (!station.latest_measurement) {
        return 1; // Offline - no recent data
      }

      // Check if the last update is recent (within last 2 hours = online, beyond = offline)
      const lastUpdate = new Date(`${station.latest_measurement.date}T${station.latest_measurement.time}`);
      const now = new Date();
      const hoursSinceUpdate = (now.getTime() - lastUpdate.getTime()) / (1000 * 60 * 60);
      
      if (hoursSinceUpdate > 2) {
        console.log(`${station.name}: Last update ${hoursSinceUpdate.toFixed(1)} hours ago -> Offline`);
        return 1; // Offline - no recent communication
      }
      
      // SPECIAL HANDLING FOR UV SENSORS - if it's 0.0W/m² during daytime, check if it's actually offline
      const sensorType = this.selectedSensorType;
      const uvSensors = ['su1', 'Downwelling Ultraviolet', 'uv', 'ultraviolet'];
      
      if (uvSensors.includes(sensorType)) {
        const value = parseFloat(station.latest_measurement?.value);
        if (value === 0) {
          // Check if it's daytime (UV should be > 0 during day)
          const hour = now.getHours();
          const isDaytime = hour >= 6 && hour <= 18; // 6 AM to 6 PM
          
          if (isDaytime) {
            console.log(`${station.name}: UV sensor reading 0.0W/m² during daytime - checking if offline`);
            // If UV is 0 during day and hasn't updated recently, it's likely offline
            if (hoursSinceUpdate > 0.1) { // More strict for UV sensors - 6 minutes
              console.log(`${station.name}: UV sensor offline during daytime -> Offline`);
              return 1; // Offline
            }
          }
        }
      }

      // SECOND: If sensor is communicating, check data quality
      if (station.chartData && station.chartData[0] && station.chartData[0].data && station.chartData[0].data.length > 0) {
        // Station has data and is communicating - now determine if data is valid
        const isInvalidValue = this.isInvalidValue(station.latest_measurement?.value);
        
        // SPECIAL HANDLING FOR BATTERY SENSORS
        const sensorType = this.selectedSensorType;
        const batterySensors = ['bpc', 'Battery Percent', 'battery_percent', 'battery'];
        const cellSignalSensors = ['css', 'Cell Signal Strength', 'cell_signal', 'signal_strength'];
        
        if (batterySensors.includes(sensorType)) {
          const value = parseFloat(station.latest_measurement?.value);
          if (value === 0) {
            return 1; // Critical Battery = highest priority (Offline)
          } else if (value <= 10) {
            return 2; // Low Battery = second priority (Warning)
          } else if (value <= 25) {
            return 2; // Battery Warning = second priority (Warning)
          } else {
            return 3; // Healthy Battery = lowest priority (Online)
          }
        }
        
        if (cellSignalSensors.includes(sensorType)) {
          const value = parseFloat(station.latest_measurement?.value);
          if (value >= 80) {
            return 3; // Excellent Signal = lowest priority (Online)
          } else if (value >= 60) {
            return 3; // Good Signal = lowest priority (Online)
          } else if (value >= 40) {
            return 2; // Fair Signal = second priority (Warning)
          } else if (value >= 20) {
            return 2; // Poor Signal = second priority (Warning)
          } else {
            return 1; // Weak Signal = highest priority (Offline)
          }
        }
        
        // Check if sensor is stuck (always reading same value) - but NOT for battery/cell signal sensors
        const isStuckSensor = this.checkStuckSensor(station);
        
        if (isInvalidValue || isStuckSensor) {
          return 2; // Online Erroneous Data
        } else {
          return 3; // Online
        }
      }
      
      // Fallback: if we have some measurement but no chart data, still consider online
      return 3; // Online
    },

    // Function to check if a sensor is stuck (always reading the same value)
    checkStuckSensor(station: any): boolean {
      if (!station.chartData || !station.chartData[0] || !station.chartData[0].data || station.chartData[0].data.length < 5) {
        return false; // Need at least 5 data points to determine if stuck
      }
      
      const dataPoints = station.chartData[0].data;
      const values = dataPoints.map((point: any) => point.y);
      
      // Check if all values are within 0.1 tolerance of the first value
      const firstValue = values[0];
      const tolerance = 0.1;
      
      for (let i = 1; i < values.length; i++) {
        if (Math.abs(values[i] - firstValue) > tolerance) {
          return false; // Sensor is not stuck
        }
      }
      
      // CRITICAL FIX: Battery sensors should NOT be flagged as stuck
      const sensorType = this.selectedSensorType;
      const batterySensors = ['bpc', 'Battery Percent', 'battery_percent', 'battery'];
      
      if (batterySensors.includes(sensorType)) {
        console.log(`${station.name}: Battery sensor detected - steady readings are GOOD, not stuck`);
        return false; // Battery sensors with steady readings are healthy
      }
      
      // Additional check: Don't flag sensors where zero values are normal
      const zeroValueSensors = ['rg', 'Precipitation', 'rain_counter', 'rain_intensity_max'];
      
      // For solar radiation sensors, check if it's during daylight hours
      if (sensorType === 'sv1' || sensorType === 'si1' || sensorType === 'su1' || sensorType === 'Solar Radiation') {
        const now = new Date();
        const hour = now.getHours();
        const isDaytime = hour >= 6 && hour <= 18; // 6 AM to 6 PM
        
        // If it's daytime and all values are 0.0, that's suspicious
        if (isDaytime && Math.abs(firstValue) < 0.1) {
          return true; // Sensor stuck at 0.0 during daytime = suspicious
        }
        
        // If it's nighttime and all values are 0.0, that's normal
        if (!isDaytime && Math.abs(firstValue) < 0.1) {
          return false; // Normal for solar sensors at night
        }
      }
      
      if (zeroValueSensors.includes(sensorType) && Math.abs(firstValue) < 0.1) {
        return false; // Precipitation sensors reading 0.0mm is normal (no rain)
      }
      
      return true; // All values are the same, sensor is stuck
    },

    async fetchStationData(forceRefresh = false) {
      if (!this.selectedBrand || !this.selectedSensorType) {
        console.warn("Missing brand or sensor type, cannot fetch data");
        return;
      }

      this.error = null;
      this.isLoading = true;

      console.log('Fetching station data with params:', {
        brand: this.selectedBrand,
        sensorType: this.selectedSensorType,
      });

      try {
        // Fetch ALL stations for this brand (no pagination) to enable global sorting
        const overviewResponse = await axios.get('/api/measurements/station_overview/', {
          params: {
            brand: this.selectedBrand,
            sensor_type: this.selectedSensorType,
            page: 1,
            page_size: 1000, // Large number to get all stations
            latest: true,
            _t: forceRefresh ? new Date().getTime() : undefined
          }
        });

        // Process overview data
        if (overviewResponse.data && overviewResponse.data.stations) {
          console.log('All stations fetched. Total stations:', overviewResponse.data.stations.length);

          // Get station IDs from the overview response
          const stationIds = overviewResponse.data.stations.map((station: Station) => station.id);
          
          // Only fetch historical data if we have station IDs and sensor type
          let historicalData: HistoricalData = {};
          if (stationIds.length > 0 && this.selectedSensorType) {
            console.log('Fetching history data for station_ids:', stationIds, 'and sensor_type:', this.selectedSensorType);
            
            const historyResponse = await axios.get('/api/measurements/history/', {
              params: {
                station_ids: stationIds.join(','),
                sensor_type: this.selectedSensorType,
                hours: 12, // Back to 12 hours
                _t: forceRefresh ? new Date().getTime() : undefined
              }
            });

            if (historyResponse.data && historyResponse.data.measurements) {
              historyResponse.data.measurements.forEach((measurement: any) => {
                if (!historicalData[measurement.station_id]) {
                  historicalData[measurement.station_id] = [];
                }
                
                // Create timestamp from separate date and time fields
                const timestamp = new Date(`${measurement.date}T${measurement.time}`).getTime();
                
                historicalData[measurement.station_id].push({
                  x: timestamp,
                  y: parseFloat(measurement.value)
                });
              });

              // Sort data points by timestamp for each station
              Object.keys(historicalData).forEach(stationId => {
                historicalData[parseInt(stationId)].sort((a, b) => a.x - b.x);
              });
            }
          } else {
            console.warn('Skipping history fetch - missing station IDs or sensor type');
          }

          // Combine overview and historical data
          this.stations = overviewResponse.data.stations.map((station: Station) => ({
            ...station,
            chartData: [{
              name: this.getSensorName(this.selectedSensorType),
              data: historicalData[station.id] || []
            }]
          }));

          // Sort stations by status priority AFTER chart data is available
          this.stations.sort((a, b) => {
            const priorityA = this.getStationStatusPriority(a);
            const priorityB = this.getStationStatusPriority(b);
            return priorityA - priorityB;
          });

          // Debug logging to show sorting results
          console.log('Stations sorted by status priority:', this.stations.map(s => ({
            name: s.name,
            priority: this.getStationStatusPriority(s),
            status: this.getStationStatusPriority(s) === 1 ? 'Offline' : 
                   this.getStationStatusPriority(s) === 2 ? 'Online Erroneous Data' : 'Online',
            chartDataLength: s.chartData?.[0]?.data?.length || 0,
            latestValue: s.latest_measurement?.value,
            latestStatus: s.latest_measurement?.status
          })));

          // Special debug for problematic stations
          const problematicStations = ['T14 UTT', 'T17 Guayaguayare', 'T05 Mt. St. Benedict', 'T03 Centeno'];
          problematicStations.forEach(stationName => {
            const station = this.stations.find(s => s.name === stationName);
            if (station) {
              console.log(`${stationName} detailed debug:`, {
                name: station.name,
                latestMeasurement: station.latest_measurement,
                value: station.latest_measurement?.value,
                parsedValue: parseFloat(String(station.latest_measurement?.value || '0')),
                status: station.latest_measurement?.status,
                chartData: station.chartData,
                isInvalidValue: this.isInvalidValue(station.latest_measurement?.value),
                isStuckSensor: this.checkStuckSensor(station),
                priority: this.getStationStatusPriority(station),
                expectedStatus: this.getStationStatusPriority(station) === 1 ? 'Offline' : 
                               this.getStationStatusPriority(station) === 2 ? 'Online Erroneous Data' : 'Online'
              });
            }
          });

          // Calculate total pages based on page size
          this.totalPages = Math.ceil(this.stations.length / this.pageSize);
        }
      } catch (error: unknown) {
        console.error('Error fetching station data:', error);
        this.error = error instanceof Error ? error.message : "Failed to fetch data";
        this.stations = [];
      } finally {
        this.isLoading = false;
      }
    },

    setBrand(brand: string) {
      console.log('Setting brand:', brand);
      this.selectedBrand = brand;
      this.currentPage = 1;
      
      // Auto-set appropriate default sensor type for the brand
      const defaultSensorTypes: Record<string, string> = {
        '3D_Paws': 'bt1',
        'Zentra': 'Air Temperature',
        'Allmeteo': 'temperature',
        'OTT': 'Air Temperature'
      };
      
      const defaultSensorType = defaultSensorTypes[brand];
      if (defaultSensorType && defaultSensorType !== this.selectedSensorType) {
        console.log(`Auto-setting sensor type to: ${defaultSensorType} for brand: ${brand}`);
        this.selectedSensorType = defaultSensorType;
      }
    },

    setSensorType(sensorType: string) {
      console.log('Setting sensor type:', sensorType);
      this.selectedSensorType = sensorType;
      this.currentPage = 1;
    },

    setPage(page: number) {
      this.currentPage = page;
      this.fetchStationData();
    },

    setPageSize(pageSize: number) {
      this.pageSize = pageSize;
      this.currentPage = 1; // Reset to first page when changing page size
      this.fetchStationData();
    },

    getSensorName(sensorType: string): string {
      const sensorConfigs: SensorConfig = {
        '3D_Paws': {
          'bt1': 'Temperature 1',
          'mt1': 'Temperature 2',
          'bp1': 'Pressure',
          'ws': 'Wind Speed',
          'wd': 'Wind Direction',
          'rg': 'Precipitation',
          'sv1': 'Downwelling Visible',
          'si1': 'Downwelling Infrared',
          'su1': 'Downwelling Ultraviolet',
          'bpc': 'Battery Percent',
          'css': 'Cell Signal Strength'
        },
        'Zentra': {
          'Air Temperature': 'Air Temperature',
          'Wind Speed': 'Wind Speed',
          'Solar Radiation': 'Solar Radiation',
          'Precipitation': 'Precipitation',
          'Relative Humidity': 'Relative Humidity',
          'Atmospheric Pressure': 'Atmospheric Pressure'
        },
        'Allmeteo': {
          'wind_ave10': 'Wind Speed (Average)',
          'wind_max10': 'Wind Speed (Max)',
          'wind_min10': 'Wind Speed (Min)',
          'dir_ave10': 'Wind Direction (Average)',
          'dir_max10': 'Wind Direction (Max)',
          'dir_hi10': 'Wind Direction (High)',
          'dir_lo10': 'Wind Direction (Low)',
          'Battery Percent': 'Battery Percent',
          'humidity': 'Humidity',
          'irradiation': 'Irradiation',
          'irr_max': 'Irradiation (Max)',
          'pressure': 'Pressure',
          'temperature': 'Temperature',
          'temperature_max': 'Temperature (Max)',
          'temperature_min': 'Temperature (Min)',
          'rain_counter': 'Rain Counter'
        },
        'OTT': {
          '5 min rain': '5 min Rain',
          'Air Temperature': 'Air Temperature',
          'Barometric Pressure': 'Barometric Pressure',
          'Baro Tendency': 'Baro Tendency',
          'Battery': 'Battery',
          'Daily Rain': 'Daily Rain',
          'Dew Point': 'Dew Point',
          'Gust Direction': 'Gust Direction',
          'Gust Speed': 'Gust Speed',
          'Hours of Sunshine': 'Hours of Sunshine',
          'Maximum Air Temperature': 'Maximum Air Temperature',
          'Minimum Air Temperature': 'Minimum Air Temperature',
          'Relative Humidity': 'Relative Humidity',
          'Solar Radiation Avg': 'Solar Radiation Average',
          'Solar Radiation Total': 'Solar Radiation Total',
          'Wind Dir Average': 'Wind Direction Average',
          'Wind Dir Inst': 'Wind Direction Instantaneous',
          'Wind Speed Average': 'Wind Speed Average',
          'Wind Speed Inst': 'Wind Speed Instantaneous'
        }
      };

      return sensorConfigs[this.selectedBrand]?.[sensorType] || sensorType;
    }
  },

  getters: {
    // Get paginated stations based on current page
    paginatedStations: (state) => {
      const start = (state.currentPage - 1) * state.pageSize;
      const end = start + state.pageSize;
      return state.stations.slice(start, end);
    },

    // Get total count of all stations
    totalStations: (state) => state.stations.length,
  }
}); 