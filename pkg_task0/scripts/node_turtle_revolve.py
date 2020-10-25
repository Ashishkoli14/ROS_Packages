#!/usr/bin/env python

# import libraries
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math


# Callback function
def pose_callback(msg):
    pass


def main():
    # node initialization.
    rospy.init_node('node_turtle_revolve', anonymous=True)

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', 
                                          Twist, queue_size=10)
    vel_msg = Twist()
    
    # angular velocity
    ang_vel = 1.0
    
    # components of vel_msg
    vel_msg.linear.x = 1.0
    vel_msg.angular.z = ang_vel

    var_loop_rate = rospy.Rate(1)
    
    # recording the starting time.
    start_time = time.time()
    # subscribe to topic /turtle/pose
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

    while not rospy.is_shutdown():
        # recording the stop time
        end_time = time.time()
        dist_traveled = ang_vel * (end_time - start_time)
        rospy.loginfo("Distance Traveled = {}".format(dist_traveled))
        
        # Stop the turtle after completing one revolution
        if dist_traveled >= (2*math.pi):
		    vel_msg.linear.x = 0.0
		    vel_msg.angular.z = 0.0
		    break
        else:
            velocity_publisher.publish(vel_msg)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

