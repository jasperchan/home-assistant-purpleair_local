## Local Purple Air Zen Integration

**This integration specifically works with the PurpleAir Zen.**

This is an integration for home assistant that works integrates with local
polling on your PurpleAir devices on your local network.

_Code adapted from https://github.com/johnboiles/home-assistant-purpleair & https://github.com/GenuineAffect/home-assistant-purpleair_local_

It creates one device per Purple Air device registered and several sensors
for each several readings.

### Installation

Simply copy the `/purpleair_local` directory in to your config's
`custom_components` directory (you may need to create it), restart Home
Assistant, and add the integration via the UI (it's simple!).

To register a new purple air device:

1. Add "Purple Air" Integration.
2. Enter the IP address of your local purple air device
3. Give it a name.

#### Current Sensors

This will create entities for all the fields returned by the `/json` endpoint of a PurpleAir Zen:

```
{
  "SensorId": "aa:aa:aa:aa:aa:aa",
  "DateTime": "2025/04/15T17:01:14z",
  "Geo": "PurpleAir-b51e",
  "Mem": 11408,
  "memfrag": 25,
  "memfb": 8552,
  "memcs": 448,
  "Id": 0,
  "lat": 0.0,
  "lon": 0.0,
  "Adc": 0.0,
  "loggingrate": 15,
  "place": "inside",
  "version": "7.04",
  "uptime": 14637,
  "rssi": -53,
  "period": 120,
  "httpsuccess": 249,
  "httpsends": 249,
  "hardwareversion": "3.0",
  "hardwarediscovered": "3.0+OPENLOG+NO-DISK+RV3028+BME68X+KX122+PMSX003-A+PMSX003-B",
  "current_temp_f": 77,
  "current_humidity": 29,
  "current_dewpoint_f": 42,
  "pressure": 980.3,
  "current_temp_f_680": 77,
  "current_humidity_680": 29,
  "current_dewpoint_f_680": 42,
  "pressure_680": 980.3,
  "gas_680": 51.79,
  "p25aqic_b": "rgb(1,228,0)",
  "pm2.5_aqi_b": 9,
  "pm1_0_cf_1_b": 1.25,
  "p_0_3_um_b": 359.34,
  "pm2_5_cf_1_b": 2.12,
  "p_0_5_um_b": 104.73,
  "pm10_0_cf_1_b": 2.68,
  "p_1_0_um_b": 14.93,
  "pm1_0_atm_b": 1.25,
  "p_2_5_um_b": 1.97,
  "pm2_5_atm_b": 2.12,
  "p_5_0_um_b": 0.56,
  "pm10_0_atm_b": 2.68,
  "p_10_0_um_b": 0.37,
  "p25aqic": "rgb(1,228,0)",
  "pm2.5_aqi": 9,
  "pm1_0_cf_1": 1.55,
  "p_0_3_um": 381.6,
  "pm2_5_cf_1": 2.16,
  "p_0_5_um": 113.56,
  "pm10_0_cf_1": 2.84,
  "p_1_0_um": 15.42,
  "pm1_0_atm": 1.55,
  "p_2_5_um": 1.96,
  "pm2_5_atm": 2.16,
  "p_5_0_um": 1,
  "pm10_0_atm": 2.84,
  "p_10_0_um": 0,
  "pa_latency": 396,
  "response": 201,
  "response_date": 1744736472,
  "latency": 703,
  "wlstate": "Connected",
  "status_0": 2,
  "status_1": 0,
  "status_2": 2,
  "status_3": 2,
  "status_4": 2,
  "status_6": 2,
  "ssid": "ssid"
}
```

Sensor data on PurpleAir is updated every 60 seconds.

##### Adjusted Sensors

In a similar manner to the actual purple air website, some sensors are adjusted manually to take into
account the fact that the housing itself increases the temperature and has reduced humidity. Calculated
sensors are marked above.

This component is licensed under the MIT license, so feel free to copy,
enhance, and redistribute as you see fit.

## Releases

### 2.0.3

Added support for dual sensor devices that have a physical issue with one sensor. If a device has dual sensors and one of them is > 300 difference, it will set the confidence to "Severe" and instead of averaging the values, will use the lower value exclusively.

### 2.0.1

Replace public purple air device support (via purpleair.com) and replace
with purpleair devices that are on your local network only.

### 1.1.0

Adds support for private hidden sensors and indoor sensors. Fixes #3 and #4.

### 1.0.0

Initial release (after versioning)
