cmake_minimum_required(VERSION 3.20)
project(UseTrajectoryArt)


set(TrajectoryArt_DIR "../lib/cmake")
find_package(TrajectoryArt CONFIG REQUIRED)

add_executable(UseTrajectoryArt UseTrajectoryArt.cpp)
target_link_libraries(UseTrajectoryArt PRIVATE TrajectoryArt::TrajectoryArt)
target_compile_features(UseTrajectoryArt PRIVATE cxx_std_23)

add_executable(TrajectoryArtWizard TrajectoryArtWizard.cpp)
target_link_libraries(TrajectoryArtWizard PRIVATE TrajectoryArt::TrajectoryArtWizard)
target_compile_features(TrajectoryArtWizard PRIVATE cxx_std_23)