import { defineStore } from 'pinia';
import axios from 'axios';

export interface InactiveSensor {
    station_name: string;
    brand_name: string;
    sensor_type: string;
    lastReading: string | null;
    status: string;
}

interface InactiveSensorsState {
    sensors: InactiveSensor[];
    isLoading: boolean;
    error: string | null;
    currentPage: number;
    totalPages: number;
    selectedBrand: string;
    pageSize: number;
    availableBrands: string[];
}

export const useInactiveSensorsStore = defineStore('inactiveSensors', {
    state: (): InactiveSensorsState => ({
        sensors: [],
        isLoading: false,
        error: null,
        currentPage: 1,
        totalPages: 1,
        selectedBrand: '', // Initial brand will be set by the component
        pageSize: 5, // Matching the component's current page size
        availableBrands: [],
    }),

    actions: {
        async fetchInactiveSensors(forceRefresh = false) {
            this.isLoading = true;
            this.error = null;
            console.log('Store: fetchInactiveSensors called with brand:', this.selectedBrand, 'page:', this.currentPage);
            try {
                const response = await axios.get('/measurements/inactive_sensors/', {
                    params: {
                        page: this.currentPage,
                        page_size: this.pageSize,
                        brand: this.selectedBrand || undefined, // Send brand only if selected
                        _t: forceRefresh ? new Date().getTime() : undefined // Cache busting
                    }
                });

                console.log('Store: Inactive sensors API response:', response.data);

                if (response.data && response.data.results) {
                    this.sensors = response.data.results.map((sensor: any) => ({
                        station_name: sensor.station_name,
                        brand_name: sensor.brand_name,
                        sensor_type: sensor.sensor_type,
                        lastReading: sensor.last_reading,
                        status: sensor.status
                    }));
                    this.totalPages = response.data.total_pages || 1;
                     if (!this.selectedBrand && response.data.available_brands && response.data.available_brands.length > 0) {
                        this.selectedBrand = response.data.available_brands[0];
                    }
                     // Store available brands from the backend response
                    // Move this outside the results check

                     console.log('Store: State updated - sensors count:', this.sensors.length, 'availableBrands count:', this.availableBrands.length);

                } else {
                    this.sensors = [];
                    this.totalPages = 1;
                     // this.availableBrands = []; // Don't clear brands here
                     console.log('Store: No data received, sensors and totalPages cleared.');
                }

                 // Always update available brands if present in the response
                if (response.data && response.data.available_brands) {
                     this.availableBrands = response.data.available_brands;
                }

            } catch (error: any) {
                console.error('Store: Error fetching inactive sensor data:', error);
                this.error = error.message || 'Failed to fetch inactive sensors';
                this.sensors = [];
                this.totalPages = 1;
                 this.availableBrands = []; // Clear brands on error
                 console.log('Store: Fetch error, state cleared.');
            } finally {
                this.isLoading = false;
                console.log('Store: isLoading set to false.');
            }
        },

        setBrand(brand: string) {
            this.selectedBrand = brand;
            this.currentPage = 1;
            this.fetchInactiveSensors(true); // Force refresh on brand change
        },

        setPage(page: number) {
            this.currentPage = page;
            this.fetchInactiveSensors(); // Fetch data for the new page
        },

        // This action might be useful if we need to get unique brands from the store later
        // async fetchUniqueBrands() {
        //     // This would require a new backend endpoint to just get unique brands
        // }
    },
}); 