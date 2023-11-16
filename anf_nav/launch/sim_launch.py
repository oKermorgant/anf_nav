from simple_launch import SimpleLauncher


def generate_launch_description():
    sl = SimpleLauncher()

    # run simulation
    sl.include('map_simulator', 'simulation2d_launch.py',
               launch_arguments={'map': sl.find('anf_nav', 'batS.yaml'),
                                 'map_server': True})

    # spawn an obstacle
    sl.service('/simulator/spawn', request = {'x': 3.5, 'y': -6.3})

    # run RViz2
    rviz_config_file = sl.find('anf_nav', 'sim.rviz')
    sl.rviz(rviz_config_file)
        
    return sl.launch_description()
