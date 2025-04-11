/**
 * Copyright © 2023 Zen Shawn. All rights reserved.
 *
 * @file UseTrajectoryArt.cpp
 * @author: Zen Shawn
 * @email: xiaozisheng2008@qq.com
 * @date: 17:55:30, January 09, 2023
 */

#include "CLI11.hpp"
#include <TA/TrajectoryArt.h>

#include <chrono>
#include <filesystem>
#include <format>
#include <fstream>
#include <iostream>
#include <print>
#include <ranges>
#include <source_location>
#include <string_view>

namespace fs = std::filesystem;
namespace ranges = std::ranges;

#define LOG(...)                                                               \
    {                                                                          \
        auto loc = std::source_location::current();                            \
        std::print("{}:{} - ", fs::path(loc.file_name()).filename().string(),  \
                   loc.line());                                                \
        std::println(__VA_ARGS__);                                             \
    }

int main(int argc, char **argv)
{
    TA::SetLoggerLevel("debug");
    TA::Initialize("zh");
    CLI::App app{std::format("TrajectoryArt{} example", TA::GetVersion())};

    fs::path fpath(fs::current_path() / "Waypoints.txt");
    app.add_option("-i,--in", fpath, "Waypoints file")
        ->check(CLI::ExistingFile);

    bool output{false};
    app.add_flag("-o,--out", output, "Output trajectory results");

    bool plot{false};
    app.add_flag("-p,--plot", plot, "Plot trajectory results");

    size_t max_waypoints = std::numeric_limits<size_t>::max();
    app.add_option("-m,--max-waypoints", max_waypoints, "Maximum waypoints");

    double dt = 0.01;
    app.add_option("--dt", dt, "waypoint sample time interval");

    double tol_blend{std::numeric_limits<double>::max()};
    app.add_option("--tolerance-blend", tol_blend, "Blending tolerance");

    double tol_colinear{1.0};
    app.add_option("--tolerance-colinear", tol_colinear,
                   "tolerance colinear unit is deg");

    double tol_overlap{0.001};
    app.add_option("--tolerance-overlap", tol_overlap, "tolerance overlap");

    double step_size{1.0};
    app.add_option("--step-size", step_size, "step size");

    std::string waypoint_type{"joint"};
    app.add_option("--waypoint-type", waypoint_type,
                   "waypoint type, joint|cartesian");

    std::string algorithm{"trapezoidal"};
    app.add_option("--algorithm", algorithm, "algorithm, trapezoidal|toppra");

    std::string path_type{"bezier_quadratic_blend"};
    app.add_option("--path-type", path_type,
                   "path type, bezier_quadratic_blend|bezier_quintic_blend");

    double vel_limits{500.0};
    app.add_option("--vel-limits", vel_limits, "velocity limits");

    double acc_limits{2500.0};
    app.add_option("--acc-limits", acc_limits, "acceleration limits");

    CLI11_PARSE(app, argc, argv);

    std::ifstream ifs(fpath);
    // read waypoints from file
    size_t dof = 0;
    std::vector<std::vector<double>> waypoints;
    std::string line;
    const std::string delim{" "};
    while (!ifs.eof()) {
        std::getline(ifs, line);
        if (line.starts_with('#') || line.empty()) {
            continue;
        }
        std::vector<double> vec;
        for (auto r : line | std::views::split(delim)) {
            if (r.empty()) {
                continue;
            }
            std::string s{r.begin(), r.end()};
            double v = std::stod(s);
            vec.push_back(v);
        }

        if (dof == 0) {
            dof = vec.size();
        }

        if (vec.size() >= dof) {
            waypoints.emplace_back(vec.begin(), vec.begin() + dof);
        }

        if (waypoints.size() >= max_waypoints) {
            break;
        }
    }

    // compute the trajectory
    LOG("compute trajectory from {} waypionts", waypoints.size());
    auto t1 = std::chrono::system_clock::now();
    auto traj = TA::Trajectory::Create(waypoints,
                                       {
                                           {"vel_limits", vel_limits},
                                           {"acc_limits", acc_limits},
                                           {"tolerance_blend", tol_blend},
                                           {"tolerance_colinear", tol_colinear},
                                           {"tolerance_overlap", tol_overlap},
                                           {"step_size", step_size},
                                           {"waypoint_type", waypoint_type},
                                           {"algorithm", algorithm},
                                           {"path_type", path_type},
                                       });
    auto t2 = std::chrono::system_clock::now();

    // check result
    LOG("Finish computing within {}",
        std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1));

    LOG("traj duration: {:.4f}", traj->GetDuration());

    // output trajectory to files
    if (output || plot) {
        std::vector<std::vector<double>> poss, vels, accs;
        std::vector<double> ts;
        for (double t = 0; t <= traj->GetDuration(); t += dt) {
            poss.push_back(traj->GetPosition(t));
            vels.push_back(traj->GetVelocity(t));
            accs.push_back(traj->GetAcceleration(t));
            ts.push_back(t);
        }

        auto fpos = fpath.replace_filename("pos.txt");
        auto fvel = fpath.replace_filename("vel.txt");
        auto facc = fpath.replace_filename("acc.txt");
        {
            std::ofstream ofs1(fpos);
            std::ofstream ofs2(fvel);
            std::ofstream ofs3(facc);
            auto to_file = [ins = traj.get()](auto &&f, double t,
                                              std::ostream &ofs,
                                              std::string delim) {
                ofs << t << delim;
                ranges::copy(std::invoke(f, ins, t),
                             std::ostream_iterator<double>(ofs, delim.c_str()));
                ofs << "\n";
            };

            double t = 0;
            double T = traj->GetDuration();
            while (true) {
                if (t > T) {
                    t = T;
                }
                to_file(&TA::Trajectory::GetPosition, t, ofs1, delim);
                to_file(&TA::Trajectory::GetVelocity, t, ofs2, delim);
                to_file(&TA::Trajectory::GetAcceleration, t, ofs3, delim);
                if (t >= T) {
                    break;
                }
                t += dt;
            }
        }

        LOG("result saved to {}, {}, {}", fpos.string(), fvel.string(),
            facc.string());

        if (plot) {
            auto cmd = std::format(
                "uv run {}/PlotTraj.py plot --fpos {} --fvel {} --facc {}",
                fs::current_path().string(), fpos.string(), fvel.string(),
                facc.string());
            if (delim != " ") {
                cmd += std::format(" --delimiter {}", delim);
            }
            LOG("run command: {}", cmd);
            system(cmd.c_str());
        }
    }

    return 0;
}