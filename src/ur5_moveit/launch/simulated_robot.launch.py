import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node  # Added this import
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("ur5_description"),
            "launch",
            "gazebo.launch.py"
        ),
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("ur5_controller"),
            "launch",
            "controller.launch.py"
        )
    )

    moveit_launch = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("ur5_moveit"),
            "launch",
            "moveit.launch.py"
        )
    )

    # Add the Quest Teleop Node
    # Replace 'quest_bridge' with your actual package name
    quest_teleop_node = Node(
        package='quest_bridge',
        executable='quest_teleop',
        name='quest_teleop_node',
        output='screen',
        # Optional: If you want to ensure it uses simulation time
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gazebo,
        controller,
        moveit_launch,
        #quest_teleop_node
    ])
