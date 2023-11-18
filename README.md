# Assignment 1 - Robot Simulator

The following picture shows the environment of this assignment:

<img src="https://github.com/Luca23C/Assignment1_robot_sim/assets/97911589/3dc09cd4-5d77-479d-8372-d27511e34936" width="400" height="400">


The aim of this assignment was to create a Python node to control a robot inside the arena, aiming to gather all the boxes in a specific area. The area where the boxes should be grouped could be arbitrary and for this project it was called 'load zone'.


## Flowchart

For developing any kind of code, it is useful to start with Pseudocode or Flowchart. These tools enable to design information and action related to each process that need to be executed in order to achieve the goal.

For this type of work, it was choosen the flowchart rapresentation for showing each process:

<img src="https://github.com/Luca23C/Assignment1_robot_sim/assets/97911589/f594a219-9635-4cbb-b98b-b4134f8fa58e" width="800" height="800">


## Functions developed

In this section, it will be explained all functions developed for this project.

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output. The left motor is connected to output `0` and the right motor to output `1`.

In this case, it was developed two different functions called: `drive()` and `turn()`. Each function requires as input the speed and the duration (expressed in seconds) that it provides to the robot.
The `drive()` function enables steering the robot either forward or backward and the `turn()` function allows to turning the robot.

Here it was shown the `drive()` function:

```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
In case of `turn()` function, there is a specific difference: one of motor needs a minus in front of its speed.

### Vision

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

For this project it was considered only three attributes: `code`, `dist` and `rot_y`.

The `R.see` method it was employed inside two functions called: `create_token_list()` and `find_token()`.
The first one, it was developed for collecting all tokens in the arena. In fact `create_token_list()` return as output the `code` of marker seen during the first process. The first process involves the robot turning and the function `create_token_list()` is called until the `code` observed matches the first `code` detected by the robot.

Here this function was shown:

```python
def create_token_list():
    global id_token

    for token in R.see():
        id_token = token.info.code

    return id_token
```

The `find_token()` function was developed and employed inside the 'Pick and Place' process. This function build a list, where each element detected has three specific value: `code`, `dist` and `rot_y`. So if robot is eable to see two different token, inside the list there are six values. Finally the function return as output this specific list of values.

Here this function was shown:

```python
def find_token():
    mat = []
    for token in R.see():
        dist = token.dist
        rot_y = token.rot_y
        id_token = token.info.code
        
        mat.append(id_token)
        mat.append(dist)
        mat.append(rot_y)

    return mat
```

It was developed another function that work with `find_token()` and its name is: `checkToken()`.
The `checkToken()` function needs as input the `code` and a list called 'tokenReleased' that contain all token released in the load zone. The `code` was given by the `find_token()` function.
This developed function checks if the detected token has already been released in the load zone and it returns a boolean value, where `True` means that the token is already in the load zone, while `False` indicates the opposite.

Here this function was shown:

```python
def checkToken(id, tokenReleased):
    bePresent = False

    for i in range(len(tokenReleased)):
        if id == tokenReleased[i]:
            bePresent = True
        
    return bePresent
```

### Grabber

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, it was called the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token in the load zone, it was called the `R.release` method.

```python
success = R.release()
```

## How to run

IMPORTANT: This project was developed with python3.8 version.

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
$ python3.8 run.py assignment.py
```