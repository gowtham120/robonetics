#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

class VelocityPublisher:
    def __init__(self):
        rospy.init_node('velocity_publisher_node', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/run', Bool, self.run_callback)
        self.running = False
        self.start_time = None
        self.rate = rospy.Rate(10)  # 10hz

    def run_callback(self, msg):
        try:
            rospy.loginfo(f"Received /run message: {msg.data}")
            if msg.data and not self.running:
                self.running = True
                self.start_time = rospy.Time.now()
                rospy.loginfo("Started running")
        except Exception as e:
            rospy.logerr(f"Exception in run_callback: {e}")

    def publish_velocity(self):
        while not rospy.is_shutdown():
            if self.running and self.start_time is not None:
                elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
                if elapsed_time <= 5:
                    self.publish_twist(0.4, 0.0)
                else:
                    self.publish_twist(0.0, 0.0)
                    self.running = False
            self.rate.sleep()

    def publish_twist(self, linear_x, angular_z):
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        rospy.loginfo(f"Publishing linear.x: {linear_x}, angular.z: {angular_z}")
        self.pub.publish(twist)

if __name__ == '__main__':
    try:
        velocity_publisher = VelocityPublisher()
        velocity_publisher.publish_velocity()
    except rospy.ROSInterruptException:
        pass

