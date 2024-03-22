cmake_minimum_required(VERSION 3.8)
project(cube_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ros2_control REQUIRED)
find_package(controller_manager REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(control_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Add include directories
include_directories(include)

# Install
install(DIRECTORY
  config
  launch
  urdf
  DESTINATION share/${PROJECT_NAME}
)

add_executable(controller_position src/node_control_position.cpp)
ament_target_dependencies(controller_position
  rclcpp
  rclcpp_action
  control_msgs
)

## Install
install(
  TARGETS
  controller_position
  DESTINATION
    lib/${PROJECT_NAME}
)

ament_package()
