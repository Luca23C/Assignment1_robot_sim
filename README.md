# Assignment 1 - Robotic Simulator

The aim of this assignment was to develop a Python code to control a robot within an arena, with the goal of putting all the boxes together. The area where they should be grouped could be arbitrary.

The following picture shows the environment:

<img src="https://github.com/Luca23C/Assignment1_robot_sim/assets/97911589/3dc09cd4-5d77-479d-8372-d27511e34936" width="400" height="400">


## Flowchart
-----------------------------

For developing any kind of code, it is useful to start with Pseudocode or Flowchart. These tools enable to design information and action related to each process that need to be executed in order to achieve the goal. For this type of work, it was choosen the flowchart rapresentation for showing each process:

<img src="https://github.com/Luca23C/Assignment1_robot_sim/assets/97911589/f594a219-9635-4cbb-b98b-b4134f8fa58e" width="800" height="800">


## How to run
-----------------------------
First of all it is necessary to clone this repository inside your workspace, into your local machine, by using the following command:

```bash
$ git clone https://github.com/Luca23C/Assignment1_robot_sim.git
```

Now navigate trought the folders by using:

```bash
$ cd <your_workspace>/python_simulator/robot-sim
```

Finally it is possible to run this project by typing this line:

```bash
$ python3 run.py assignment.py
```

## Functions developed

In this section, it will be explained all functions developed for this project.

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output. The left motor is connected to output `0` and the right motor to output `1`.

In this case, it was developed two different functions called: `drive()` and `turn()`. Each function requires as input the speed and the duration (expressed in seconds) that it provides to the robot.
The `drive()` function enables steering the robot either forward or backward and the `turn()` function allows to turning the robot.
For these funcitons , i

Here it was reported the `drive()` function:

```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
In case of `turn()` function, there is a specific difference: one of motor needs a minus in front of its speed.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/


### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.
