#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input

global kp
global kd
global prev_error
global vel_input
kp = 14.0
kd = 0.09
prev_error = 0.0 
vel_input = 25.0
servo_offset = 18.5
angle = 0

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)


def clamp(num):
	if num < -100:
		return -100
	elif num > 100:
		return 100
	
	return num

def control(data):


	## Your code goes here
	# 1. Scale the error
	# 2. Apply the PID equation on error
	# 3. Make sure the error is within bounds
 	
 	error = data.error
 	vel_input = data.velocity
 	v_theta = clamp(kp * error + kd * (prev_error - error))
 	angle -= v_theta

	## END

	msg = drive_param();
	msg.velocity = vel_input	
	msg.angle = angle
	pub.publish(msg)

if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	kp = input("Enter Kp Value: ")
	kd = input("Enter Kd Value: ")
	vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()
