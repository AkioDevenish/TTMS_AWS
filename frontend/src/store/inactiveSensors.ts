import { defineStore } from 'pinia';
import axios from '../plugins/axios';

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
    totalSensors: number;
    hasNext: boolean;
    hasPrevious: boolean;
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
        totalSensors: 0,
        hasNext: false,
        hasPrevious: false,
        selectedBrand: '3D_Paws', // Set default brand to avoid showing all brands initially
        pageSize: 20, // Increased page size to reduce pagination issues
        availableBrands: [],
    }),

    getters: {
        hasRecentData: (state) => {
            return state.sensors.length > 0;
        },

        // Pagination getters
        getPaginationInfo: (state) => {
            return {
                currentPage: state.currentPage,
                pageSize: state.pageSize,
                totalSensors: state.totalSensors,
                totalPages: state.totalPages,
                hasNext: state.hasNext,
                hasPrevious: state.hasPrevious
            };
        },

        getPageRange: (state) => {
            const range = [];
            const start = Math.max(1, state.currentPage - 2);
            const end = Math.min(state.totalPages, state.currentPage + 2);
            
            for (let i = start; i <= end; i++) {
                range.push(i);
            }
            
            return range;
        }
    },

    actions: {
        async fetchInactiveSensors(forceRefresh = false) {
            this.isLoading = true;
            this.error = null;
            console.log('Store: fetchInactiveSensors called with brand:', this.selectedBrand, 'page:', this.currentPage);
            try {
                const response = await axios.get('/api/measurements/inactive_sensors/', {
                    params: {
                        page: this.currentPage,
                        page_size: this.pageSize,
                        brand: this.selectedBrand || undefined, // Send brand only if selected
                        _t: forceRefresh ? new Date().getTime() : undefined // Cache busting
                    }
                });

                console.log('Store: Inactive sensors API response:', response.data);

                if (response.data && response.data.results) {
                    console.log('Store: Raw sensor data from backend:', response.data.results[0]);
                    this.sensors = response.data.results.map((sensor: any) => {
                        const mappedSensor = {
                            station_name: sensor.station_name,
                            brand_name: sensor.brand_name,
                            sensor_type: sensor.sensor_type,
                            lastReading: sensor.last_reading,
                            status: sensor.status
                        };
                        console.log('Store: Mapped sensor:', mappedSensor);
                        return mappedSensor;
                    });
                    
                    // Update pagination info
                    this.currentPage = response.data.page || 1;
                    this.totalPages = response.data.total_pages || 1;
                    this.totalSensors = response.data.total_count || 0;
                    this.hasNext = this.currentPage < this.totalPages;
                    this.hasPrevious = this.currentPage > 1;
                    
                     // Only set selectedBrand if it's empty and we have available brands
                     if (!this.selectedBrand && response.data.available_brands && response.data.available_brands.length > 0) {
                        this.selectedBrand = response.data.available_brands[0];
                    }
                     // Store available brands from the backend response
                     this.availableBrands = response.data.available_brands || [];

                     console.log('Store: State updated - sensors count:', this.sensors.length, 'totalSensors:', this.totalSensors, 'availableBrands count:', this.availableBrands.length);

                } else {
                    this.sensors = [];
                    this.currentPage = 1;
                    this.totalPages = 1;
                    this.totalSensors = 0;
                    this.hasNext = false;
                    this.hasPrevious = false;
                     // this.availableBrands = []; // Don't clear brands here
                     console.log('Store: No data received, sensors and pagination data cleared.');
                }

                 // Always update available brands if present in the response
                if (response.data && response.data.available_brands) {
                     // Always ensure OTT is included
                     if (!response.data.available_brands.includes('OTT')) {
                        response.data.available_brands.push('OTT');
                     }
                     this.availableBrands = response.data.available_brands;
                }

            } catch (error: any) {
                console.error('Store: Error fetching inactive sensor data:', error);
                this.error = error.message || 'Failed to fetch inactive sensors';
                this.sensors = [];
                this.currentPage = 1;
                this.totalPages = 1;
                this.totalSensors = 0;
                this.hasNext = false;
                this.hasPrevious = false;
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

        // Pagination methods
        async goToPage(page: number) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                await this.fetchInactiveSensors();
            }
        },

        async nextPage() {
            if (this.hasNext) {
                await this.goToPage(this.currentPage + 1);
            }
        },

        async previousPage() {
            if (this.hasPrevious) {
                await this.goToPage(this.currentPage - 1);
            }
        },

        async changePageSize(newPageSize: number) {
            if (newPageSize >= 1 && newPageSize <= 100) {
                this.pageSize = newPageSize;
                this.currentPage = 1; // Reset to first page when changing page size
                await this.fetchInactiveSensors();
            }
        }
    },
}); 