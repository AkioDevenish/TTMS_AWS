import { defineStore } from 'pinia';
import axios from '../plugins/axios';

export interface StationHealth {
    id: number;
    name: string;
    battery_status: string;
    connectivity_status: string;
    created_at: string | null;
    station: number;
    brand: string;
    status: string;
}

interface AWSStationsState {
    stations: any[];
    stationHealth: StationHealth[];
    isLoading: boolean;
    error: string | null;
    selectedBrand: string | null;
    availableBrands: string[];
    refreshInterval: number | null;
    // Pagination state
    currentPage: number;
    pageSize: number;
    totalStations: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
}

export const useAWSStationsStore = defineStore('awsStations', {
    state: (): AWSStationsState => ({
        stations: [],
        stationHealth: [],
        isLoading: false,
        error: null,
        selectedBrand: null,
        availableBrands: ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron'],
        refreshInterval: null,
        // Pagination state
        currentPage: 1,
        pageSize: 10,
        totalStations: 0,
        totalPages: 0,
        hasNext: false,
        hasPrevious: false,
    }),

    getters: {
        getStationStatus: (state) => {
            const total = state.stationHealth.length;
            const online = state.stationHealth.filter(s => s.status === 'Online').length;
            const offline = state.stationHealth.filter(s => s.status === 'Offline').length;
            const warning = state.stationHealth.filter(s => s.status === 'Warning').length;
            
            const uptime = total > 0 ? Math.round((online / total) * 100) : 0;
            
            return {
                total,
                online,
                offline,
                warning,
                uptime
            };
        },

        hasRecentData: (state) => {
            return state.stationHealth.length > 0;
        },

        getStationsByBrand: (state) => (brand: string) => {
            return state.stationHealth.filter(s => s.brand === brand);
        },

        getBrandStatus: (state) => (brand: string) => {
            const brandStations = state.stationHealth.filter(s => s.brand === brand);
            const total = brandStations.length;
            const online = brandStations.filter(s => s.status === 'Online').length;
            const offline = brandStations.filter(s => s.status === 'Offline').length;
            const warning = brandStations.filter(s => s.status === 'Warning').length;
            
            return {
                total,
                online,
                offline,
                warning,
                uptime: total > 0 ? Math.round((online / total) * 100) : 0
            };
        },

        // Pagination getters
        getPaginationInfo: (state) => {
            return {
                currentPage: state.currentPage,
                pageSize: state.pageSize,
                totalStations: state.totalStations,
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
        async fetchStationHealth(brand?: string, page: number = 1, pageSize: number = 10) {
            this.isLoading = true;
            this.error = null;
            
            try {
                console.log('Fetching station health for brand:', brand || 'all', 'page:', page, 'pageSize:', pageSize);
                
                const params: any = {
                    page: page,
                    page_size: pageSize
                };
                if (brand) {
                    params.brand = brand;
                }
                
                const response = await axios.get('/api/stations/aws-health/', { params });
                console.log('Station health response:', response.data);
                
                if (response.data && response.data.data) {
                    this.stationHealth = response.data.data;
                    console.log('Station health data updated:', this.stationHealth.length, 'stations');
                    
                    // Update pagination state
                    if (response.data.pagination) {
                        this.currentPage = response.data.pagination.page;
                        this.pageSize = response.data.pagination.page_size;
                        this.totalStations = response.data.pagination.total;
                        this.totalPages = response.data.pagination.total_pages;
                        this.hasNext = response.data.pagination.has_next;
                        this.hasPrevious = response.data.pagination.has_previous;
                    }
                } else {
                    console.log('No station health data received');
                    this.stationHealth = [];
                    // Reset pagination state
                    this.currentPage = 1;
                    this.totalStations = 0;
                    this.totalPages = 0;
                    this.hasNext = false;
                    this.hasPrevious = false;
                }
                
                // Update available brands if not already set
                if (this.availableBrands.length === 0) {
                    this.availableBrands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron'];
                }
                
            } catch (err: any) {
                console.error('Error fetching station health:', err);
                this.error = err.response?.data?.error || err.message || 'Failed to fetch station health';
                this.stationHealth = [];
                // Reset pagination state on error
                this.currentPage = 1;
                this.totalStations = 0;
                this.totalPages = 0;
                this.hasNext = false;
                this.hasPrevious = false;
            } finally {
                this.isLoading = false;
            }
        },

        setBrand(brand: string | null) {
            this.selectedBrand = brand;
            if (brand) {
                this.fetchStationHealth(brand, 1, this.pageSize);
            } else {
                this.fetchStationHealth(undefined, 1, this.pageSize);
            }
        },

        // Pagination methods
        async goToPage(page: number) {
            if (page >= 1 && page <= this.totalPages) {
                await this.fetchStationHealth(this.selectedBrand || undefined, page, this.pageSize);
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
                await this.fetchStationHealth(this.selectedBrand || undefined, 1, newPageSize);
            }
        },

        async init() {
            console.log('Initializing AWS Stations store');
            await this.fetchStationHealth(undefined, 1, this.pageSize);
            
            // Set up auto-refresh every 5 minutes
            this.refreshInterval = window.setInterval(() => {
                this.fetchStationHealth(this.selectedBrand || undefined, this.currentPage, this.pageSize);
            }, 5 * 60 * 1000);
        },

        cleanup() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
                this.refreshInterval = null;
            }
        },

        async testAPI() {
            try {
                console.log('Testing API endpoints...');
                
                // Test the main stations endpoint
                const stationsResponse = await axios.get('/api/stations/');
                console.log('Stations endpoint response:', stationsResponse.data);
                
                // Test the health endpoint
                const healthResponse = await axios.get('/api/stations/aws-health/');
                console.log('Health endpoint response:', healthResponse.data);
                
                return {
                    stations: stationsResponse.data,
                    health: healthResponse.data
                };
            } catch (err: any) {
                console.error('API test failed:', err);
                throw err;
            }
        }
    }
}); 