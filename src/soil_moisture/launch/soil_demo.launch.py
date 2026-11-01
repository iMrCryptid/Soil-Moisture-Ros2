from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='soil_moisture',
            executable='moisture_publisher',
            name='moisture_publisher',
            output='screen',
            parameters=[{'sensor_id': 'probe_1', 'publish_rate_hz': 2.0}],
        ),
        Node(
            package='soil_moisture',
            executable='moisture_monitor',
            name='moisture_monitor',
            output='screen',
        ),
    ])
