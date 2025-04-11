#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "TrajectoryArt::TrajectoryArt" for configuration "Release"
set_property(TARGET TrajectoryArt::TrajectoryArt APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(TrajectoryArt::TrajectoryArt PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/TrajectoryArt.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/TrajectoryArt.dll"
  )

list(APPEND _cmake_import_check_targets TrajectoryArt::TrajectoryArt )
list(APPEND _cmake_import_check_files_for_TrajectoryArt::TrajectoryArt "${_IMPORT_PREFIX}/lib/TrajectoryArt.lib" "${_IMPORT_PREFIX}/bin/TrajectoryArt.dll" )

# Import target "TrajectoryArt::TrajectoryArtWizard" for configuration "Release"
set_property(TARGET TrajectoryArt::TrajectoryArtWizard APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(TrajectoryArt::TrajectoryArtWizard PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/TrajectoryArtWizard.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/TrajectoryArtWizard.dll"
  )

list(APPEND _cmake_import_check_targets TrajectoryArt::TrajectoryArtWizard )
list(APPEND _cmake_import_check_files_for_TrajectoryArt::TrajectoryArtWizard "${_IMPORT_PREFIX}/lib/TrajectoryArtWizard.lib" "${_IMPORT_PREFIX}/bin/TrajectoryArtWizard.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
