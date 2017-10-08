import urllib

import requests

BASE_API_INFO = {
    'auth': {
        'name': 'SYNO.API.Auth',
        'version': 2
    },
    'camera': {
        'name': 'SYNO.SurveillanceStation.Camera',
        'version': 1
    },
    'camera_event': {
        'name': 'SYNO.SurveillanceStation.Camera.Event',
        'version': 1
    },
    'video_stream': {
        'name': 'SYNO.SurveillanceStation.VideoStream',
        'version': 1
    },
}

API_NAMES = [api['name'] for api in BASE_API_INFO.values()]

RECORDING_STATUS = [
    # Continue recording schedule
    1,
    # Motion detect recording schedule
    2,
    # Digital input recording schedule
    3,
    # Digital input recording schedule
    4,
    # Manual recording schedule
    5]
MOTION_DETECTION_SOURCE_DISABLED = -1
MOTION_DETECTION_SOURCE_BY_CAMERA = 0
MOTION_DETECTION_SOURCE_BY_SURVEILLANCE = 1


class Api:
    """An implementation of a Synology SurveillanceStation API."""

    def __init__(self, url, username, password, timeout=10, verify_ssl=True):
        """Initialize a Synology Surveillance API."""
        self._base_url = url + '/webapi/'
        self._username = username
        self._password = password
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._api_info = None
        self._sid = None

        self._initialize_api_info()
        self._initialize_api_sid()

    def _initialize_api_info(self, **kwargs):
        payload = dict({
            'api': 'SYNO.API.Info',
            'method': 'Query',
            'version': '1',
            'query': ','.join(API_NAMES),
        }, **kwargs)
        response = self._get_json(self._base_url + 'query.cgi', payload)

        self._api_info = BASE_API_INFO
        for api in self._api_info.values():
            api_name = api['name']
            api['url'] = self._base_url + response['data'][api_name]['path']

    def _initialize_api_sid(self, **kwargs):
        api = self._api_info['auth']
        payload = dict({
            'api': api['name'],
            'method': 'Login',
            'version': api['version'],
            'account': self._username,
            'passwd': self._password,
            'format': 'sid',
        }, **kwargs)
        response = self._get_json(api['url'], payload)

        self._sid = response['data']['sid']

    def camera_list(self, **kwargs):
        """Return a list of cameras."""
        api = self._api_info['camera']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'List',
            'version': api['version'],
        }, **kwargs)
        response = self._get_json(api['url'], payload)

        cameras = []

        for data in response['data']['cameras']:
            cameras.append(Camera(data, self._video_stream_url))

        return cameras

    def camera_info(self, camera_ids, **kwargs):
        """Return a list of cameras matching camera_ids."""
        api = self._api_info['camera']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'GetInfo',
            'version': api['version'],
            'cameraIds': ', '.join(str(id) for id in camera_ids),
        }, **kwargs)
        response = self._get_json(api['url'], payload)

        cameras = []

        for data in response['data']['cameras']:
            cameras.append(Camera(data, self._video_stream_url))

        return cameras

    def camera_snapshot(self, camera_id, **kwargs):
        """Return bytes of camera image."""
        api = self._api_info['camera']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'GetSnapshot',
            'version': api['version'],
            'cameraId': camera_id,
        }, **kwargs)
        response = self._get(api['url'], payload)

        return response.content

    def camera_event_motion_enum(self, camera_id, **kwargs):
        """Return motion settings matching camera_id."""
        api = self._api_info['camera_event']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'MotionEnum',
            'version': api['version'],
            'camId': camera_id,
        }, **kwargs)
        response = self._get_json(api['url'], payload)

        return MotionSetting(camera_id, response['data']['MDParam'])

    def camera_event_md_param_save(self, camera_id, **kwargs):
        """Update motion settings matching camera_id with keyword args."""
        api = self._api_info['camera_event']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'MDParamSave',
            'version': api['version'],
            'camId': camera_id,
        }, **kwargs)
        response = self._get_json(api['url'], payload)

        return response['data']['camId']

    def _video_stream_url(self, camera_id, video_format='mjpeg'):
        api = self._api_info['video_stream']

        return api['url'] + '?' + urllib.parse.urlencode({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'Stream',
            'version': api['version'],
            'cameraId': camera_id,
            'format': video_format,
        })

    def _get(self, url, payload):
        response = requests.get(url, payload, timeout=self._timeout,
                                verify=self._verify_ssl)

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def _get_json(self, url, payload):
        response = self._get(url, payload)
        content = response.json()

        if 'success' not in content or content['success'] is False:
            raise ValueError('Invalid or failed response', content)

        return content


class Camera:
    """An representation of a Synology SurveillanceStation camera."""

    def __init__(self, data, video_stream_url_provider):
        """Initialize a Surveillance Station camera."""
        self._camera_id = data['id']
        self._name = data['name']
        self._is_enabled = data['enabled']
        self._recording_status = data['recStatus']
        self._video_stream_url = video_stream_url_provider(self.camera_id)

    @property
    def camera_id(self):
        """Return id of the camera."""
        return self._camera_id

    @property
    def name(self):
        """Return name of the camera."""
        return self._name

    @property
    def video_stream_url(self):
        """Return video stream url of the camera."""
        return self._video_stream_url

    @property
    def is_enabled(self):
        """Return true if camera is enabled."""
        return self._is_enabled

    @property
    def is_recording(self):
        """Return true if camera is recording."""
        return self._recording_status in RECORDING_STATUS


class MotionSetting:
    """An representation of a Synology SurveillanceStation motion setting."""

    def __init__(self, camera_id, data):
        """Initialize a Surveillance Station motion setting."""
        self._camera_id = camera_id
        self._source = data['source']

    @property
    def camera_id(self):
        """Return id of the camera."""
        return self._camera_id

    @property
    def is_enabled(self):
        """Return true if motion detection is enabled."""
        return MOTION_DETECTION_SOURCE_DISABLED != self._source
