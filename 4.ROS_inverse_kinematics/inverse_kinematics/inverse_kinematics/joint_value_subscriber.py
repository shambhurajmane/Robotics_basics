

import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Pose
from std_msgs.msg import Float32MultiArray


class QuatSubscriber(Node):

    def __init__(self):
        super().__init__('joint_value_subscriber')
        self.subscription1 = self.create_subscription(
            Float32MultiArray,
            'joint_value_topic',
            self.joint_value_callback,
            10)
        self.subscription1  # prevent unused variable warning

        self.subscription2 = self.create_subscription(
            Pose,
            'pose_topic',
            self.pose_callback,
            10)
        self.subscription2 

    def joint_value_callback(self, msg):
        #Accessing the published message 
        q1=msg.data[0]
        q2=msg.data[1]
        q3=msg.data[2]

        #Assume link lengths
        l1=5
        l2=5
        l3=5

        #Homogeneous matrix: Rotation matrix values
        r11= math.cos(q1)*math.cos(q2)*math.cos(q3)-math.cos(q1)*math.sin(q2)*math.sin(q3) 
        r21= math.sin(q1)*math.cos(q2)*math.cos(q3)-math.sin(q1)*math.sin(q2)*math.sin(q3)
        r31= -math.sin(q2)*math.cos(q3)-math.cos(q2)*math.sin(q3)
        r12= -math.cos(q1)*math.cos(q2)*math.sin(q3)-math.cos(q1)*math.sin(q2)*math.cos(q3)
        r22= -math.sin(q1)*math.cos(q2)*math.sin(q3)-math.sin(q1)*math.sin(q2)*math.cos(q3)
        r32= math.sin(q2)*math.sin(q3)-math.cos(q2)*math.cos(q3)
        r13= -math.sin(q1)
        r23= math.cos(q1)
        r33= 0 


        #x, y, z values for end effector pose orientation
        dx = l3*math.cos(q1)*math.cos(q2)*math.cos(q3)-l3*math.cos(q1)*math.sin(q2)*math.sin(q3)+l2*math.cos(q1)*math.cos(q2) 
        dy = l3*math.sin(q1)*math.cos(q2)*math.cos(q3)-l3*math.sin(q1)*math.sin(q2)*math.sin(q3)+l2*math.sin(q1)*math.cos(q2)  
        dz = -l3*math.sin(q2)*math.cos(q3)-l3*math.cos(q2)*math.sin(q3)+l1-l2*math.sin(q2)  
        print("Forward Kinematics topic")
        print("end effector pose orientation values are x:"+ str(dx) + ", y:" + str(dy) + ", z:" + str(dz))

        #values in quaternian 
        q_w= 0.5 * math.sqrt(1 + r11 + r22 + r33)
        q_x= (r32 - r23) / (4 * q_w) 
        q_y= (r13 - r31) / (4 * q_w)
        q_z= (r21 -r12) / (4 * q_w)

        # #roll, pitch, yaw values for end effector pose orientation
        # roll= math.atan2(2*(q_w*q_x + q_y*q_z), 1 - 2*(q_x*q_x + q_y*q_y))
        # pitch= math.asin(2*(q_w*q_y - q_x*q_z))
        # yaw= math.atan2(2*(q_w*q_z + q_x*q_y), 1 - 2*(q_y*q_y+ q_z*q_z))
        

        print("end effector pose orientation values are x: "+ str(q_x) + ", y: " + str(q_y) + ", z: " + str(q_z) + ", w:" + str(q_w)+"\n")
        
    def pose_callback(self, msg):
        #Accessing the published message 

        xc=msg.position.x
        yc=msg.position.y
        zc=msg.position.z
        q_w= msg.orientation.w
        q_x= msg.orientation.x
        q_y= msg.orientation.y
        q_z= msg.orientation.z




        #Assume link lengths
        l1=5
        l2=5
        l3=5

        print("Inverse Kinematics 4 possible answers are:")
        try:

            for i in [0,math.pi]:
                q1=i + math.atan2(yc,xc)
                for i in [1,-1]:
                    cosq3= ((xc*xc+yc*yc)+(zc-l1)*(zc-l1)-l2*l2-l3*l3) / (2*l2*l3)
                    q3=math.atan2(i*math.sqrt(1-cosq3*cosq3),cosq3)
                    val1= math.atan2(zc-l1, math.sqrt(xc*xc+yc*yc)) 
                    #print(val1)
                    
                    val2= math.atan2(l3*math.sin(q3), l2+(l3*math.cos(q3)))
                    #print(val2)
                    q2= -1*(val2+val1)
                    print("joint angle values are q1: "+ str(q1) + ", q2: " + str(q2) + ", q3: " + str(q3))
        except ValueError as ve:
            print("Coordinate out of configuration space")

def main(args=None):
    rclpy.init(args=args)

    quat_subscriber = QuatSubscriber()

    rclpy.spin(quat_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    quat_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()