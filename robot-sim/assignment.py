from __future__ import print_function

import time
from sr.robot import *

R = Robot()

start = True
generate_IdMarker_list = True
pickPlace = True
Markers_id = []     # token code list 

dist_th = 0.40      # threshold of distance for grabbing
dist_rel_th = 0.70  # threshold of distance for releasing
angle_th = 0.7     # threshold of orientation


# Function for driving robot
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function for turning robot
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function return the token code detected into the environment
def create_token_list():
    global id_token

    for token in R.see():
        id_token = token.info.code

    return id_token

# Function for finding information of token 
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

# Function for checking if the token is already released
def checkToken(id, tokenReleased):
    bePresent = False

    for i in range(len(tokenReleased)):
        if id == tokenReleased[i]:
            bePresent = True
        
    return bePresent
        

# MAIN
while start:

    # Scan tokens into the environment and create the list
    while generate_IdMarker_list:

        isEqual = True
        turn(20, 0.1)
        id_token = create_token_list()
        
        # Case of the first token detected
        if len(Markers_id) == 0:
            Markers_id.append(id_token)
            first_token = id_token

        # Check if the token code was already detected and break while loop
        for i in range(len(Markers_id)):
            if Markers_id[i] == id_token:
                isEqual = False
            
            elif (first_token == id_token and len(Markers_id) != 1):
                generate_IdMarker_list = False

        if isEqual == True:
            Markers_id.append(id_token)

    
    # Define the load zone (code = 38) and an empty list for saving the released token
    element_num = len(Markers_id)   # Get number of elements in the Markers_id list
    base = min(Markers_id)          # Declare the load zone
    tokenReleased = []              # List for token released
    tokenReleased.append(base)


    # Pick and place token
    while pickPlace:
        
        # if the length of tokenReleased list is equal to Marker_id list break while loop
        if len(tokenReleased) == element_num:
            print('All tokens are located in the load zone')
            start = False
            break

        # Get list with info of token detected
        arrInfo = find_token()
        
        if len(arrInfo) != 0:
            for i in range(int(len(arrInfo)/3)):

                # Cicle the all token code in the list
                id_token = arrInfo[i+(2*i)]

                # Check if this token is already released
                check = checkToken(id_token, tokenReleased)

                # If the token code is not into released list, it's possible to define the variable for this specific token detected
                if check == False:
                    id_token = arrInfo[i+(2*i)]
                    dist = arrInfo[i+(2*i)+1]
                    rot_y = arrInfo[i+(2*i)+2]

        dist = round(dist, 2)
        rot_y = round(rot_y, 1)

        # If I can't find any token, the robot turns
        if len(arrInfo) == 0:
            print('I can not see any token')
            turn(20, 0.5)

        # If the robot see token in the load zone, it must carry on to turn
        elif check == True:
            print('This token is already in the load zone')
            turn(20, 0.5)

        # If the robot is well aligned with the token, it goes forward
        elif -angle_th <= rot_y <= angle_th:
            print('Here we go')
            drive(30, 0.1)

            # If the distance is quite close to the token, the robot can grab it
            if dist < dist_th:
                print('Grab token')
                if R.grab():
                    print('Got it!')

                    # Save token_id into a tokenReleased[] for taking in mind what robot have done
                    tokenReleased.append(id_token)

                    # Go to the load zone
                    while True:

                        # Find the load zone
                        arrInfo_w = find_token()
                        id_token_w = 0
                        dist_w = 0
                        rot_y_w = 0

                        # Check the code = 38, means check if the load zone is visible
                        for i in range(len(arrInfo_w)):
                            if arrInfo_w[i] == base:
                                id_token_w = arrInfo_w[i]
                                dist_w = arrInfo_w[i+1]
                                rot_y_w = arrInfo_w[i+2] 

                        distance = round(dist_w, 2)
                        angle = round(rot_y_w, 1)

                        # If the robot can't see the load zone, it turns
                        if id_token_w != base:
                            print('I can not see the load zone')
                            turn(20, 0.5)

                        # If the robot is well aligned with the load zone, it goes forward
                        elif ((-angle_th <= angle <= angle_th) and id_token_w == base):
                            print('Here we go')
                            drive(30, 0.1)

                            # If the distance is quite close to the load zone, the robot can release the token
                            if ((distance < dist_rel_th) and (id_token_w == base)):
                                if R.release():
                                    print('Release token')
                                    drive(-20, 2)
                                    break

                        # If the robot is not well aligned with the load zone, it moves on the left or on the right
                        elif ((angle < -angle_th) and id_token_w == base):
                            print('Turn left')
                            turn(-1, 0.4)

                        elif ((angle > angle_th) and id_token_w == base):
                            print('Turn right')
                            turn(1, 0.4)
            
            
        # If the robot is not well aligned with the token, it moves on the left or on the right
        elif rot_y < -angle_th:
            print('Turn left')
            turn(-1, 0.4)

        elif rot_y > angle_th:
            print('Turn right')
            turn(1, 0.4)
