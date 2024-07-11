import math
import time

wheelbase = 0.16
wheelRadius = 0.033
prevTime = 0
prevAngularPosition = 0
firstRun = True
start_time = time.time()

def makeModel(rWheelPos, lWheelPos, rWheelVel, lWheelVel):
    global prevTime, prevAngularPosition, dt, firstRun, startLpos, startRpos, positionX, positionY

    if firstRun:
        print("starting model")
        start_time
        dt = 0
        positionX = 0
        positionY = 0
        firstRun = False
        startLpos = rWheelPos
        startRpos = lWheelPos

        return None, None

    currentTime = time.time()
    dt = currentTime - start_time

    rPos = startLpos - rWheelPos
    lPos = startRpos - lWheelPos

    angularPosition = (rPos - lPos)*(wheelRadius/wheelbase)
    
    rLinSpeed = rWheelVel * wheelRadius
    lLinSpeed = lWheelVel * wheelRadius

    if dt == 0:
        angularSpeed = 0
        return None
    else:
        angularSpeed = (angularPosition-prevAngularPosition)/dt

    speedX = (lLinSpeed+angularSpeed*(wheelbase/2))*math.cos(angularPosition)
    speedY = (lLinSpeed+angularSpeed*(wheelbase/2))*math.sin(angularPosition)

    positionX += speedX * dt
    positionY += speedY * dt

    prevAngularPosition = angularPosition
    prevTime = currentTime

def findDirection(angularPosition, Lidar):
    lidar_length = len(Lidar)
    window_size = 22  # Assuming a window size of 22 elements
    if (isinstance(angularPosition, float)):
        print("angularposition " + str(angularPosition)) 
        
        # Calculate the indices for the window around the direction
        start_index = (int(angularPosition) - window_size) % lidar_length
        end_index = (int(angularPosition) + window_size) % lidar_length

        if start_index < end_index:
            # If the window doesn't wrap around, simply slice the Lidar array
            return Lidar[start_index:end_index + 1]
        else:
            # If the window wraps around, concatenate two slices
            return Lidar[start_index:] + Lidar[:end_index + 1]

#Previous implementation for running the DT with Python only
'''
def checkLidar(lidar):
    limit = 10
    n = len(lidar)

    for i in range(n):
        if i == 0:
            if abs(lidar[i] - lidar[i+1]) > limit and abs(lidar[i] - lidar[n-1]) > 10:
                return False
        elif i == n - 1:
             if abs(lidar[i] - lidar[i-1]) > limit and abs(lidar[i] - lidar[0]) > 10:
                return False
        else:
            if abs(lidar[i] - lidar[i-1]) > 10 and abs(lidar[i] - lidar[i+1]) > 10:
                return False
    
    return True

def checkFaultyActualSpeed(actualSpeed):
    if actualSpeed > 2 or actualSpeed < 0:
        print(actualSpeed)
        return False
    return True

def optimizeActualSpeed(actualSpeed, linearX):
    limit = 0.03
    diff = linearX - actualSpeed
    if diff > limit:
        newSpeed = linearX + diff * 0.5
        if newSpeed > 0.22:
            newSpeed = 0.22
        return newSpeed, True
    
    return linearX, False

def safety(lidar, linearX, brakingDist):
    frontLidar = lidar[340:360]+lidar[0:20]
    backLidar = lidar[160:200]

    if linearX > 0:
        for i in range(len(frontLidar)):
            if (lidar[i] < brakingDist):
                print("SAFETY STOP")
                return False
    elif linearX < 0:
        for i in range(len(backLidar)):
            if (lidar[i] < brakingDist):
                print("SAFETY STOP")
                return False

def yesNo(lidar, actualSpeed, linearX, angularZ):
    frontLidar = lidar[340:360]+lidar[0:20]
    closestFront = min(frontLidar)
    n = len(frontLidar)
    
    if (angularZ > 0.0):
        if (closestFront < 0.1):
            return str(linearX) + " , " + str(angularZ)
        else:
            return "0.05, 0.0"
    else:
        return "0.05, 0.0"
    
def calculateAction():
    return
    
'''