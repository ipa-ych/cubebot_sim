import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # URDF file
    # xacro_file = os.path.join(get_package_share_directory('cube_sim'), 'urdf', 'cubic_with_controller.urdf.xacro')
    # robotDescription = xacro.process_file(xacro_file).toxml()

    urdf_file = os.path.join(get_package_share_directory('cube_sim'), 'urdf', 'cubic_simple.xacro.urdf')
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    robotDescription = doc.toxml()

    

    world_file = os.path.join(get_package_share_directory("cube_sim"),"urdf","empty_world.world")

    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"),'launch', 'gazebo.launch.py'))

    gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'world': world_file}.items())

    spawnModelNode = Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                output='screen',
                arguments=['-topic','robot_description','-entity', 'cubic'])
    
    nodeRobotStatePublisher = Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[{'robot_description': robotDescription,
                'use_sim_time': True }]
            )
    
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    # Gazebo launch
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawnModelNode,
                on_exit=[load_joint_state_broadcaster],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_broadcaster,
                on_exit=[load_joint_trajectory_controller],
            )
        ),
        gazeboLaunch,
        nodeRobotStatePublisher,
        spawnModelNode,


    ])
