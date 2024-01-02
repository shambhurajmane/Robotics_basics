# 2.ROS_quat_to_eular
##Purpose
A node that converts quaternion representations to Euler angles representations.
##Description:
Here I have created a subscriber as follows.
The subscriber will receive the message published on "/quat_topic" in quaternion
representations in terms of array of float values. Which then will be converted into Euler
angles representations.
##How to build and run tests
Open a new terminal and source your ROS 2 installation so that ros2 commands will
work.
ros2 run quat_to_euler quat_subscriber
ros2 topic pub --once /quat_topic std_msgs/msg/Float32MultiArray
"{data:0.7071,0.0,0.7071,0.0]}"
##Required dependencies to be added in package.xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
##Required entry points to be added in setup.py
entry_points={
'console_scripts': [
'quat_subscriber = quat_to_euler.quat_2_eular:main'
],
},
##Working of nodes
1. I have created one nodes, which is "quat_subscriber"
2. "subscription" subscribes to the topic "quat_topic" and fetches the message data
of type Float32MultiArray. Data from the quat_topic is accessed in the callback
function "quat_callback".
3. Received quaternion representations data is then accessed and converted into
euler angles representation and printed on the terminal as roll, pitch and yaw
values.
4. Message type : Float32MultiArray (imported from std_msgs directory)
5. Topic name : quat_topic
6. Callback function : quat_callback
7. Queue size: 10