import { defineStore } from 'pinia';
import axios from 'axios';

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
    async fetchStationData(forceRefresh = false) {
      if (!this.selectedBrand || !this.selectedSensorType) {
        console.warn("Missing brand or sensor type, cannot fetch data");
        return;
      }

      this.error = null;
      this.isLoading = true;

      console.log('Fetching station data with params:', {
        page: this.currentPage,
        pageSize: this.pageSize,
        brand: this.selectedBrand,
        sensorType: this.selectedSensorType,
      });

      try {
        // First fetch overview data
        const overviewResponse = await axios.get('/measurements/station_overview/', {
          params: {
            brand: this.selectedBrand,
            sensor_type: this.selectedSensorType,
            page: this.currentPage,
            page_size: 6,
            latest: true,
            _t: forceRefresh ? new Date().getTime() : undefined
          }
        });

        // Process overview data
        if (overviewResponse.data && overviewResponse.data.stations) {
          this.totalPages = overviewResponse.data.total_pages || 1;
          
          console.log('Station overview data fetched. Total stations:', overviewResponse.data.total, 'Total pages:', this.totalPages);

          // Get station IDs from the overview response
          const stationIds = overviewResponse.data.stations.map((station: Station) => station.id);
          
          // Only fetch historical data if we have station IDs and sensor type
          let historicalData: HistoricalData = {};
          if (stationIds.length > 0 && this.selectedSensorType) {
            console.log('Fetching history data for station_ids:', stationIds, 'and sensor_type:', this.selectedSensorType);
            
            const historyResponse = await axios.get('/measurements/history/', {
              params: {
                station_ids: stationIds.join(','),
                sensor_type: this.selectedSensorType,
                hours: 12,
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
          'battery': 'Battery',
          'humidity': 'Humidity',
          'irradiation': 'Irradiation',
          'irr_max': 'Irradiation (Max)',
          'pressure': 'Pressure',
          'temperature': 'Temperature',
          'temperature_max': 'Temperature (Max)',
          'temperature_min': 'Temperature (Min)',
          'rain_counter': 'Rain Counter',
          'rain_intensity_max': 'Rain Intensity (Max)'
        }
      };

      return sensorConfigs[this.selectedBrand]?.[sensorType] || sensorType;
    }
  }
}); 