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
from math import pi
from pulseapi_integration import *
from pulseapi_integration_rounding_motion.rounding_motion import rounding_motion

host = "192.168.1.33:8081"
robot = NewRobotPulse(host)

SPEED = 20

x = -0.58
y = -0.20
z = 0.155
robot.set_reference_frame(position([x, y, z], [0, 0, 0]))

targets = [
    [position([0.015, 0.072, 0.1], [pi, 0, 0])],
    [position([0.015, 0.08, 0.1], [pi, 0, 0], [output_action(1, SIG_HIGH)])],
    [position([0.015, 0.09, 0.1], [pi, 0, 0])],
    
    [position([0.015, 0.1234, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.0277, 0.1234, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.0277, 0.135, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.1300, 0.135, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.1300, 0.1234, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.142, 0.1234, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.1425, 0.1345, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.2458, 0.135, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.2458, 0.1234, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.2585, 0.1234, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.26, 0.0266, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.2473, 0.0266, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.2483, 0.015, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.144, 0.0137, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.144, 0.0261, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.132, 0.0261, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.132, 0.0145, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.0287, 0.015, 0.1], [pi, 0, 0]), [0.003]],
    [position([0.0287, 0.0266, 0.1], [pi, 0, 0]), [0.006]],
    [position([0.016, 0.0266, 0.1], [pi, 0, 0]), [0.003]],

    [position([0.015, 0.0296, 0.1], [pi, 0, 0])],
    [position([0.015, 0.04, 0.1], [pi, 0, 0], [output_action(1, SIG_LOW)])],
    [position([0.015, 0.08, 0.1], [pi, 0, 0])]
]

home_pose = pose([0, -90, 0, -90, -90, 0])
start_pose = pose([0, -90, 90, -90, -90, 0])

robot.set_pose(home_pose, speed=20)
robot.set_pose(start_pose, speed=20)

robot.run_positions(rounding_motion(targets), speed=SPEED, motion_type=MT_LINEAR)
robot.set_pose(start_pose, speed=20)
```

#### New function:

_rounding_motion(targets)_

Return new_target_list with angle rounding

**_Target parameters:_**
[position([x, y, z], [r, p, y], [action]), [rounding_radius_in_meters]]

**Important!** 
A list of points must consist of three or more points.
There should be no rounding radius at the first and last point.



