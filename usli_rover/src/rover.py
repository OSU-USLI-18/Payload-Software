#!/usr/bin/python2

import rospy
import tf 
from tf.transformations import euler_from_quaternion
import message_filters
import math

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

globalOdom = Odometry()
obstableAvoidanceThreshold = 2.0

def initTwist():
    command = Twist()

    command.linear.x = 0.0
    command.linear.y = 0.0
    command.linear.z = 0.0
    command.angular.x = 0.0
    command.angular.y = 0.0
    command.angular.z = 0.0

    return command

def shutdownRoutine():
    print("deploying solar panels...")

    #activate solar servos

    print("finished deploying solar panels...")

def getEuler():
    odom = Odometry()
    # find current orientation of robot based on odometry (quaternion coordinates)
    xOr = odom.pose.pose.orientation.x
    yOr = odom.pose.pose.orientation.y
    zOr = odom.pose.pose.orientation.z
    wOr = odom.pose.pose.orientation.w

    # find orientation of robot (Euler coordinates)
    (roll, pitch, yaw) = euler_from_quaternion([xOr, yOr, zOr, wOr])
    return (roll, pitch, yaw)

def getCurrentCoor():
    odom = Odometry()

    currX = odom.pose.pose.position.x
    currY = odom.pose.pose.position.y

    return (currX,currY)


def callback(scan,odom):

    # find laser scanner properties (min scan angle, max scan angle, scan angle increment)
    #http://docs.ros.org/api/sensor_msgs/html/msg/Range.html
    sensorMaxAngle = scan.angle_max
    sensorMinAngle = scan.angle_min
    angleIncrement = scan.angle_increment

    defualtVelocity = 5.0
    newBearing = 0.0


    #only read scans left to right in the givin angle increments
    minimumScannedDistance = scan.range_max
    scanTheta = sensorMinAngle
    for currentScan in scan.ranges:
        if scanTheta > (-math.pi)/2 and scanTheta < 0 and currentScan < obstableAvoidanceThreshold:
            newBearing = 1.0 #turn left
        elif scanTheta < (math.pi)/2 and scanTheta >= 0 and currentScan < obstableAvoidanceThreshold:
            newBearing = -1.0 #turn right
        
        if currentScan < minimumScannedDistance:
            minimumScannedDistance = currentScan

        scanTheta += angleIncrement

    newMovementCommand = initTwist()
    newMovementCommand.linear.x = defualtVelocity * min(1.0, minimumScannedDistance/obstableAvoidanceThreshold)
    newMovementCommand.angular.z = newBearing

    roverPublish.publish(newMovementCommand)

            

if __name__ == "__main__":
    rospy.init_node('rover', disable_signals=False, log_level=rospy.DEBUG)
    rospy.on_shutdown(shutdownRoutine)

    # subscribe to laser scan message
    sub = message_filters.Subscriber('base_scan', LaserScan)

    # subscribe to odometry message    
    sub2 = message_filters.Subscriber('odom', Odometry)

    # synchronize laser scan and odometry data
    ts = message_filters.TimeSynchronizer([sub, sub2], 10)
    ts.registerCallback(callback)

    roverPublish = rospy.Publisher('cmd_vel',Twist)

    rospy.spin()