#!/usr/bin/env python

# ROS Node - Simple Action Client - Turtle

import rospy
import actionlib
import time
import paho.mqtt.client as mqtt

from pkg_task1.msg import msgTurtleAction       # Message Class that is used by ROS Actions internally
from pkg_task1.msg import msgTurtleGoal         # Message Class that is used for Goal messages
from pkg_ros_iot_bridge.msg import msgMqttSub

# flag used to wait for "start" message
flag = False

class SimpleActionClientTurtle:

    # Constructor
    def __init__(self):
        self._ac = actionlib.SimpleActionClient('/action_turtle',
                                                msgTurtleAction)
        self._ac.wait_for_server()
        rospy.loginfo("Action server is up, we can send new goals!")

        param_config_iot = rospy.get_param('config_pyiot')
        self._config_mqtt_server_url = param_config_iot['mqtt']['server_url']
        self._config_mqtt_server_port = param_config_iot['mqtt']['server_port']
        self._config_mqtt_sub_topic = param_config_iot['mqtt']['topic_sub']
        self._config_mqtt_pub_topic = param_config_iot['mqtt']['topic_pub']
        self._config_mqtt_qos = param_config_iot['mqtt']['qos']
        self._config_mqtt_sub_cb_ros_topic = param_config_iot['mqtt']['sub_cb_ros_topic']
        self._config_google_apps_spread_sheet_id = param_config_iot['google_apps']['spread_sheet_id']
        print(param_config_iot)
        broker_url = self._config_mqtt_server_url
        broker_port = self._config_mqtt_server_port
        self.pub_message = ""
        self.pub_topic = self._config_mqtt_pub_topic

        self.pub_client = mqtt.Client()
        self.pub_client.on_publish = self.on_publish
        self.pub_client.connect(broker_url, broker_port)
        #pub_client.on_publish = on_publish
        

    # Function to send Goals to Action Servers
    def send_goal(self, arg_dis, arg_angle):
        
        # Create Goal message for Simple Action Server
        goal = msgTurtleGoal(distance=arg_dis, angle=arg_angle)
        
        '''
            * done_cb is set to the function pointer of the function which should be called once 
                the Goal is processed by the Simple Action Server.

            * feedback_cb is set to the function pointer of the function which should be called while
                the goal is being processed by the Simple Action Server.
        ''' 
        self._ac.send_goal(goal, done_cb=self.done_callback,
                           feedback_cb=self.feedback_callback)
        
        rospy.loginfo("Goal has been sent.")

    def on_publish(self,client, userdata, mid):
        '''print("--- Publisher ---")
        print("[INFO] Topic: {}".format(pub_topic))
        print("[INFO] Message Published: {}".format(pub_message))
        print("------------")'''
        pass

    # Function print result on Goal completion
    def done_callback(self, status, result):
        #publish to MQTT client 
        pub_message = "("+str(result.final_x)+","+str(result.final_y)+","+str(result.final_theta)+")"
        self.pub_client.publish(topic=self.pub_topic, payload=pub_message, qos=0, retain=False)
        
        rospy.loginfo("Status is : " + str(status))
        rospy.loginfo("Result is : " + str(result))
        print("______________Goal____________")

    # Function to print feedback while Goal is being processed
    def feedback_callback(self, feedback):
        rospy.loginfo(feedback)

def func_callback_topic_my_topic(myMsg):
    global flag
    rospy.loginfo("Data Received:" + myMsg.message)
    if myMsg.message == "start":
        flag = True
        


# Main Function
def main():
    global flag
    
    rospy.init_node('node_iot_action_client_turtle')

    obj_client = SimpleActionClientTurtle()
    i = 10
    while True:
        if not flag:
            rospy.Subscriber("/ros_iot_bridge/mqtt/sub", msgMqttSub, func_callback_topic_my_topic)
            print("in loop")
        else:
            break

    obj_client.send_goal(2, 0)
    rospy.sleep(i)

    obj_client.send_goal(2, 60)
    rospy.sleep(i)

    obj_client.send_goal(2, 60)
    rospy.sleep(i)

    obj_client.send_goal(2, 60)
    rospy.sleep(i)
    
    obj_client.send_goal(2, 60)
    rospy.sleep(i)

    obj_client.send_goal(2, 60)
    rospy.sleep(i)
       
    # 4. Loop forever
    rospy.spin()


if __name__ == '__main__':
    main()

