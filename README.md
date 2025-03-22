# TrajectoryArt 预编译库文件

本仓库定期发布预编译好的TrajectoryArt动态库文件，可以在[Release](https://github.com/xiaodaxia-8/TrajectoryArtPub/releases)中下载。

![时间最优匀速轨迹](./Doc/toppra_constant_speed.png)

## 使用教程

查看博客 [TrajectoryArt 轨迹规划教程](https://blog.myshawn.com/blog/trajectoryart-%E8%BD%A8%E8%BF%B9%E8%A7%84%E5%88%92%E6%95%99%E7%A8%8B/)
或者请参考 [TrajectoryArt Notebook教程1](./Doc/Tutorial1.ipynb)

## 更新日志

### v0.3.0

- 实现toppra时间最优算法
- 支持梯形匀速算法
- 路径插值实现了圆弧、贝塞尔五阶过度算法
- 调整了调用接口，除 `waypoints` 外，其他参数都以关键字参数传入