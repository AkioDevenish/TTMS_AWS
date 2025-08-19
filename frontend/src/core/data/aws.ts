export interface AWSStation {
    id: string;
    name: string;
    location: string;
    lastUpdate: string | null;
    parameters: {
        temperature?: number;
        humidity?: number;
        windSpeed?: number;
        rainfall?: number;
    };
    brand?: string;
    brand_name?: string;
} 