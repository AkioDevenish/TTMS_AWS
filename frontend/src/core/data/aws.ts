export interface AWSStation {
    id: string;
    name: string;
    location: string;
    lastUpdate: string | null;
    status: 'Online' | 'Offline' | 'Maintenance';
    parameters: {
        temperature?: number;
        humidity?: number;
        windSpeed?: number;
        rainfall?: number;
    }
}

export const awsStations: AWSStation[] = [
    {
        id: 'T09',
        name: 'Brigand Hill',
        location: 'Eastern Trinidad',
        lastUpdate: null,
        status: 'Offline',
        parameters: {}
    },
    {
        id: 'T16',
        name: 'Lochmaben',
        location: 'Southern Trinidad',
        lastUpdate: '2024-03-21T15:30:00',
        status: 'Online',
        parameters: {
            temperature: 28.5,
            humidity: 75,
            windSpeed: 12,
            rainfall: 0
        }
    },
    {
        id: 'T18',
        name: 'Matura',
        location: 'North-Eastern Trinidad',
        lastUpdate: null,
        status: 'Offline',
        parameters: {}
    },
    {
        id: 'T05',
        name: 'Mt. St. Benedict',
        location: 'Northern Trinidad',
        lastUpdate: '2024-03-21T15:25:00',
        status: 'Maintenance',
        parameters: {
            temperature: 26.8,
            humidity: 82,
            windSpeed: 8,
            rainfall: 0.2
        }
    }
]

export const getOfflineStations = () => {
    return awsStations.filter(station => station.status === 'Offline')
}

export const getStationStatus = () => {
    const total = awsStations.length
    const offline = awsStations.filter(s => s.status === 'Offline').length
    const maintenance = awsStations.filter(s => s.status === 'Maintenance').length
    const online = total - offline - maintenance
    
    return {
        total,
        online,
        offline,
        maintenance,
        uptime: ((online / total) * 100).toFixed(1)
    }
} 