cmake_minimum_required(VERSION 3.5)
project(anf_nav)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch urdf maps params DESTINATION share/${PROJECT_NAME})

file(GLOB scripts src/*)
install(PROGRAMS ${scripts} DESTINATION lib/${PROJECT_NAME})

ament_package()
