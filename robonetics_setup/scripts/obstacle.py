#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan

def callback(msg):
    #print(msg.ranges)
    if (min(msg.ranges) < 2):
        print( " stop " )
        bool_msg = Bool()
        bool_msg.data = True
        rospy.loginfo(f"Publishing: {bool_msg.data}")
        obstacle_pub.publish(bool_msg)
    else:
        print( " go " )
        bool_msg = Bool()
        bool_msg.data = False
        rospy.loginfo(f"Publishing: {bool_msg.data}")
        obstacle_pub.publish(bool_msg)
    
def scan_listener():


    rospy.Subscriber("scan", LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('scan_listener', anonymous=True)
    rate = rospy.Rate(10)    
    obstacle_pub = rospy.Publisher('/flag', Bool, queue_size=10)
    scan_listener()
    
    

