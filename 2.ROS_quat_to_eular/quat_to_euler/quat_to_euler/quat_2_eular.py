

import rclpy
from rclpy.node import Node
import math

from std_msgs.msg import Float32MultiArray


class QuatSubscriber(Node):

    def __init__(self):
        super().__init__('quat_subscriber')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'quat_topic',
            self.quat_callback,
            10)
        self.subscription  # prevent unused variable warning

    def quat_callback(self, msg):
        w=msg.data[0]
        x=msg.data[1]
        y=msg.data[2]
        z=msg.data[2]

        #roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z);
        cosr_cosp = 1 - 2 * (x * x + y * y);
        roll = math.atan2(sinr_cosp, cosr_cosp);

        # pitch (y-axis rotation)
        sinp = math.sqrt(1 + 2 * (w * y - x * z));
        cosp = math.sqrt(1 - 2 * (w * y - x * z));
        pitch = 2 * math.atan2(sinp, cosp) - math.pi/ 2;

        # yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y);
        cosy_cosp = 1 - 2 * (y * y + z * z);
        yaw = math.atan2(siny_cosp, cosy_cosp);

        print("Eular angles are roll="+ str(roll) + ", pitch=" + str(pitch) + ", yaw=" + str(yaw))
        


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