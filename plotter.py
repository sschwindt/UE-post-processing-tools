from config import *
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


mpl.rcParams.update({
    "font.family": "Ubuntu",
    "font.weight": "light",
    "font.size": 10,
    "figure.dpi": 500,
})


class Plotter:
    """Generates scatter plots visualising particle data."""
    def __init__(self, plot_axis):
        """

        Parameters
        ----------
        plot_axis : bool
            Defaults is True. If set to False, no axis will be plotted.
        """
        self.plot_axis = plot_axis

    def __call__(self,
                 data,
                 avg_particles,
                 sd_velocity,
                 valid_particle_count,
                 avg_velocity,
                 section_number,
                 *_x_limits):
        self.print_stats_on_plot = False
        """Entry point that delegates to the plotting routine."""
        self.plot_data(data,
                       avg_particles,
                       sd_velocity,
                       valid_particle_count,
                       avg_velocity,
                       section_number)

    def plot_data(self,
                  data: np.ndarray,
                  avg_particles: float,
                  sd_velocity: float,
                  valid_particle_count: int,
                  avg_velocity: float,
                  section_number: int):
        """Main routine for assembling the figure."""

        fig, ax_scatter, ax_cbar = self._setup_figure()
        self._scatter(ax_scatter, data)
        if self.plot_axis:
            self._add_colorbar(fig, ax_scatter)
        else:
            # used for comparison with OpenFOAM
            ax_scatter.set_axis_off()
        if self.print_stats_on_plot:
            self._add_title(
                fig,
                valid_particle_count,
                avg_particles,
                avg_velocity,
                sd_velocity,
                section_number
            )
        self._save(fig, section_number)


    # Figure building blocks
    @staticmethod
    def _setup_figure():
        """5‑inch‑wide canvas with a dedicated color‑bar row."""
        fig, ax = plt.subplots(figsize=(5, 3.5), dpi=mpl.rcParams["figure.dpi"])
        return fig, ax, None

    def _scatter(self, ax, data):
        """Scatter plot with velocity coloring and custom axes formatting."""
        # Shift X so the minimum becomes 0, satisfying
        x_raw = data[:, 0]
        x = x_raw - x_raw.min()
        y = data[:, 1]  # Elevation above channel bottom
        vel = data[:, 2]

        norm = Normalize(vmin=0.0, vmax=2.0)

        # Color map and scatter
        ax.scatter(x,
                   y,
                   c=vel,
                   cmap="turbo",
                   norm=norm,
                   alpha=1.0,
                   s=np.pi * (0.1 * radius) ** 2)

        # Axis labels
        ax.set_xlabel("Channel width (m)")
        ax.set_ylabel("Elevation above bottom (m)")

        # Axis limits
        ax.set_xlim(0, x.max())
        ax.set_ylim(0, y.max())
        ax.set_aspect('equal', adjustable='box')  # 1 unit x == 1 unit y

        # Grid and tick layout
        ax.grid(True, which="both", linestyle="--", color="grey", linewidth=0.4)
        # X: only every 5th value labeled (e.g., 0.0, 0.5, 1.0, ...)
        x_tick_step = 0.1
        x_ticks = np.arange(0, x.max() + x_tick_step, x_tick_step)
        def every_fifth_x(val, _):
            return f"{val:.1f}" if np.isclose(val % 0.5, 0, atol=1e-8) else ""
        ax.xaxis.set_major_locator(MultipleLocator(x_tick_step))
        ax.xaxis.set_major_formatter(FuncFormatter(every_fifth_x))
        # Y: only every 5th tick labeled (0.00, 0.05, 0.10, ...)
        y_tick_step = 0.05
        def every_fifth(val, _):
            return f"{val:.2f}" if (round(val * 100) % 5 == 0) else ""
        ax.yaxis.set_major_locator(MultipleLocator(y_tick_step))
        ax.yaxis.set_major_formatter(FuncFormatter(every_fifth))
        # Thinner ticks, set ticks inside
        ax.tick_params(axis="both", labelsize=mpl.rcParams["font.size"], width=0.4, length=3, direction="in")

    @staticmethod
    def _add_colorbar(fig, ax_scatter):
        mappable = ax_scatter.collections[0]  # uses Normalize(0, 2)
        cb_ax = inset_axes(
            ax_scatter,
            width="100%", height="50%",  # thin, full-width bar
            loc="upper center",
            bbox_to_anchor=(0, 1.0, 1, 0.2),  # x0,y0,w,h in axes coords
            bbox_transform=ax_scatter.transAxes,
            borderpad=0,
        )
        cbar = fig.colorbar(mappable, cax=cb_ax, orientation="horizontal")

        # show ticks/label only on top
        cbar.ax.xaxis.set_ticks_position("top")
        cbar.ax.xaxis.set_label_position("top")
        cbar.ax.tick_params(which="both", bottom=False, labelbottom=False,
                            top=True, labeltop=True)

        # optional: control tick values
        cbar.set_ticks([0.0, 0.5, 1.0, 1.5, 2.0])

        # make room above axes
        fig.subplots_adjust(top=0.9)
        cbar.set_label(r"Velocity (m s$^{-1}$)")

    @staticmethod
    def _add_title(fig,
                   count: int,
                   avg_particle: float,
                   avg_velocity: float,
                   sd_velocity: float,
                   section_number: int):
        fig.suptitle(
            f"Section {section_number} Results \n"
            f"Particles: {count}, Average particles: {avg_particle}, "
            f"Average velocity: {avg_velocity:.3f} m/s, sd velocity: {sd_velocity:.3f}",
            y=0.01  # keep this low so it stays under the color‑bar row
        )

    @staticmethod
    def _save(fig, section_number: int):
        filename = f"section_plot_{section_number}.png"
        fig.savefig(filename, format="png", bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def reduce_particles(data: np.ndarray, limit: float):
        """Filter out particles with velocity below *limit*."""
        if data.size == 0:
            return data
        return data[data[:, 2] >= limit]

    @staticmethod
    def subtract_global_var():
        """Demonstrates calculation with globals."""
        print(var1 - var2 - var3)
