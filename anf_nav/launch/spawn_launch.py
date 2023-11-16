from simple_launch import SimpleLauncher

sl = SimpleLauncher()
sl.declare_arg('gt', True, description='Whether the robot uses ground truth localization for BB8')
sl.declare_arg('robot', 'turtlebot')


def launch_setup():

    robot = sl.arg('robot')

    gt = sl.arg('gt') or robot == 'turtlebot'

    with sl.group(ns = robot):

        request = {'robot_namespace': '__ns', 'static_tf_odom': gt}

        if robot == 'bb8':
            sl.robot_state_publisher('anf_launch', 'bb8.xacro')
            # run velocity -> joints
            sl.node('anf_nav', 'vel2joints.py')

        else:

            sl.robot_state_publisher('turtlebot3_xacro', 'turtlebot3_waffle_pi.urdf.xacro',
                                 xacro_args = {'prefix': 'turtlebot/'})
            request['x'] = 2.85
            request['y'] = 2.53
            request['theta'] = -2.1
            request['laser_color'] = [0,255,0]

            # move the wheels
            sl.node('map_simulator', 'kinematics.py')

        if not gt:
            # AMCL
            sl.node('nav2_amcl', 'amcl',name='amcl',
                parameters=[sl.find('anf_nav', 'amcl_param.yaml')],
                arguments='--ros-args --log-level warn')

            # run lifecycle manager just for AMCL
            sl.node('nav2_lifecycle_manager','lifecycle_manager',name='lifecycle_manager',
            parameters={'autostart': True, 'node_names': ['amcl']})

        # spawn robot in simulation at a given position
        sl.service('/simulator/spawn', request = request)
        
    return sl.launch_description()


generate_launch_description = sl.launch_description(launch_setup)
