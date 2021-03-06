#!/usr/bin/env python3
# Parameters are taken from http://www.inase.org/library/2015/vienna/bypaper/MECH/MECH-13.pdf
import numpy as np
import roslib
import rospy
from realsense_perception.msg import DetectedObject, DetectedObjectsArray
# Values of theta should be obtained in real-time, here they are used for a sample case so they are fixed
theta1 =35.583455 
d1 = 0
a1 = 0.075
alpha1 = np.pi / 2.0

theta2 = -53.747694
d2 = 0
a2 = 0.3
alpha2 = 0

theta3 = -55.641353 
d3 = 0
a3 = 0.075
alpha3 = np.pi / 2.0

theta4 = -0.003467 
d4 = 0.32
a4 = 0 
alpha4 = -np.pi / 2.0

theta5 =  -0.008734
d5 = 0
a5 = 0 
alpha5 = np.pi / 2.0 

theta6 =  0.004491
d6 =0.08
a6 = 0
alpha6 = 0

T01 = np.array([[np.cos(theta1),0,np.sin(theta1),a1*np.cos(theta1)],
				[np.sin(theta1),0,-np.cos(theta1),a1*np.sin(theta1)],
				[0,1,0,0],
				[0,0,0,1]])

T12 = np.array([[np.cos(theta2),-np.sin(theta2),0,a2*np.cos(theta2)],
				[np.sin(theta2),np.cos(theta2),0,a2*np.sin(theta2)],
				[0,0,1,0],
				[0,0,0,1]])

T23 = np.array([[np.cos(theta3),0,np.sin(theta3),a3*np.cos(theta3)],
				[np.sin(theta3),0,-np.cos(theta3),a3*np.sin(theta3)],
				[0,1,0,0],
				[0,0,0,1]])

T34 = np.array([[np.cos(theta4),0,-np.sin(theta4),0],
				[np.sin(theta4),0,np.cos(theta4),0],
				[0,-1,0,d4],
				[0,0,0,1]])

T45 = np.array([[np.cos(theta5),0,np.sin(theta5),0],
				[np.sin(theta5),0,-np.cos(theta5),0],
				[0,1,0,0],
				[0,0,0,1]])

T56 = np.array([[np.cos(theta6),0,-np.sin(theta6),0],
				[np.sin(theta6),0,np.cos(theta6),0],
				[0,0,1,d6],
				[0,0,0,1]])

T06 = T01.dot(T12).dot(T23).dot(T34).dot(T45).dot(T56)

# End effector pose relative to the 
px = T06[0,3]
py = T06[1,3]
pz = T06[2,3]



def callback(data):
	count = data.count
	detected = data.detectedObjects
	length = len(detected) 
	i = 0
	while i < length:
		obj_x = detected[i].x
		obj_y = detected[i].y
		obj_z = detected[i].z

		# X and Y axes for robot are rotated
		obj_x = obj_x + py
		obj_y = obj_y+ px
		obj_z = obj_z +pz
		print(detected[i].ClassName+" "+"\n x="+str(obj_x)+"\n y="+str(obj_y)+"\n z="+str(obj_z))
		data.detectedObjects[i].x = obj_x
		data.detectedObjects[i].y = obj_y
		data.detectedObjects[i].z = obj_z
		pub.publish(data)
		i += 1
	
	

rospy.init_node('coordinate_transformer')
rospy.Subscriber("Objects", DetectedObjectsArray, callback)
pub = rospy.Publisher('TransformedObjects', DetectedObjectsArray, queue_size=10)
while(1):
	rospy.spin()
