cmake_minimum_required(VERSION 3.12)

set(CMAKE_CXX_FLAGS "-std=c++14 -O3 -g")

find_package(OpenCV REQUIRED)
find_package(Boost REQUIRED COMPONENTS filesystem)

add_executable(statistic_image_pixel src/utils/statistic_image_pixel.cc)
target_link_libraries(statistic_image_pixel ${Boost_LIBRARIES} ${OpenCV_LIBRARIES})
