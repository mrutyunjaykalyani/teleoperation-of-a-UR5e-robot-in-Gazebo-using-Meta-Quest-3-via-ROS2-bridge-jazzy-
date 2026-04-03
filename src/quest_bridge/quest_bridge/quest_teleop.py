import rclpy
from rclpy.node import Node
import openvr
from geometry_msgs.msg import PoseStamped
from scipy.spatial.transform import Rotation as R
import sys

class QuestTeleop(Node):
    def __init__(self):
        super().__init__('quest_teleop_node')
        self.publisher_ = self.create_publisher(PoseStamped, '/target_pose', 10)
        
        try:
            self.vr = openvr.init(openvr.VRApplication_Background)
        except openvr.OpenVRError as e:
            self.get_logger().error(f"OpenVR Init Failed: {e}")
            sys.exit(1)

        self.get_logger().info("Quest 3 Teleop Started: Position + Orientation active.")
        self.timer = self.create_timer(0.033, self.timer_callback)

    def timer_callback(self):
        poses_type = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
        poses = poses_type()
        self.vr.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseRawAndUncalibrated, 0, poses)
        
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            device_class = self.vr.getTrackedDeviceClass(i)
            if device_class == openvr.TrackedDeviceClass_Controller:
                role = self.vr.getControllerRoleForTrackedDeviceIndex(i)
                
                if role == openvr.TrackedControllerRole_RightHand and poses[i].bPoseIsValid:
                    matrix = poses[i].mDeviceToAbsoluteTracking
                    
                    msg = PoseStamped()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = "base_link"

                    # --- POSITION ---
                    msg.pose.position.x = float(matrix[0][3])
                    msg.pose.position.y = float(matrix[1][3])
                    msg.pose.position.z = float(matrix[2][3])

                    # --- ORIENTATION (Rotation Matrix to Quaternion) ---
                    # Extract the 3x3 rotation part from the 3x4 matrix
                    rotation_matrix = [
                        [matrix[0][0], matrix[0][1], matrix[0][2]],
                        [matrix[1][0], matrix[1][1], matrix[1][2]],
                        [matrix[2][0], matrix[2][1], matrix[2][2]]
                    ]
                    
                    # Convert using SciPy
                    r = R.from_matrix(rotation_matrix)
                    quat = r.as_quat() # Returns [x, y, z, w]

                    msg.pose.orientation.x = quat[0]
                    msg.pose.orientation.y = quat[1]
                    msg.pose.orientation.z = quat[2]
                    msg.pose.orientation.w = quat[3]

                    self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = QuestTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        openvr.shutdown()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
