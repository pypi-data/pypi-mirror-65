## Rounding motion for robot Pulse by Rozum Robotics

### Requirements
Python 3.6+

pulse-api (pip3 install pulse-api -i https://pip.rozum.com/simple)

pulseapi-integration (pip3 install pulseapi-integration)

### Installation
To get the latest version, use the following command:

**pip install pulseapi-integration-rounding-motion**


### Getting started
Examples use the latest version of the library.
#### Quickstart

```python

```

#### New function:

_rounding_motion(targets)_

Return new_target_list with angle rounding

**_Target parameters:_**
[position([x, y, z], [r, p, y], [action]), [rounding_radius_in_meters]]

**Important!** 
A list of points must consist of three or more points.
There should be no rounding radius at the first and last point.



