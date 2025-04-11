/**
 * Copyright © 2025 Zen Shawn. All rights reserved.
 *
 * @file TrajectoryArtWizard.h
 * @author Zen Shawn
 * @email xiaozisheng2008@hotmail.com
 * @date 12:05:11, April 11, 2025
 */
#ifdef _MSC_VER
#ifdef TrajectoryArtWizard_EXPORTS
#define TRAJECTORYARTWIZARD_EXPORT __declspec(dllexport)
#else
#define TRAJECTORYARTWIZARD_EXPORT __declspec(dllimport)
#endif
#else
#define TRAJECTORYARTWIZARD_EXPORT
#endif

#include <TA/TrajectoryArt.h>
#include <filesystem>

namespace TA
{

TRAJECTORYARTWIZARD_EXPORT
void ShowTrajectoryArtWizard(
    const std::vector<std::vector<double>> &waypoints = {},
    std::shared_ptr<Trajectory> traj = nullptr);

} // namespace TA