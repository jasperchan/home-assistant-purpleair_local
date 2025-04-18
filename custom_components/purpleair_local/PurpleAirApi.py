from datetime import timedelta
import logging

import math

from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_interval, async_track_point_in_utc_time
from homeassistant.util import dt

from .const import DISPATCHER, LOCAL_SCAN_INTERVAL, LOCAL_URL_FORMAT, \
    TEMP_ADJUSTMENT, HUMIDITY_ADJUSTMENT, SENSORS_MAP

_LOGGER = logging.getLogger(__name__)


def calc_dewpoint(temp_f, humidity):
    """
    Calculate dewpoint using August-Roche-Magnus approximation.
    Note: Rounding twice for both F>C and C>F conversions simply because the purpleair website does this (so I
    do this too, to match the purpleair website).
    """
    temp_c = round((temp_f - 32) * 5.0/9.0)

    numerator = 243.04 * (math.log(humidity / 100) + ((17.625 * temp_c) / (243.04 + temp_c)))
    denominator = 17.625 - math.log(humidity / 100) - ((17.625 * temp_c) / (243.04 + temp_c))
    dew_point_c = numerator / denominator

    dew_point_f = round((dew_point_c * 9/5) + 32)
    return dew_point_f


def process_heat_adjustments(json_result):
    """Since the purple air devices are affected by heat from itself, modify readings to account for difference"""
    new_temp = json_result['current_temp_f'] + TEMP_ADJUSTMENT
    new_humid = min(100, json_result['current_humidity'] + HUMIDITY_ADJUSTMENT)

    return {
        'current_temp_f': new_temp,
        'current_humidity': new_humid,
        'current_dewpoint_f': calc_dewpoint(new_temp, new_humid)
    }


class PurpleAirApi:
    def __init__(self, hass, session):
        self._hass = hass
        self._session = session
        self._nodes = {}
        self._data = {}
        self._scan_interval = timedelta(seconds=LOCAL_SCAN_INTERVAL)
        self._shutdown_interval = None

    def is_node_registered(self, pa_sensor_id):
        return pa_sensor_id in self._data

    def get_reading(self, pa_sensor_id, prop):
        if pa_sensor_id not in self._data:
            return None

        node = self._data[pa_sensor_id]
        return node[prop] if prop in node else None

    def register_node(self, pa_sensor_id, ip_address):
        if pa_sensor_id in self._nodes:
            _LOGGER.debug('detected duplicate registration: %s', pa_sensor_id)
            return

        self._nodes[pa_sensor_id] = { 'ip_address': ip_address }
        _LOGGER.debug('registered new node: %s', pa_sensor_id)

        if not self._shutdown_interval:
            _LOGGER.debug('starting background poll: %s', self._scan_interval)
            self._shutdown_interval = async_track_time_interval(
                self._hass,
                self._update,
                self._scan_interval
            )

            async_track_point_in_utc_time(
                self._hass,
                self._update,
                dt.utcnow() + timedelta(seconds=5)
            )

    def unregister_node(self, pa_sensor_id):
        if pa_sensor_id not in self._nodes:
            _LOGGER.debug('detected non-existent unregistration: %s', pa_sensor_id)
            return

        del self._nodes[pa_sensor_id]
        _LOGGER.debug('unregistered node: %s', pa_sensor_id)

        if not self._nodes and self._shutdown_interval:
            _LOGGER.debug('no more nodes, shutting down interval')
            self._shutdown_interval()
            self._shutdown_interval = None


    async def _fetch_data(self, local_node_ips):
        if not local_node_ips:
            _LOGGER.debug('no nodes provided')
            return []

        urls = list(map(LOCAL_URL_FORMAT.format, local_node_ips))
        _LOGGER.debug('fetch url list: %s', urls)

        results = []
        for url in urls:
            _LOGGER.debug('fetching url: %s', url)

            try:
                async with self._session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error('bad API response for %s: %s', url, response.status)

                    json = await response.json()
                    results.append(json)
            except Exception:
                _LOGGER.error('Unable to connect to purple air device: ' + url)

        return results

    async def _update(self, now=None):
        local_node_ips = [n['ip_address'] for n in self._nodes.values()]
        _LOGGER.debug('Purple Air nodes: %s', local_node_ips)

        results = await self._fetch_data(local_node_ips)

        nodes = {}
        for result in results:
            pa_sensor_id = result['SensorId']
            nodes[pa_sensor_id] = {
                'device_location': result['place']
            }
            # copy fields
            for index, entity_desc in SENSORS_MAP.items():
                key = entity_desc['key']
                if entity_desc['is_dual']:
                    key_a = key
                    key_b = f"{key}_b"
                    key_avg = f"{key}_avg"
                    if key_a in result and key_b in result:
                        nodes[pa_sensor_id][key_a] = result[key_a]
                        nodes[pa_sensor_id][key_b] = result[key_b]
                        nodes[pa_sensor_id][key_avg] = (result[key_a]+result[key_b])/2
                else:
                    if key in result:
                        nodes[pa_sensor_id][key] = result[key]
            # adjustments
            nodes[pa_sensor_id].update(process_heat_adjustments(result))
            # debug
            _LOGGER.debug('Json results for %s: %s', pa_sensor_id, result)
            _LOGGER.debug('Readings for %s: %s', pa_sensor_id, nodes[pa_sensor_id])

        self._data = nodes
        async_dispatcher_send(self._hass, DISPATCHER)
