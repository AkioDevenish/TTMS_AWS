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
}

export const useAWSStationsStore = defineStore('awsStations', {
    state: (): AWSStationsState => ({
        stations: [],
        stationHealth: [],
        isLoading: false,
        error: null,
        selectedBrand: null,
        availableBrands: ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT'],
        refreshInterval: null,
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
        }
    },

    actions: {
        async fetchStationHealth(brand?: string) {
            this.isLoading = true;
            this.error = null;
            
            try {
                console.log('Fetching station health for brand:', brand || 'all');
                
                const params: any = {};
                if (brand) {
                    params.brand = brand;
                }
                
                const response = await axios.get('/api/stations/aws-health/', { params });
                console.log('Station health response:', response.data);
                
                if (response.data && response.data.data) {
                    this.stationHealth = response.data.data;
                    console.log('Station health data updated:', this.stationHealth.length, 'stations');
                } else {
                    console.log('No station health data received');
                    this.stationHealth = [];
                }
                
                // Update available brands if not already set
                if (this.availableBrands.length === 0) {
                    this.availableBrands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT'];
                }
                
            } catch (err: any) {
                console.error('Error fetching station health:', err);
                this.error = err.response?.data?.error || err.message || 'Failed to fetch station health';
                this.stationHealth = [];
            } finally {
                this.isLoading = false;
            }
        },

        setBrand(brand: string | null) {
            this.selectedBrand = brand;
            if (brand) {
                this.fetchStationHealth(brand);
            } else {
                this.fetchStationHealth();
            }
        },

        async init() {
            console.log('Initializing AWS Stations store');
            await this.fetchStationHealth();
            
            // Set up auto-refresh every 5 minutes
            this.refreshInterval = window.setInterval(() => {
                this.fetchStationHealth(this.selectedBrand || undefined);
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