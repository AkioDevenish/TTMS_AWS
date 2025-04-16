from rest_framework_csv.renderers import CSVRenderer

class MeasurementCSVRenderer(CSVRenderer):
    header = ['station_name', 'sensor_type', 'date', 'time', 'value']

class StationCSVRenderer(CSVRenderer):
    header = ['name', 'location', 'status']
