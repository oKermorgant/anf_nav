# Nav stack examples for ANF ROS 2

## Cloning

Clone this repo recursively:

```
git clone https://github.com/oKermorgant/anf_nav.git --recursive
```

If you forgot, activate the submodule with:

```
git submodule update --init --recursive
```

## Dependencies

- `simple_launch`
- `slider_publisher`
- `navigation2`
- `map_simulator` (cloned with this repo)
    - `opencv`
- `turtlebot3_description`

### Install all deps before compiling:

```
sudo apt install ros-${ROS_DISTRO}-navigation2 ros-${ROS_DISTRO}-simple-launch \
                ros-${ROS_DISTRO}-slider-publisher ros-${ROS_DISTRO}-turtlebot3-description \
                libopencv-dev
```

### Compile and source your workspace

`colcon build --symlink-install && source install/setup.bash`

## Running the simulation

```
ros2 launch anf_nav sim_launch.py
```

## Available launch files

### Spawing a robot

```
ros2 launch anf_nav spawn_launch.py
```

Arguments:

- `robot` (bb8 or turtlebot): which robot to spawn
- `gt` (bool): whether we use ground truth localization as opposed to AMCL


### Launching the nav stack

```
ros2 launch anf_nav nav_launch.py
```

Arguments:

- `robot` (bb8 or turtlebot): which robot to spawn
- `nav` (bool): whether to use the nav stack or manual control


### Spawn + nav

```
ros2 launch anf_nav robot_launch.py
```

Arguments:

- `robot` (bb8 or turtlebot): which robot to spawn
- `gt` (bool): whether we use ground truth localization as opposed to AMCL
- `nav` (bool): whether to use the nav stack or manual control



