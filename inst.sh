ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py


ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=true map:=./turtlebot3_world.yaml params_file:=/opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml

# ros2 launch nav2_costmap_filters_demo filter.launch.py use_sim_time:=true params_file:=./src/navigation2_tutorials/nav2_costmap_filters_demo/params/nav2_params.yaml use_composition:=True


ros2 launch nav2_keepout_filter filter.launch.py use_sim_time:=true params_file:=./src/nav2_keepout_filter/params/mask.yaml mask:=./keepout_mask.yaml

ros2 launch nav2_keepout_filter navigation_filter.launch.py use_sim_time:=true map:=./turtlebot3_world.yaml params_file:=./src/nav2_keepout_filter/params/mask.yaml mask:=./keepout_mask.yaml

ros2 action send_goal /dock_robot opennav_docking_msgs/action/DockRobot "{use_dock_id: true, dock_id: 'dock1', dock_type: 'turtlebot3_dock', max_staging_time: 1000.0, navigate_to_staging_pose: true}"


# Straight line
# Change the planner server in params
https://automaticaddison.com/how-to-create-a-straight-line-path-planner-plugin-ros-2/
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=true map:=./turtlebot3_world.yaml params_file:=./src/nav2_keepout_filter/params/nav2_params.yaml