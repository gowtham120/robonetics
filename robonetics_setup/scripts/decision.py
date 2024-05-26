#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class decision_making:
    def __init__(self):
        self.vel_pub = rospy.Publisher('/cmd_vel_final', Twist, queue_size=10)
        self.vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.vel_callback)
        self.bool_sub = rospy.Subscriber('/flag', Bool, self.bool_callback)
        self.publish_vel_flag = True

    def vel_callback(self, msg):
        if self.publish_vel_flag == True:    # for True
            stop_msg = Twist()
            stop_msg.linear.x = 0
            stop_msg.angular.z = 0
            self.vel_pub.publish(stop_msg)
            rospy.loginfo("Publishing Zeros")

        else:                         # for False
            self.vel_pub.publish(msg)
            rospy.loginfo("Publishing velocity commands")
    
    def bool_callback(self, bool_msg):
        self.publish_vel_flag = bool_msg.data
        rospy.loginfo(f"Assigining Bool data: {bool_msg.data}")

        if self.publish_vel_flag == True:    # for True
            stop_msg = Twist()
            stop_msg.linear.x = 0
            stop_msg.angular.z = 0
            self.vel_pub.publish(stop_msg)
            rospy.loginfo("Publishing Zeros")



if __name__ == '__main__':
    rospy.init_node('decision_making')
    decision_making()
    rospy.spin()

