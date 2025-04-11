# 轨迹规划

`TrajectoryArt` 可以计算速度连续的关节或者笛卡尔轨迹。

接口如下：
```c++
auto traj =
    TA::Trajectory::Create(waypoints, vel_limits, acc_limits, {},
                            {
                                {"tolerance_blend", tolerance_blend},
                                {"tolerance_colinear", 3.0},
                                {"tolerance_overlap", 0.001},
                                {"report_preprocess_result", true},
                            });
```

参数解释：
- waypoints：轨迹的控制点，控制点会被接近，但不会经过
  - 当单个waypoint的维度小于7的时候，调用关节轨迹规划，传入的vel_limits、acc_limits要和单个waypoint的维度一致
- vel_limits: 各个自由度的最大速度限制，必须是正值
- acc_limits: 各个自由度的最大加速度限制，必须是正值
- jerk_limits: 各个自由度的最大加加速度限制，必须是正值；当前算法不需要这个约束，可以传入空的vector

剩下的参数都通过 `TA::NamedParameters` 的方式传入，可选的参数如下：
- tolerance_blend: 两段直线轨迹会使用弧线进行过度，这个参数影响弧线的长短
- tolerance_colinear: 如果相邻三个waypoint之间的角度小于这个值，则它们共线，中间的waypoint会被删除，以减少不必要的计算
- tolerance_overlap: 如果相邻两个waypoint之间的距离小于这个值，则它们重叠，前一个waypoint会被删除，以减少不必要的计算
- report_preprocess_result: 是否输出预处理结果，打印原始点个数，过滤后的点个数到控制台


## 运行示例
运行 `UseTrajectoryArt --help` 可以查看运行示例运行不要的参数。

运行 `UseTrajectoryArt.py` 需要安装的Python版本与编译好的一致。

输出轨迹结果后，如果采样点太多，使用matplotlib显示会比较卡，使用下面的命令可以更高效的显示：

```shell
uv run ./Example/PlotTraj.py plot-large-3d --fpos ./pos.txt --fpos2 ./Waypoints.txt
```