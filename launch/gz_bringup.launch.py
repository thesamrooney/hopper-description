import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    package_name = "hopper-description"

    ### DECLARE LAUNCH ARGUMENTS

    # ...

    ### INCLUDE LAUNCH FILES

    # Create the robot state publisher
    rsp_source = PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory("hopper-description"),
        "launch",
        "rsp.launch.py"
    ))

    rsp = IncludeLaunchDescription(
        rsp_source,
        launch_arguments={
            "use_sim_time": "true"
        }.items()
    )

    gz_sim_source = PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory("ros_gz_sim"), 
        "launch", 
        "gz_sim.launch.py"
    ))

    gz_world_file = os.path.join(
        get_package_share_directory(package_name),
        "worlds",
        "empty.world"
    )

    gz_sim = IncludeLaunchDescription(
        gz_sim_source,
        launch_arguments={
            'gz_args': ["-r ", gz_world_file],
            'on_exit_shutdown': 'True'
        }.items(),
    )

    # DEFINE NODES

    gz_create_robot = Node(
        package = "ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description",
                   "-name", "hopper"],
        output="screen",
    )

    # gz_param_bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     parameters=[
    #         {"config_file": os.path.join(
    #             get_package_share_directory("hopper"),
    #             "config",
    #             "gz_bridge.config.yaml",
    #         )}
    #     ],
    #     # remappings=[],
    #     output='screen'
    # )

    # twist_stamper = Node(
    #     package='twist_stamper',
    #     executable='twist_stamper',
    #     parameters=[{'use_sim_time': True}],
    #     remappings=[('/cmd_vel_in','/hopper_cont/cmd_vel_unstamped'),
    #                 ('/cmd_vel_out','/hopper_cont/cmd_vel')],
    # )

    # controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["hopper_cont", "joint_broad"],
    # )

    # DEFINE ACTIONS

    # we have to have a delay here because it takes a long time to load the world
    # actions_after_world_loads = TimerAction(
    #     period=5.0,
    #     actions=[
    #         controller_spawner
    #     ]
    # )


    return LaunchDescription([
        rsp,
        # twist_stamper,
        gz_sim,
        gz_create_robot,
        # gz_param_bridge,
        # actions_after_world_loads
    ])