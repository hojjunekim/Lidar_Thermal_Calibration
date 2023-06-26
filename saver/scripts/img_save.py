#!/usr/bin/env python

import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

# Instantiate CvBridge
bridge = CvBridge()

def image_callback(msg):
    try:
        # Convert your ROS Image message to OpenCV2
        img16 = bridge.imgmsg_to_cv2(msg, "mono16")
        img8 = cv2.normalize(img16, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    except CvBridgeError, e:
        print(e)
    else:
        # Save your OpenCV2 image as a jpeg
        time = msg.header.stamp
        cv2.imwrite('./calib/'+str(time)+'.png', img8)
        print("image saved!")
        rospy.sleep(1)

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    left_topic = "/left/image_raw"
    right_topic = "/right/image_raw"
    # Set up your subscriber and define its callback
    rospy.Subscriber(left_topic, Image, image_callback)
    rospy.Subscriber(right_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()