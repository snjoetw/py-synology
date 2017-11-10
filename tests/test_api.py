"""The tests for the Canary sensor platform."""
import os
import unittest

import requests_mock

from synology.api import Api

BASE_URL = "http://192.168.1.8:5000"
QUERY_URL = BASE_URL + "/webapi/query.cgi"
AUTH_URL = BASE_URL + "/webapi/auth.cgi"
CAMERA_URL = BASE_URL + "/webapi/entry.cgi"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(path) as fptr:
        return fptr.read()


def _setup_responses(mock):
    mock.register_uri(
        "GET",
        QUERY_URL,
        text=load_fixture("api_query.json"))

    mock.register_uri(
        "GET",
        AUTH_URL,
        text=load_fixture("api_auth.json"))

    mock.register_uri(
        "GET",
        CAMERA_URL,
        text=load_fixture("api_camera.json"))


class TestApi(unittest.TestCase):
    @requests_mock.Mocker()
    def test_cameras(self, mock):
        """Test the Canary senskor class and methods."""
        _setup_responses(mock)
        api = Api(BASE_URL, "user", "pass")
        cameras = api.camera_list()

        self.assertEqual(2, len(cameras))

        for camera in cameras:
            if camera.name == "Laundry Room Cam":
                self.assertEqual(1, camera.camera_id)
                self.assertTrue("cameraId=1" in camera._video_stream_url)
                self.assertEqual(True, camera.is_enabled)
                self.assertEqual(True, camera.is_recording)
            elif camera.name == "Family Room Cam":
                self.assertEqual(2, camera.camera_id)
                self.assertTrue("cameraId=2" in camera._video_stream_url)
                self.assertEqual(False, camera.is_enabled)
                self.assertEqual(True, camera.is_recording)
