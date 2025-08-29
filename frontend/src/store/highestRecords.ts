import { defineStore } from 'pinia';
import axios from '../plugins/axios';

export interface HighestRecord {
    station_name: string;
    brand_name: string;
    date: string;
    time: string;
    value: number;
    sensor_type: string;
    sensor_unit: string;
}

interface HighestRecordsState {
    records: HighestRecord[];
    isLoading: boolean;
    error: string | null;
    currentPage: number;
    totalPages: number;
    selectedBrand: string;
    availableBrands: string[];
    pageSize: number;
}

function parseXMLRecords(xmlString: string): HighestRecord[] {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlString, 'application/xml');
    const items = Array.from(xmlDoc.getElementsByTagName('list-item'));
    return items.map(item => ({
        station_name: item.getElementsByTagName('station_name')[0]?.textContent || '',
        brand_name: item.getElementsByTagName('brand_name')[0]?.textContent || '',
        date: item.getElementsByTagName('date')[0]?.textContent || '',
        time: item.getElementsByTagName('time')[0]?.textContent || '',
        value: parseFloat(item.getElementsByTagName('value')[0]?.textContent || '0'),
        sensor_type: item.getElementsByTagName('sensor_type')[0]?.textContent || '',
        sensor_unit: item.getElementsByTagName('sensor_unit')[0]?.textContent || '',
    }));
}

export const useHighestRecordsStore = defineStore('highestRecords', {
    state: (): HighestRecordsState => ({
        records: [],
        isLoading: false,
        error: null,
        currentPage: 1,
        totalPages: 1,
        selectedBrand: '',
        availableBrands: [],
        pageSize: 10,
    }),

    actions: {
        async fetchHighestRecords(forceRefresh = false) {
            this.isLoading = true;
            this.error = null;
            console.log('Store: fetchHighestRecords called with brand:', this.selectedBrand, 'page:', this.currentPage);
            try {
                const stationsResponse = await axios.get('/api/stations/');
                console.log('Store: Stations response:', stationsResponse.data);
                
                // Always include these brands as tabs
                const requiredBrands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron'];
                
                // Handle paginated response - check if data has 'results' property
                const stationsData = stationsResponse.data.results || stationsResponse.data;
                console.log('Store: Processed stations data:', stationsData);
                
                // Extract brands from stations - try both possible field names
                const brandsFromStations = (stationsData || []).map((station: any) => {
                    console.log('Store: Processing station:', station);
                    // Try both possible field names for brand
                    if (station.brand && typeof station.brand === 'object' && station.brand.name) {
                        return station.brand.name;
                    } else if (station.brand_name) {
                        return station.brand_name;
                    } else if (station.brand && typeof station.brand === 'string') {
                        return station.brand;
                    }
                    return null;
                }).filter((b: unknown): b is string => typeof b === 'string' && !!b);
                
                console.log('Store: Extracted brands from stations:', brandsFromStations);
                
                let brands = Array.from(new Set([...requiredBrands, ...brandsFromStations]));
                // Optionally, sort for consistent order
                brands = requiredBrands.concat(brands.filter(b => !requiredBrands.includes(b)));
                this.availableBrands = brands;
                
                console.log('Store: Final available brands:', brands);
                
                if (!this.selectedBrand && brands.length > 0) {
                    this.selectedBrand = brands[0];
                    console.log('Store: Set default brand to:', this.selectedBrand);
                }
                
                if (!this.selectedBrand) {
                    console.log('Store: No brand selected, clearing data');
                    this.records = [];
                    this.totalPages = 1;
                    this.isLoading = false;
                    return;
                }
                
                console.log('Store: Fetching highest records for brand:', this.selectedBrand);
                const response = await axios.get('/api/measurements/highest_by_brand/', {
                    params: {
                        brand: this.selectedBrand
                    },
                    responseType: 'text'
                });
                
                console.log('Store: Highest records response:', response.data);
                
                let records: HighestRecord[] = [];
                try {
                    records = JSON.parse(response.data);
                    console.log('Store: Parsed JSON records:', records);
                } catch (parseError) {
                    console.log('Store: JSON parse failed, trying XML:', parseError);
                    records = parseXMLRecords(response.data);
                    console.log('Store: Parsed XML records:', records);
                }
                
                this.records = records;
                this.totalPages = Math.max(1, Math.ceil(this.records.length / this.pageSize));
                if (this.currentPage > this.totalPages) this.currentPage = 1;
                
                console.log('Store: State updated - records count:', this.records.length, 'totalPages:', this.totalPages, 'availableBrands count:', this.availableBrands.length);
            } catch (error: any) {
                console.error('Store: Error fetching highest records:', error);
                this.error = error.message || 'Failed to fetch highest records';
                this.records = [];
                this.totalPages = 1;
                this.availableBrands = [];
                console.log('Store: Fetch error, state cleared.');
            } finally {
                this.isLoading = false;
                console.log('Store: isLoading set to false.');
            }
        },
        setBrand(brand: string) {
            this.selectedBrand = brand;
            this.currentPage = 1;
            this.fetchHighestRecords(true);
        },
        setPage(page: number) {
            this.currentPage = page;
        },
    },
}); 