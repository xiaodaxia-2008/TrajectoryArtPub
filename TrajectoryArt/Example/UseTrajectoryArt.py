import sys
import os
from types import SimpleNamespace
from pathlib import Path

import numpy as np

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../build/bin"))
)

from PyTrajectoryArt import GetVersion, Trajectory, SetLoggerLevel, Initialize  # noqa: E402


def plot_traj_parameterizer(traj: Trajectory, num=10000):
    import matplotlib.pyplot as plt

    ts = np.linspace(0.0, traj.GetDuration(), num)
    arr = np.array([traj.GetParameterizerValue(t, 2) for t in ts])
    plt.suptitle("trajectory parameterizer")
    plt.subplot(311)
    plt.plot(ts, arr[:, 0])
    plt.title("value")

    plt.subplot(312)
    plt.plot(ts, arr[:, 1])
    plt.title("velocity")

    plt.subplot(313)
    plt.plot(ts, arr[:, 2])
    plt.title("acceleration")

    plt.show()


def animate_traj_path(traj, waypoints=None, num=10000):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from functools import partial
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    ts = np.linspace(0, traj.GetDuration(), num)
    positions = np.array([traj.GetPosition(t) for t in ts])

    def update_line(frames, line):
        line.set_data_3d(positions[: frames * 100, :3].T)

    plt.suptitle("trajectory path")
    ax: Axes3D = plt.subplot(
        111,
        projection="3d" if positions.shape[1] >= 3 else None,
    )

    if waypoints is not None:
        ax.plot(*waypoints[:, :3].T, "bo-", lw=1)

    line = plt.plot(*positions[:, :3].T, "r-", lw=2)[0]
    ani = animation.FuncAnimation(
        plt.gcf(),
        partial(update_line, line=line),
        positions.shape[0] // 100,
        interval=50,
        repeat=False,
    )
    ani.save("animation.gif", dpi=100)
    ax.axis("equal")
    ax.set_title("path")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()


