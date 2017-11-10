# py-synology [![Build Status](https://travis-ci.org/snjoetw/py-synology.svg?branch=master)](https://travis-ci.org/snjoetw/py-synology)
Python API for Synology Surveillance Station.  This is used in [Home Assistant](https://home-assistant.io) but should be generic enough that can be used elsewhere.


## Install

```bash
pip install py-synology
```


## Usage
```python
from synology.surveillance_station import SurveillanceStation

# Synology API url
api_url = 'https://localhost:5001'
username = 'USERNAME'
password = 'PASSWORD'
# Verify SSL certificate or not, default true 
verify_ssl = False
# Timeout in seconds, default 10
timeout = 10

# Instantiates SurveillanceStation
# This will call Synology API to get SID (session ID), fetch all the cameras/motion settings and cache them
surveillance = SurveillanceStation(api_url, username, password, verify_ssl=verify_ssl, timeout=timeout)

# Returns a list of cached cameras available
cameras = surveillance.get_all_cameras()

# Assuming there's at least one camera, get the first camera_id
camera_id = cameras[0].camera_id

# Returns cached camera object by camera_id
camera = surveillance.get_camera(camera_id)

# Returns cached motion setting object by camera_id
motion_setting = surveillance.get_motion_setting(camera_id)

# Return bytes of camera image
surveillance.get_camera_image(camera_id)

# Updates all cameras/motion settings and cahce them
surveillance.update()
```


## Data Model

### Camera

A representation of a Synology SurveillanceStation camera

| Property         | Description                    |
| ---------------- | ------------------------------ |
| camera_id        | id of the camera               |
| name             | name of the camera             |
| video_stream_url | video stream url of the camera |
| is_enabled       | true if camera is enabled      |
| is_recording     | true if camera is recording    |


### MotionSetting

A representation of a Synology SurveillanceStation motion setting

| Property         | Description                    |
| ---------------- | ------------------------------ |
| camera_id        | id of the camera               |
| is_enabled       | true if motion detection is enabled |


## Reference

[Surveillance Station API v2.7](https://global.download.synology.com/download/Document/DeveloperGuide/Surveillance_Station_Web_API_v2.7.pdf)
