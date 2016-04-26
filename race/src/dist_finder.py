#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input
from datetime import datetime


desired_trajectory = 1
vel = 30
prev_time = 0

pub = rospy.Publisher('error', pid_input, queue_size=10)

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
	rad = math.radians(theta) - pi/2 - data.angle_min
	idx = int(round(rad/data.angle_increment))
	return data.ranges[idx]

def callback(data):
	theta = 50;
	a = getRange(data,theta)
	b = getRange(data,0)
	swing = math.radians(theta)
	
	## Your code goes here

	print("dist[0]", b)
	print("dist[50]", a)
	current_time = datetime.now()

	AC = vel * current_time - previous_time
	alpha = math.atan(((a * math.cos(theta)) - b)/(a * math.sin(theta)))
	AB = b * math.cos(alpha)
	CD = AB + (AC * math.sin(alpha))

	## END

	error = CD - 1



	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	pub.publish(msg)
	
	prev_time = current_time

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()