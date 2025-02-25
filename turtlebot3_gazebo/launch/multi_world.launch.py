#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction, GroupAction, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import PushRosNamespace, SetRemap, Node

def robot_controller_actions(context, *args, **kwargs):
    # Accessing launch configurations
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    use_sim_time = LaunchConfiguration('use_sim_time').perform(context)
    num_robots = int(LaunchConfiguration('num_robots').perform(context))
    x_pose = LaunchConfiguration('x_pose').perform(context)
    y_pose = LaunchConfiguration('y_pose').perform(context)

    actions = []

    for robot_number in range(1, num_robots + 1):
        robot_name = f'robot{robot_number}'

        group = GroupAction([
            PushRosNamespace(robot_name),
            SetRemap('/tf', 'tf'),
            SetRemap('/tf_static', 'tf_static'),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
                ),
                launch_arguments={
                    'use_sim_time': use_sim_time
                }.items()
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(launch_file_dir, 'multi_spawn.launch.py')
                ),
                launch_arguments={
                    'x_pose': str(float(x_pose) + robot_number * 2.0),
                    'y_pose': y_pose,
                    'entity_name': robot_name
                }.items()
            ),

            Node(
                package='turtlebot3_gazebo',
                executable='turtlebot3_drive',
                output='screen'
            )
        ])

        actions.append(group)

    return actions

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    # Declare launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    num_robots = LaunchConfiguration('num_robots', default='1')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')

    world = os.path.join(pkg_turtlebot3_gazebo, 'worlds', 'turtlebot3_dqn_stage1.world')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    declare_num_robots_cmd = DeclareLaunchArgument(
        'num_robots',
        default_value='1',
        description='Number of robots to spawn'
    )

    declare_x_pose_cmd = DeclareLaunchArgument(
        'x_pose',
        default_value='-2.0',
        description='Initial x pose'
    )

    declare_y_pose_cmd = DeclareLaunchArgument(
        'y_pose',
        default_value='-0.5',
        description='Initial y pose'
    )

    # Gazebo server and client
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # Robot controllers
    robot_controller_cmd = OpaqueFunction(function=robot_controller_actions)
    delay_before_robot_controller = TimerAction(
        period=10.0,
        actions=[robot_controller_cmd]
    )

    # Build the launch description
    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_num_robots_cmd)
    ld.add_action(declare_x_pose_cmd)
    ld.add_action(declare_y_pose_cmd)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(delay_before_robot_controller)

    return ld
