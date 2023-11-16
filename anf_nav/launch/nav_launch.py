from simple_launch import SimpleLauncher
from nav2_common.launch import RewrittenYaml

sl = SimpleLauncher()

sl.declare_arg('vx_max', 2.)
sl.declare_arg('vx_min', 0.)
sl.declare_arg('robot', 'turtlebot')
sl.declare_arg('nav', False, description = 'Whether to use nav stack or manual control')


def launch_setup():

    robot = sl.arg('robot')

    with sl.group(ns = robot):

        if sl.arg('nav'):

            # all required nodes
            nav_nodes = [('nav2_behaviors', 'behavior_server'),
                            ('nav2_bt_navigator', 'bt_navigator'),
                            ('nav2_controller', 'controller_server'),
                            ('nav2_planner', 'planner_server'),
                            ('nav2_smoother', 'smoother_server'),
                            ('nav2_waypoint_follower', 'waypoint_follower'),
                            ('nav2_collision_monitor', 'collision_monitor')
                            ]

            node_names = [executable for _,executable in nav_nodes]

            # get default configuration file from nav2
            nav2_params = sl.find('anf_nav', 'nav_params.yaml')

            # adapt it to this robot
            # link prefixes are updated with robot name
            vmax = str(sl.arg('vx_max'))
            rewrites = {'global_frame': robot+'/odom',
                        'use_sim_time': 'False',
                        'base_frame_id': robot+'/base_link',
                        'robot_base_frame': robot+'/base_link',
                        'robot_radius': '.27',
                        'topic': '/'+robot+'/scan',
                        'max_vel_x': vmax,
                        'min_vel_x': str(sl.arg('vx_min')),
                        'max_speed_xy': vmax}

            configured_params = RewrittenYaml(
                            source_file = nav2_params,
                            root_key=robot,
                            param_rewrites=rewrites,
                            convert_types=True)

            # common remappings, some nav2 nodes assume a local map topic or a global scan topic
            remappings = {f'/{robot}/map': '/map', 'map': '/map', '/scan': 'scan'}
            remappings_cmd = {'cmd_vel': 'cmd_vel_raw'}

            # launch navigation nodes
            for pkg,executable in nav_nodes:
                sl.node(pkg, executable,name=executable,
                    parameters=[configured_params],
                    remappings=remappings_cmd if executable == 'controller_server' else remappings,
                    arguments='--ros-args --log-level warn')

            # also run overall manager
            sl.node('nav2_lifecycle_manager','lifecycle_manager',name='lifecycle_manager',
            output='screen',
            parameters=[{'autostart': True,
                        'node_names': node_names}])

        else:
            # manual control
            sl.node('slider_publisher', arguments = [sl.find('anf_nav', 'cmd_vel.yaml')])

    return sl.launch_description()


generate_launch_description = sl.launch_description(launch_setup)
    
