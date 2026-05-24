from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    turtlebot3_navigation2 = get_package_share_directory('turtlebot3_navigation2')

    map_file = os.path.join(
        get_package_share_directory('task_manager'),
        'maps',
        'map.yaml'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    nav2 = ExecuteProcess(
        cmd=['ros2', 'launch', 'turtlebot3_navigation2', 'navigation2.launch.py', 'use_sim_time:=True', f'map:={map_file}'],
        output='screen'
    )

    task_manager = Node(
        package='task_manager',
        executable='task_manager_node',
        name='task_manager',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        TimerAction(period=3.0, actions=[nav2]),
        TimerAction(period=6.0, actions=[task_manager])
    ])