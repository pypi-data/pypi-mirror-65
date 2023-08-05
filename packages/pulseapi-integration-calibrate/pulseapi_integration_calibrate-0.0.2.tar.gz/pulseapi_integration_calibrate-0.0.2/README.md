## Rounding motion for robot Pulse by Rozum Robotics

### Requirements
Python 3.6+

pulse-api (pip3 install pulse-api -i https://pip.rozum.com/simple)

pulseapi-integration (pip3 install pulseapi-integration)

### Installation
To get the latest version, use the following command:

**pip install pulseapi-integration-calibrate**


### Getting started
Examples use the latest version of the library.
#### Quickstart

```python
from pulseapi_integration_calibrate.plane import calibrate_reference_frame
from pulseapi_integration import *

host = "192.168.1.33:8081"
robot = NewRobotPulse(host)

CALIBRATE_FRAME_3P_P1_ORIGIN = 1 

M1 = [x1,y1,z1]
M2 = [x2,y2,z2]
M3 = [x3,y3,z3]

frame = calibrate_reference_frame([M1,M2,M3], method = CALIBRATE_FRAME_3P_P1_ORIGIN)
robot.set_reference_frame(position(frame[0],frame[1]))
```

#### New function:

_calibrate_reference_frame(points,method)_

Return calibrate frame

**_Points definition:_**

If method = CALIBRATE_FRAME_3P_P1_ORIGIN, then set points as in the image

![points](Three-points-in-part-coordinate-system.png)

_**Methods:**_

CALIBRATE_FRAME_3P_P1_ON_X = 0  # Calibrate by 3 points: [X, X+, Y+] (p1 on X axis)

CALIBRATE_FRAME_3P_P1_ORIGIN = 1  # Calibrate by 3 points: [Origin, X+, XY+] (p1 is origin)

CALIBRATE_FRAME_6P = 2  # Calibrate by 6 points

**Important!**

Now only CALIBRATE_FRAME_3P_P1_ORIGIN method works


