"""
Data validation utility for TTMS AWS system.
Provides validation methods for various sensor types with sensible thresholds.
"""

import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Data validation class for TTMS AWS measurements.
    Validates sensor data against predefined thresholds and returns validation results.
    """
    
    # Sensor type thresholds based on realistic meteorological ranges
    SENSOR_THRESHOLDS = {
        # Wind sensors (0-300 mph as specified)
        'ws': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},  # 300 mph = 134 m/s
        'wind_ave10': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_max10': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_min10': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'Wind Speed': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'Wind Speed Average': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'Wind Speed Inst': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'Gust Speed': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        # Common field names from instruments
        'wind': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'windspeed': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_speed': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_speed_avg': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_speed_max': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'wind_speed_min': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'gust_speed': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        'gust': {'min': 0.0, 'max': 134.0, 'unit': 'm/s'},
        
        # Wind direction sensors (0-360 degrees)
        'wd': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'dir_ave10': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'dir_max10': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'dir_hi10': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'dir_lo10': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'Wind Direction': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'Gust Direction': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'Wind Dir Average': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'Wind Dir Inst': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        # Common field names from instruments
        'winddir': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'wind_direction': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'direction': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'wind_dir': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'wind_dir_avg': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'wind_dir_max': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        'gust_dir': {'min': 0.0, 'max': 360.0, 'unit': '°'},
        
        # Rainfall sensors (0-15 mm as specified)
        'rg': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'Precipitation': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        '5 min rain': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'Daily Rain': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'Max Precipitation Rate': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},
        'rain_counter': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'rain_intensity_max': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},

        
        # Common field names from instruments
        'rain': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'rainfall': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'rainfall_rate': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},
        'precip': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'precipitation': {'min': 0.0, 'max': 15.0, 'unit': 'mm'},
        'rain_intensity': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},
        'rain_rate': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},
        'rainfall_intensity': {'min': 0.0, 'max': 15.0, 'unit': 'mm/h'},
        
        # Temperature sensors (-12 to 50 degrees as specified)
        'bt1': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'mt1': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'Air Temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'Maximum Air Temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'Minimum Air Temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'Dew Point': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'Soil Temp (15cm)': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'RH Sensor Temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        # Common field names from instruments
        'temp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'air_temp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'air_temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'dewpoint': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'dew_point': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'airtemp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'air_t': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        't': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'temp_air': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'temp_out': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'temp_outdoor': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'outdoor_temp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'external_temp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        
        # Pressure sensors (reasonable atmospheric pressure range)
        'bp1': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'Barometric Pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'Baro Tendency': {'min': -50.0, 'max': 50.0, 'unit': 'hPa'},
        'Atmospheric Pressure': {'min': 80.0, 'max': 120.0, 'unit': 'kPa'},
        'Reference Pressure': {'min': 80.0, 'max': 120.0, 'unit': 'kPa'},
        'Vapor Pressure Deficit': {'min': 0.0, 'max': 10.0, 'unit': 'kPa'},
        # Common field names from instruments
        'baro': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'barometric': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'atmospheric_pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'barometric_pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'atm_pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'p': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'pressure_abs': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        'abs_pressure': {'min': 800.0, 'max': 1200.0, 'unit': 'hPa'},
        
        # Solar radiation sensors (realistic solar radiation range)
        'sv1': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'si1': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'su1': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'irradiation': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'irr_max': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'Solar Radiation': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'Solar Radiation Avg': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'Solar Radiation Total': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        # Common field names from instruments
        'solar': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'solar_radiation': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'radiation': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'solar_rad': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'solar_irradiance': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'irradiance': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'sun': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        'sunlight': {'min': 0.0, 'max': 1200.0, 'unit': 'W/m²'},
        
        # Humidity sensors (0-100%)
        'humidity': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'Relative Humidity': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        # Common field names from instruments
        'rh': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'relative_humidity': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'hum': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'humidity_rel': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'relative_hum': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'humidity_relative': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'h': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        
        # Battery and connectivity sensors
        'battery': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'bpc': {'min': 0.0, 'max': 100.0, 'unit': 'V'},
        'css': {'min': -120.0, 'max': -30.0, 'unit': 'dBm'},
        'Battery': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'Battery Percent': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        # Common field names from instruments
        'batt': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'battery_voltage': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'battery_percent': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'battery_level': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'batt_voltage': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'batt_level': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'voltage': {'min': 0.0, 'max': 15.0, 'unit': 'V'},
        'signal_strength': {'min': -120.0, 'max': -30.0, 'unit': 'dBm'},
        'rssi': {'min': -120.0, 'max': -30.0, 'unit': 'dBm'},
        'signal': {'min': -120.0, 'max': -30.0, 'unit': 'dBm'},
        
        # Other sensors with reasonable ranges
        'Leaf Wetness': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'Soil Moisture (10cm)': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'Soil Moisture (20cm)': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'Soil Moisture (30cm)': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'Hours of Sunshine': {'min': 0.0, 'max': 24.0, 'unit': 'hr'},
        'EvapoTranspiration': {'min': 0.0, 'max': 20.0, 'unit': 'mm'},
        'Lightning Activity': {'min': 0.0, 'max': 1.0, 'unit': 'binary'},
        'Lightning Distance': {'min': 0.0, 'max': 100.0, 'unit': 'km'},
        'X-axis Level': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        'Y-axis Level': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        # Common field names from instruments
        'soil_moisture': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'soil_temp': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'lightning': {'min': 0.0, 'max': 1.0, 'unit': 'binary'},
        'sunshine': {'min': 0.0, 'max': 24.0, 'unit': 'hr'},
        'soil_moist': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'soil_temperature': {'min': -12.0, 'max': 50.0, 'unit': '°C'},
        'leaf_wetness': {'min': 0.0, 'max': 100.0, 'unit': '%'},
        'evapotranspiration': {'min': 0.0, 'max': 20.0, 'unit': 'mm'},
        'et': {'min': 0.0, 'max': 20.0, 'unit': 'mm'},
        'tilt_x': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        'tilt_y': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        'level_x': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        'level_y': {'min': -90.0, 'max': 90.0, 'unit': '°'},
        
        # Additional common instrument field names
        'timestamp': {'min': 0.0, 'max': 9999999999.0, 'unit': 'timestamp'},
        'device_id': {'min': 0.0, 'max': 999999.0, 'unit': 'id'},
        'sn': {'min': 0.0, 'max': 999999.0, 'unit': 'id'},
        'sampleTime': {'min': 0.0, 'max': 9999999999.0, 'unit': 'timestamp'},
        'datetime': {'min': 0.0, 'max': 9999999999.0, 'unit': 'timestamp'},
    }
    
    @classmethod
    def is_invalid_sensor_value(cls, value: float) -> bool:
        """
        Check if a sensor value represents an invalid reading.
        Common invalid values that indicate sensor errors or missing data.
        """
        if value is None:
            return True
            
        # Common invalid values that indicate sensor issues
        invalid_values = [
            -999, -999.0, 999, 999.0,
            -9999, -9999.0, 9999, 9999.0,
            -32768, -32768.0, 32768, 32768.0,
            -99999, -99999.0, 99999, 99999.0
        ]
        
        return value in invalid_values

    @classmethod
    def is_stuck_sensor(cls, measurements: list, min_measurements: int = 5, tolerance: float = 0.1) -> bool:
        """
        Check if a sensor is stuck (always reading the same value).
        
        Args:
            measurements: List of recent measurements for the sensor
            min_measurements: Minimum number of measurements to check (default: 5)
            tolerance: Tolerance for considering values "the same" (default: 0.1)
            
        Returns:
            True if sensor appears to be stuck, False otherwise
        """
        if not measurements or len(measurements) < min_measurements:
            return False
            
        try:
            # Get the most recent measurements
            recent_measurements = measurements[:min_measurements]
            values = [float(m.get('value', m)) for m in recent_measurements]
            
            # Check if all values are within tolerance of the first value
            first_value = values[0]
            for value in values[1:]:
                if abs(value - first_value) > tolerance:
                    return False
                    
            # If we get here, all values are within tolerance
            return True
            
        except (ValueError, TypeError):
            return False

    @classmethod
    def validate_measurement(cls, sensor_type: str, value: float) -> Tuple[bool, str]:
        """
        Validate a measurement value against predefined thresholds.
        
        Args:
            sensor_type: The type of sensor (e.g., 'ws', 'rg', 'bt1')
            value: The measurement value to validate
            
        Returns:
            Tuple of (is_valid, validation_message)
        """
        try:
            # First check if the value is an invalid sensor reading
            if cls.is_invalid_sensor_value(value):
                return False, f"Value {value} is an invalid sensor reading (sensor error or missing data)"
            
            # First try exact match
            if sensor_type in cls.SENSOR_THRESHOLDS:
                thresholds = cls.SENSOR_THRESHOLDS[sensor_type]
            else:
                # Try case-insensitive match
                sensor_type_lower = sensor_type.lower()
                thresholds = None
                for key in cls.SENSOR_THRESHOLDS:
                    if key.lower() == sensor_type_lower:
                        thresholds = cls.SENSOR_THRESHOLDS[key]
                        break
                
                # If still no match, try partial matching for common patterns
                if not thresholds:
                    for key in cls.SENSOR_THRESHOLDS:
                        if (sensor_type_lower in key.lower() or 
                            key.lower() in sensor_type_lower or
                            any(word in sensor_type_lower for word in key.lower().split('_'))):
                            thresholds = cls.SENSOR_THRESHOLDS[key]
                            logger.info(f"Partial match found: '{sensor_type}' matched with '{key}'")
                            break
            
            if not thresholds:
                # If no thresholds found, log warning and return True (don't fail validation)
                logger.warning(f"No validation thresholds defined for sensor type: {sensor_type}")
                return True, f"No validation thresholds defined for {sensor_type}"
            
            min_val = thresholds['min']
            max_val = thresholds['max']
            unit = thresholds['unit']
            
            # Check if value is within range
            if min_val <= value <= max_val:
                return True, f"Value {value} {unit} is within acceptable range [{min_val}, {max_val}] {unit}"
            else:
                return False, f"Value {value} {unit} is outside acceptable range [{min_val}, {max_val}] {unit}"
                
        except (TypeError, ValueError) as e:
            logger.error(f"Error validating measurement for sensor {sensor_type}: {e}")
            return False, f"Validation error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error validating measurement for sensor {sensor_type}: {e}")
            return False, f"Unexpected validation error: {str(e)}"
    
    @classmethod
    def get_sensor_thresholds(cls, sensor_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the validation thresholds for a specific sensor type.
        
        Args:
            sensor_type: The type of sensor
            
        Returns:
            Dictionary with min, max, and unit values, or None if not found
        """
        return cls.SENSOR_THRESHOLDS.get(sensor_type)
    
    @classmethod
    def get_all_thresholds(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all sensor validation thresholds.
        
        Returns:
            Dictionary of all sensor thresholds
        """
        return cls.SENSOR_THRESHOLDS.copy()
    
    @classmethod
    def add_custom_threshold(cls, sensor_type: str, min_val: float, max_val: float, unit: str) -> None:
        """
        Add or update custom validation thresholds for a sensor type.
        
        Args:
            sensor_type: The type of sensor
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
            unit: Unit of measurement
        """
        cls.SENSOR_THRESHOLDS[sensor_type] = {
            'min': min_val,
            'max': max_val,
            'unit': unit
        }
        logger.info(f"Added custom threshold for {sensor_type}: [{min_val}, {max_val}] {unit}")
    
    @classmethod
    def validate_batch_measurements(cls, measurements: list) -> list:
        """
        Validate a batch of measurements.
        
        Args:
            measurements: List of measurement dictionaries with 'sensor_type' and 'value' keys
            
        Returns:
            List of validation results with 'is_valid', 'message', and original measurement data
        """
        results = []
        
        for measurement in measurements:
            sensor_type = measurement.get('sensor_type')
            value = measurement.get('value')
            
            if sensor_type is None or value is None:
                results.append({
                    'measurement': measurement,
                    'is_valid': False,
                    'message': 'Missing sensor_type or value'
                })
                continue
            
            is_valid, message = cls.validate_measurement(sensor_type, value)
            results.append({
                'measurement': measurement,
                'is_valid': is_valid,
                'message': message
            })
        
        return results
    
    @classmethod
    def debug_sensor_matching(cls, sensor_type: str) -> str:
        """
        Debug method to help understand why a sensor type might not be matching.
        
        Args:
            sensor_type: The sensor type to debug
            
        Returns:
            Debug information string
        """
        sensor_type_lower = sensor_type.lower()
        exact_matches = []
        case_insensitive_matches = []
        partial_matches = []
        
        for key in cls.SENSOR_THRESHOLDS:
            if key == sensor_type:
                exact_matches.append(key)
            elif key.lower() == sensor_type_lower:
                case_insensitive_matches.append(key)
            elif (sensor_type_lower in key.lower() or 
                  key.lower() in sensor_type_lower or
                  any(word in sensor_type_lower for word in key.lower().split('_'))):
                partial_matches.append(key)
        
        debug_info = f"Debug for sensor type: '{sensor_type}'\n"
        debug_info += f"Exact matches: {exact_matches}\n"
        debug_info += f"Case-insensitive matches: {case_insensitive_matches}\n"
        debug_info += f"Partial matches: {partial_matches}\n"
        debug_info += f"Available sensor types: {list(cls.SENSOR_THRESHOLDS.keys())}\n"
        
        return debug_info


# Test method to verify validation is working
def test_validation():
    """
    Test method to verify validation logic is working correctly.
    Run this to see if validation is functioning as expected.
    """
    print("Testing DataValidator...")
    
    # Test some valid measurements
    test_cases = [
        ('ws', 50.0),      # Wind speed within range
        ('ws', 150.0),     # Wind speed above range (should fail)
        ('rg', 5.0),       # Rainfall within range
        ('rg', 20.0),      # Rainfall above range (should fail)
        ('bt1', 25.0),     # Temperature within range
        ('bt1', -20.0),    # Temperature below range (should fail)
        ('humidity', 75.0), # Humidity within range
        ('humidity', 150.0), # Humidity above range (should fail)
        ('unknown_sensor', 100.0), # Unknown sensor (should pass with warning)
    ]
    
    for sensor_type, value in test_cases:
        is_valid, message = DataValidator.validate_measurement(sensor_type, value)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status}: {sensor_type} = {value} -> {message}")
    
    print("\nValidation test completed!")


if __name__ == "__main__":
    test_validation() 