# Meta Quest 3 Teleoperation for UR5e (ROS 2 Jazzy)

![ROS2](https://img.shields.io/badge/ros2-jazzy-blue?logo=ros)
![Python](https://img.shields.io/badge/python-3.12+-yellow?logo=python)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

This project enables real-time, 6-DOF teleoperation of a **Universal Robots UR5e** using a **Meta Quest 3**. Designed for **ROS 2 Jazzy Jalisco** on Ubuntu 24.04, it bridges SteamVR spatial data into the ROS 2 ecosystem for intuitive robot control.

---

## 🏗 System Architecture

The control loop follows this data flow:

1. **Meta Quest 3**: Tracks controller pose and sends it to the PC via **ALVR**.
2. **SteamVR**: Provides the spatial matrices via the **OpenVR API**.
3. **`quest_teleop` Node**: 
    - Polls the Right Hand controller pose at **30Hz**.
    - Converts the 3x4 Transformation Matrix into a ROS 2 `PoseStamped` message.
    - Uses **SciPy** to calculate Quaternions for orientation.
    - Implements a **Grip-to-Engage** (Deadman's Switch) safety mechanism.
4. **MoveIt Servo**: Processes the pose stream to generate smooth, collision-aware joint velocities for the **UR5e**.

---

## 🛠 Prerequisites

### Hardware
* **Meta Quest 3** (or Quest 2/Pro).
* **Linux Workstation**: Ubuntu 24.04 LTS.
* **Wi-Fi 6 Router**: Required for low-latency wireless ALVR streaming.

### Software
* **ROS 2 Jazzy Jalisco**
* **ALVR** (Linux Streamer) & **SteamVR**
* **Python Dependencies**:
  ```bash
  # Note: Ubuntu 24.04 requires --break-system-packages or a venv
  pip install openvr scipy --break-system-packages


🚀 Installation

    #Clone the repository:
    #Bash

    cd ~/ur5_ws/src
    git clone [https://github.com/yourusername/quest_bridge.git](https://github.com/yourusername/quest_bridge.git)

    #Build for Jazzy:
    #Bash

    cd ~/ur5_ws
    colcon build --packages-select quest_bridge
    source install/setup.bash

🎮 Usage Instructions (Jazzy)
1. Start the VR Bridge

    Launch ALVR and connect your Quest 3.

    Ensure SteamVR shows both controllers as active.

2. Launch Robot Simulation (Gazebo/Ignition)
    Bash
    
    ros2 launch ur_simulation_gazebo ur_sim_control.launch.py ur_type:=ur5e

3. Launch MoveIt Servo
    Bash
    
    ros2 launch ur_moveit_config servo.launch.py

4. Run the Teleop Node
    Bash
    
    ros2 run quest_bridge quest_teleop

🕹 Operation & Controls

Engage (Move): Hold the Grip Button on the Right Controller. The UR5e follows your hand while pressed.

Clutching: Release the Grip button to reposition your hand without moving the robot (useful for reaching further).

Visuals: Use SteamVR Desktop View in the headset to see the Gazebo window.

⚙️ Configuration

In quest_teleop.py, you can tune the following:

Offsets: Adjust the + 0.4 values to change the robot's starting position relative to its base.

Topic Mapping: Ensure your topic matches your Servo configuration (default: /servo_node/pose_target_cmds).

📝 License

Licensed under Apache License 2.0.
