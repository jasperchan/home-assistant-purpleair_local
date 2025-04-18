"""Constants for the Purple Air integration."""
from homeassistant.const import UnitOfTemperature, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UnitOfPressure, PERCENTAGE, Platform, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER


# Map of sensors to create entities for
SENSORS_MAP = {
    # single sensors
    'temperature':             {'key': 'current_temp_f',     'uom': UnitOfTemperature.FAHRENHEIT,  'icon': 'mdi:thermometer', 'name': 'Temperature', 'is_dual': False},
    'dewpoint':                {'key': 'current_dewpoint_f', 'uom': UnitOfTemperature.FAHRENHEIT,  'icon': 'mdi:water-outline', 'name': 'Dewpoint', 'is_dual': False},
    'humidity':                {'key': 'current_humidity',   'uom': PERCENTAGE,  'icon': 'mdi:water-percent', 'name': 'Humidity', 'is_dual': False},
    'pressure':                {'key': 'pressure',         'uom': UnitOfPressure.HPA,     'icon': 'mdi:gauge', 'name': 'Pressure', 'is_dual': False},
    'rssi':                    {'key': 'rssi',             'uom': SIGNAL_STRENGTH_DECIBELS_MILLIWATT, 'icon': 'mdi:wifi', 'name': 'Signal Strength', 'is_dual': False},
    'gas_680':                 {'key': 'gas_680',          'uom': Platform.AIR_QUALITY, 'icon': 'mdi:weather-hazy', 'name': 'VOC IAQ', 'is_dual': False},
    # has `_b` for dual sensors
    'pm2_5_aqi':               {'key': 'pm2.5_aqi',        'uom': Platform.AIR_QUALITY, 'icon': 'mdi:blur-linear', 'name': 'PM2.5 AQI', 'is_dual': True},
    'pm1_0_atm':               {'key': 'pm1_0_atm',        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM1.0 (ATM)', 'is_dual': True},
    'pm2_5_atm':               {'key': 'pm2_5_atm',        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM2.5 (ATM)', 'is_dual': True},
    'pm10_0_atm':              {'key': 'pm10_0_atm',       'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM10.0 (ATM)', 'is_dual': True},
    'pm1_0_cf_1':              {'key': 'pm1_0_cf_1',       'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM1.0 (CF=1)', 'is_dual': True},
    'pm2_5_cf_1':              {'key': 'pm2_5_cf_1',       'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM2.5 (CF=1)', 'is_dual': True},
    'pm10_0_cf_1':             {'key': 'pm10_0_cf_1',      'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'icon': 'mdi:blur', 'name': 'PM10.0 (CF=1)', 'is_dual': True},
    'p_10_0_um':               {'key': 'p_10_0_um',        'uom': None, 'icon': 'mdi:blur', 'name': '10.0µm Particles / dL', 'is_dual': True},
    'p_5_0_um':                {'key': 'p_5_0_um',         'uom': None, 'icon': 'mdi:blur', 'name': '5.0µm Particles / dL', 'is_dual': True},
    'p_2_5_um':                {'key': 'p_2_5_um',         'uom': None, 'icon': 'mdi:blur', 'name': '2.5µm Particles / dL', 'is_dual': True},
    'p_1_0_um':                {'key': 'p_1_0_um',         'uom': None, 'icon': 'mdi:blur', 'name': '1.0µm Particles / dL', 'is_dual': True},
    'p_0_5_um':                {'key': 'p_0_5_um',         'uom': None, 'icon': 'mdi:blur', 'name': '0.5µm Particles / dL', 'is_dual': True},
    'p_0_3_um':                {'key': 'p_0_3_um',         'uom': None, 'icon': 'mdi:blur', 'name': '0.3µm Particles / dL', 'is_dual': True},
}

MANUFACTURER = 'PurpleAir'
DISPATCHER = 'dispatcher_purpleair_local'
DOMAIN = "purpleair_local"
TEMP_ADJUSTMENT = -8  # From PurpleAir javascript: `(parseInt(temp) + -8).toFixed(0);`
HUMIDITY_ADJUSTMENT = +4  # From PurpleAir javascript: `(hum = parseInt(hum) + 4) > 100 && (hum = 100)`

LOCAL_SCAN_INTERVAL = 30
LOCAL_URL_FORMAT = "http://{0}/json?live=false"

