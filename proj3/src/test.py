
#! /usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

def curOrient(msg):
    global curX, curY, curYaw
    curX = msg.pose.pose.position.x
    curY = msg.pose.pose.position.y
    quat = (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
        	msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
    _, _, curYaw = euler_from_quaternion(quat)

def transTurtlebot(xCoor, yCoor):
	twist=Twist()
	pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
	rate = rospy.Rate(10)
	checkGoal = False


	while not checkGoal and not rospy.is_shutdown():
		delX = xCoor - curX
		delY = yCoor - curY
		tarAngle = math.atan2(delY, delX)
		distTar = math.sqrt(delX**2 + delY**2)
	
		if abs(tarAngle - curYaw) > 0.1:
			twist.linear.x = 0.0
			twist.angular.z = tarAngle - curYaw

		else:
			twist.linear.x = min(0.2, distTar)
			twist.angular.z = 0.0

			if distTar < 0.05:
				checkGoal = True
				twist.linear.x = 0.0
				twist.angular.z = 0.0

		pub.publish(twist)
		rate.sleep()

def test(command):
	rospy.init_node('robot_talker',anonymous=True)
	rospy.Subscriber('/odom', Odometry, curOrient)
	xCoor = []
	yCoor = []
	for i in range(0, len(command)-1, 2):
		xCoor.append(command[i])
		yCoor.append(command[i+1])

	for j in range(len(xCoor)):
		transTurtlebot(xCoor[j], yCoor[j])
	
if __name__=='__main__':
	global checkGoal
	checkGoal = False
	curX = 0.0
	curY = 0.0
	curYaw = 0.0

	f = open("./../ros.txt", "r")
	data = f.read()
	val = [float(c) for c in data.strip().replace('\n', ' ').split(' ')]

	test(val)

	rospy.sleep()

	
