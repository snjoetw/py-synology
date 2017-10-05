# py-synology
Python API for Synology Surveillance Station


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
verify_ssl = false
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
