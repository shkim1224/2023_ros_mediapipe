#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
import rospy
from std_msgs.msg import String
import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture(0) #'PoseVideos/sample-mp4-file.mp4')
pTime = 0
detector = pm.poseDetector()
pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.imshow("Image", img)
    send_str = "detected position %s" % str(lmList[14])
    rospy.loginfo(send_str)
    pub.publish(send_str)
    rate.sleep()
    cv2.waitKey(1)
    


