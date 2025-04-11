/**
 * Copyright © 2023 Zen Shawn. All rights reserved.
 *
 * @file TrajectoryArt.h
 * @author: Zen Shawn
 * @email: xiaozisheng2008@qq.com
 * @date: 16:31:06, January 09, 2023
 */
#pragma once

#ifdef _MSC_VER
#ifdef TrajectoryArt_EXPORTS
#define TRAJECTORYART_EXPORT __declspec(dllexport)
#else
#define TRAJECTORYART_EXPORT __declspec(dllimport)
#endif
#else
#define TRAJECTORYART_EXPORT
#endif

#include <any>
#include <memory>
#include <string>
#include <string_view>
#include <unordered_map>
#include <variant>
#include <vector>

namespace TA
{

/**
 * @brief
 *
 * @param lang "zh" or "en"
 * @return TRAJECTORYART_EXPORT
 */
TRAJECTORYART_EXPORT void Initialize(const std::string &lang = "zh");

TRAJECTORYART_EXPORT std::string_view GetVersion();

/// @brief Set logger level, trace/debug/info/warn/error/critical/off
TRAJECTORYART_EXPORT void SetLoggerLevel(const std::string &level_name);

using ParamValue =
    std::variant<std::string, double, bool, int, std::vector<double>>;

class Trajectory
{
  public:
    TRAJECTORYART_EXPORT
    static std::shared_ptr<Trajectory>
    Create(const std::vector<std::vector<double>> &waypoints,
           const std::unordered_map<std::string, ParamValue> &params = {
               {"algorithm", "trapezoidal"},
               {"tolerance_blend", std::numeric_limits<double>::max()},
               {"tolerance_colinear", 1.0},
               {"tolerance_overlap", 0.001},
               {"waypoint_type", "joint"},
               {"step_size", 0.01},
               {"vel_limits", 5.0},
               {"acc_limits", 25.0},
               {"jerk_limits", 50.0},
           });

    TRAJECTORYART_EXPORT double GetDuration() const;
    TRAJECTORYART_EXPORT std::vector<double>
    GetParameterizerValue(double t, unsigned order = 0) const;
    TRAJECTORYART_EXPORT std::vector<double> GetPosition(double t) const;
    TRAJECTORYART_EXPORT std::vector<double> GetVelocity(double t) const;
    TRAJECTORYART_EXPORT std::vector<double> GetAcceleration(double t) const;

    TRAJECTORYART_EXPORT ~Trajectory();

  private:
    Trajectory() = default;

    struct TrajectoryImpl;
    std::unique_ptr<TrajectoryImpl> m_impl;
};
} // namespace TA