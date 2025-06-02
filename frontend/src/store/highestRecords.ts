import { defineStore } from 'pinia';
import axios from 'axios';

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
                const stationsResponse = await axios.get('/stations/');
                // Always include these brands as tabs
                const requiredBrands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT'];
                const brandsFromStations = (stationsResponse.data || []).map((station: any) => station.brand || station.brand_name).filter((b: unknown): b is string => typeof b === 'string' && !!b);
                let brands = Array.from(new Set([...requiredBrands, ...brandsFromStations]));
                // Optionally, sort for consistent order
                brands = requiredBrands.concat(brands.filter(b => !requiredBrands.includes(b)));
                this.availableBrands = brands;
                if (!this.selectedBrand && brands.length > 0) {
                    this.selectedBrand = brands[0];
                }
                if (!this.selectedBrand) {
                    this.records = [];
                    this.totalPages = 1;
                    this.isLoading = false;
                    return;
                }
                const response = await axios.get('/measurements/highest_by_brand/', {
                    params: {
                        brand: this.selectedBrand
                    },
                    responseType: 'text'
                });
                let records: HighestRecord[] = [];
                try {
                    records = JSON.parse(response.data);
                } catch {
                    records = parseXMLRecords(response.data);
                }
                this.records = records;
                this.totalPages = Math.max(1, Math.ceil(this.records.length / this.pageSize));
                if (this.currentPage > this.totalPages) this.currentPage = 1;
                console.log('Store: State updated - records count:', this.records.length, 'availableBrands count:', this.availableBrands.length);
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