def plot_traj_components(traj, animate=False, step=0.01):
    """
    Plot the components of a trajectory.

    Parameters
    ----------
    traj : Trajectory
        The trajectory to plot.
    animate : bool, optional
        If True, animate the trajectory. Default is False.
    num : int, optional
        The number of samples to take from the trajectory. Default is 10000.

    Returns
    -------
    None

    """
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from functools import partial
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    ts = np.linspace(
        0, traj.GetDuration(), max(int(traj.GetDuration()) / step, 10), endpoint=True
    )
    positions = np.array([traj.GetPosition(t) for t in ts])
    velocities = np.array([traj.GetVelocity(t) for t in ts])
    acceleration = np.array([traj.GetAcceleration(t) for t in ts])

    def update_line(frames, line):
        if hasattr(line, "set_data_3d"):
            line.set_data_3d(positions[: frames * 100, :3].T)
        else:
            line.set_data(positions[: frames * 100, :2].T)

    nr = 3
    nc = 2
    ax: Axes3D = plt.subplot2grid(
        (nr, nc),
        (0, 0),
        rowspan=2,
        projection="3d" if positions.shape[1] >= 3 else None,
    )
    line = plt.plot(*positions[:, :3].T, "r-")[0]
    if animate:
        ani = animation.FuncAnimation(
            fig=plt.gcf(),
            func=partial(update_line, line=line),
            frames=max(positions.shape[0] // 100, 2),
            interval=50,
            repeat=False,
        )
    ax.axis("equal")
    ax.set_title("path")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if isinstance(ax, Axes3D):
        ax.set_zlabel("z")

    plt.subplot(nr, nc, 2)
    plt.plot(ts, positions)
    plt.legend([f"J{i}" for i in range(positions.shape[1])])
    plt.title("position")

    plt.subplot(nr, nc, 4)
    plt.plot(ts, velocities)
    plt.title("velocity")
    plt.legend([f"J{i}" for i in range(velocities.shape[1])])

    plt.subplot(nr, nc, 5)
    plt.plot(ts, acceleration)
    plt.title("acceleration")
    plt.legend([f"J{i}" for i in range(acceleration.shape[1])])

    speeds = np.linalg.norm(velocities[:, :3], axis=1)
    plt.subplot(nr, nc, 6)
    plt.plot(ts, speeds)
    plt.title("tcp speed")

    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()


def compare_traj_path(
    traj,
    original_waypoints: np.ndarray | Path,
    num=10000,
):
    """
    Plot the path of a trajectory.

    Parameters
    ----------
    traj : Trajectory
        Trajectory to plot
    original_waypoints : np.ndarray | Path
        Original waypoints
    num : int, optional (default: 10000)
        Number of samples to plot
    """
    from pytransform3d.visualizer import figure

    ts = np.linspace(0, traj.GetDuration(), num)
    points = np.array([traj.GetPosition(t) for t in ts])
    mean = points.mean(axis=0)
    points -= mean

    fig = figure("对比计算的轨迹(绿色)和原始路径点(红色)")
    fig.plot_basis(s=np.abs(points).max() * 0.1)
    fig.plot(points, c=[0, 1, 0])

    points2 = None
    if isinstance(original_waypoints, Path):
        points2 = np.loadtxt(original_waypoints)
    elif isinstance(original_waypoints, np.ndarray):
        points2 = original_waypoints

    if points2 is not None:
        points2 = points2[:, :3]
        points2 -= mean
        fig.plot(points2, c=[1, 0, 0])

    fig.show()


def helix_waypoints(n=1000, radius=1000.0, pitch=100.0):
    # helix curve
    ss = np.linspace(0, np.pi * 2 * 10, n)
    return np.c_[radius * np.cos(ss), radius * np.sin(ss), ss * pitch / (np.pi * 2)]


def half_cylinder_waypoints(n=1000, R=1000.0):
    # cylinder
    ss = np.linspace(0, np.pi * 2 * 10, n)
    quotients, remainders = np.divmod(ss, np.pi)
    for quotient in np.unique(quotients):
        if quotient % 2 == 0:
            continue
        mask = quotients == quotient
        remainders[mask] = remainders[mask][::-1]
    return np.c_[R * np.cos(remainders), R * np.sin(remainders), 100 * quotients]


if __name__ == "__main__":
    SetLoggerLevel("debug")
    Initialize()
    print(f"TrajectoryArt {GetVersion()}")

    waypoints = np.array(
        [
            [0.0, 0.0, 0.0],
            [1000.0, 0.0, 100.0],
            [1000.0, 1000.0, 200.0],
            [0.0, 1000.0, 300.0],
            [0.0, 0.0, 400.0],
            [1000.0, 0.0, 500.0],
            [1000.0, 1000.0, 600.0],
            [0.0, 1000.0, 700.0],
            [0.0, 0.0, 800.0],
        ],
        dtype=float,
    )

    # waypoints = np.array([
    #     [1675.840, -210.967, -450.756, -1.697, -43.772],
    #     [1675.844, -210.967, -450.756, -1.697, -43.772]
    # ])

    # file = Path(__file__).parent / "../../Data/Waypoints.txt"
    file = Path(__file__).parent / "../build/test-waypoints.txt"
    # waypoints = np.loadtxt(file)[::1000, :3]
    waypoints = np.loadtxt(file)

    dof = waypoints.shape[1]

    params = SimpleNamespace()
    # params.algorithm = "toppra"
    # params.path_type = "bezier_quadratic_blend"
    # params.acceleration = 5
    # params.tolerance_blend = 300.0
    # params.speed = 108.333
    params.vel_limits = 500.0
    # params.vel_limits = [500.0] * dof
    # params.vel_limits = 0.01
    # params.acc_limits = [3000, 3000, 2500, 2000, 2000]
    params.acc_limits = 2500.0
    params.step_size = 0.01
    traj = Trajectory.Create(waypoints, vars(params))
    print(f"{traj.GetDuration()= :.4f}s")

    # plot_traj_parameterizer(traj)
    # animate_traj_path(traj, waypoints)
    # compare_traj_path(traj, waypoints)
    plot_traj_components(traj, animate=True, step=0.001)
