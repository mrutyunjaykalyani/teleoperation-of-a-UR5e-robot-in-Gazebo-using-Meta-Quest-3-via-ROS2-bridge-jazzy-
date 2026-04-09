import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # 1. Load MoveIt Configs
    moveit_config = (
        MoveItConfigsBuilder("ur5_robot", package_name="ur5_moveit_config")
        .robot_description(
            file_path=os.path.join(
                get_package_share_directory("ur5_description"),
                "urdf",
                "ur5_robot.urdf.xacro",
            )
        )
        .to_moveit_configs()
    )

    # 2. Path to your Servo YAML
    # We pass the path directly to avoid the "Uninitialized" error
    servo_yaml_path = os.path.join(
        get_package_share_directory("ur5_moveit_config"),
        "config",
        "ur_servo.yaml",
    )

    # 3. The Servo Node
    servo_node = launch_ros.actions.Node(
        package="moveit_servo",
        executable="servo_node",
        # Set the name to match the top-level key in your YAML
        name="servo_node",
        parameters=[
            moveit_config.to_dict(),
            servo_yaml_path,  # Directly include the YAML file
            {"use_sim_time": True},
        ],
        output="screen",
    )

    # 4. Robot State Publisher (Container)
    container = launch_ros.actions.ComposableNodeContainer(
        name="ur_servo_container",
        namespace="/",
        package="rclcpp_components",
        executable="component_container_mt",
        composable_node_descriptions=[
            launch_ros.descriptions.ComposableNode(
                package="robot_state_publisher",
                plugin="robot_state_publisher::RobotStatePublisher",
                name="robot_state_publisher",
                parameters=[moveit_config.robot_description],
            ),
        ],
        output="screen",
    )

    return launch.LaunchDescription([servo_node, container])
