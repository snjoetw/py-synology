"""Python Synology SurveillanceStation wrapper."""
from synology.api import (
    Api, MOTION_DETECTION_SOURCE_BY_SURVEILLANCE,
    MOTION_DETECTION_SOURCE_DISABLED,
    HOME_MODE_ON, HOME_MODE_OFF)


class SurveillanceStation:
    """An implementation of a Synology SurveillanceStation."""

    def __init__(self, url, username, password, timeout=10, verify_ssl=True):
        """Initialize a Surveillance Station."""
        self._api = Api(url, username, password, timeout, verify_ssl)
        self._cameras_by_id = None
        self._motion_settings_by_id = None

        self.update()

    def update(self):
        """Update cameras and motion settings with latest from API."""
        cameras = self._api.camera_list()
        self._cameras_by_id = {v.camera_id: v for i, v in enumerate(cameras)}

        motion_settings = []
        for camera_id in self._cameras_by_id.keys():
            motion_setting = self._api.camera_event_motion_enum(camera_id)
            motion_settings.append(motion_setting)

        self._motion_settings_by_id = {
            v.camera_id: v for i, v in enumerate(motion_settings)}

    def get_all_cameras(self):
        """Return a list of cameras."""
        return self._cameras_by_id.values()

    def get_camera(self, camera_id):
        """Return camera matching camera_id."""
        return self._cameras_by_id[camera_id]

    def get_camera_image(self, camera_id):
        """Return bytes of camera image for camera matching camera_id."""
        return self._api.camera_snapshot(camera_id)

    def disable_camera(self, camera_id):
        """Disable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._api.camera_disable(camera_id)

    def enable_camera(self, camera_id):
        """Enable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._api.camera_enable(camera_id)

    def get_motion_setting(self, camera_id):
        """Return motion setting matching camera_id."""
        return self._motion_settings_by_id[camera_id]

    def enable_motion_detection(self, camera_id):
        """Enable motion detection for camera matching camera_id."""
        self._api.camera_event_md_param_save(
            camera_id,
            source=MOTION_DETECTION_SOURCE_BY_SURVEILLANCE)

    def disable_motion_detection(self, camera_id):
        """Disable motion detection for camera matching camera_id."""
        self._api.camera_event_md_param_save(
            camera_id,
            source=MOTION_DETECTION_SOURCE_DISABLED)

    def set_home_mode(self, state):
        """Set the state of Home Mode"""
        state_parameter = HOME_MODE_OFF
        if state:
            state_parameter = HOME_MODE_ON
        return self._api.home_mode_set_state(state_parameter)

    def get_home_mode_status(self):
        """Get the state of Home Mode"""
        return self._api.home_mode_status()
