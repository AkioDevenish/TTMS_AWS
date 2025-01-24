export interface AWSStation {
    id: string;
    name: string;
    location: string;
    lastUpdate: string | null;
    status: 'Online' | 'Offline' | 'Maintenance' | 'NoData';
    parameters: {
        temperature?: number;
        humidity?: number;
        windSpeed?: number;
        rainfall?: number;
    }
}

export const getOfflineStations = (stations: AWSStation[]) => {
    return stations.filter(station => station.status === 'Offline')
}

export const getNoDataStations = (stations: AWSStation[]) => {
    return stations.filter(station => station.status === 'NoData')
}

export const getStationStatus = (stations: AWSStation[]) => {
    const total = stations.length
    const offline = stations.filter(s => s.status === 'Offline').length
    const maintenance = stations.filter(s => s.status === 'Maintenance').length
    const noData = stations.filter(s => s.status === 'NoData').length
    const online = total - offline - maintenance - noData
    
    return {
        total,
        online,
        offline,
        maintenance,
        noData,
        uptime: total ? ((online / total) * 100).toFixed(1) : '0'
    }
} 