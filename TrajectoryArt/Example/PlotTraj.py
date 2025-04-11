# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "numpy",
#     "pytransform3d[all]",
#     "typer",
# ]
#
# [[tool.uv.index]]
# url = "https://pypi.tuna.tsinghua.edu.cn/simple"
# ///

# run the script with `uv run PlotResult.py`, see here https://docs.astral.sh/uv/guides/scripts/#using-different-python-versions

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import typer
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from pytransform3d.trajectories import plot_trajectory
from typing_extensions import Annotated, Optional

dir = os.getcwd()

app = typer.Typer(name="PlotTraj application")


@app.command()
def plot_large_3d(
    fpos: Annotated[Path, typer.Option(help="positions file")] = dir + "/pos.txt",
    start_col: int = 1,
    fpos2: Annotated[Path, typer.Option(help="positions file")] = None,
    start_col2: int = 0,
):
    from pytransform3d.visualizer import figure

    positions = np.loadtxt(fpos)
    points = positions[:, start_col : start_col + 3]
    mean = points.mean(axis=0)
    points -= mean

    fig = figure()
    fig.plot_basis(s=np.abs(points).max() * 0.1)
    fig.plot(points, c=[1, 0, 0])

    if fpos2 is not None:
        positions2 = np.loadtxt(fpos2)
        points2 = positions2[:, start_col2 : start_col2 + 3]
        points2 -= mean
        fig.plot(points2)

    fig.show()


@app.command()
def plot(
    fpos: Annotated[Path, typer.Option(help="positions file")] = dir + "/pos.txt",
    fvel: Annotated[Path, typer.Option(help="velocities file")] = dir + "/vel.txt",
    facc: Annotated[Path, typer.Option(help="accelerations file")] = dir + "/acc.txt",
    delimiter: Optional[str] = None,
):
    if not Path(fpos).exists():
        print(f"{fpos} not found")
        return
    if not Path(fvel).exists():
        print(f"{fvel} not found")
        return
    if not Path(facc).exists():
        print(f"{facc} not found")
        return
    positions = np.loadtxt(fpos, delimiter=delimiter)
    velocities = np.loadtxt(fvel, delimiter=delimiter)
    accelerations = np.loadtxt(facc, delimiter=delimiter)
    dof = positions.shape[1]
    print(f"positions shape: {positions.shape}")
    print(f"velocities shape: {velocities.shape}")
    print(f"accelerations shape: {accelerations.shape}")

    nrows = 2
    ncols = 2
    ax = plt.subplot(
        nrows, ncols, 1, projection="3d" if positions.shape[1] >= 4 else None
    )
    ax.axis("equal")
    if positions.shape[1] == 8:
        poses = positions[:, 1:]
        poses[:, [3, -1]] = poses[:, [-1, 3]]
        plot_trajectory(ax, poses, s=0.1, n_frames=100)
    else:
        plt.plot(*positions[:, 1:4].T)
    plt.title("path")

    plt.subplot(nrows, ncols, 2)
    if positions.shape[1] == 8:
        plt.plot(positions[:, 0], positions[:, 1:4])
        plt.legend([f"Axis{i}" for i in range(3)])
    else:
        plt.plot(positions[:, 0], positions[:, 1:])
        plt.legend([f"Axis{i}" for i in range(dof)])
    plt.title("positions")

    plt.subplot(nrows, ncols, 3)
    plt.plot(accelerations[:, 0], accelerations[:, 1:])
    plt.legend([f"Axis{i}" for i in range(dof)])
    plt.title("accelerations")

    plt.subplot(nrows, ncols, 4)
    plt.plot(velocities[:, 0], velocities[:, 1:])
    plt.legend([f"Axis{i}" for i in range(dof)])
    plt.title("velocities")
    plt.show()


if __name__ == "__main__":
    # typer.run(plot)
    app()
