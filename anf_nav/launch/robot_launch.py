from simple_launch import SimpleLauncher


def generate_launch_description():

    sl = SimpleLauncher()
    sl.declare_arg('robot', 'turtlebot')
    sl.declare_arg('nav', False, description = 'Whether to use nav stack or manual control')
    sl.declare_arg('gt', True, description='Whether the robot uses ground truth localization for BB8')

    sl.include('anf_nav', 'spawn_launch.py',
               launch_arguments=sl.arg_map('robot', 'gt'))

    sl.include('anf_nav', 'nav_launch.py',
            launch_arguments=sl.arg_map('robot', 'nav'))

    return sl.launch_description()
