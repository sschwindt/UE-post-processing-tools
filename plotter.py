from config import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator, FuncFormatter

# -----------------------------------------------------------------------------
# Global Matplotlib style: Ubuntu Light 10.5 pt on a 400 dpi, 5‑inch‑wide figure
# -----------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "Ubuntu",
    "font.weight": "light",
    "font.size": 10.5,
    "figure.dpi": 400,
})


class Plotter:
    """Generates scatter plots visualising particle data."""

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _create_custom_cmap():
        """Custom rainbow‐like colour map consistent with the original script."""
        colours = [
            (0.0,   (0,   0,   0.5)),
            (0.125, (0,   0,   1.0)),
            (0.375, (0,   1.0, 1.0)),
            (0.5,   (0,   1.0, 0)),
            (0.625, (1.0, 1.0, 0)),
            (0.875, (1.0, 0,   0)),
            (1.0,   (0.5, 0,   0)),
        ]
        return LinearSegmentedColormap.from_list("custom_rainbow", colours)

    def plot_data(self,
                  data: np.ndarray,
                  avg_particles: float,
                  sd_velocity: float,
                  valid_particle_count: int,
                  avg_velocity: float,
                  section_number: int):
        """Master routine assembling the figure."""
        fig, ax_scatter, ax_cbar = self._setup_figure()
        self._scatter(ax_scatter, data)
        self._add_colourbar(fig, ax_cbar)
        if self.print_stats_on_plot:
            self._add_title(fig,
                            valid_particle_count,
                            avg_particles,
                            avg_velocity,
                            sd_velocity,
                            section_number
                        )
        self._save(fig, section_number)

    # ------------------------------------------------------------------
    # Figure building blocks
    # ------------------------------------------------------------------
    @staticmethod
    def _setup_figure():
        """5‑inch‑wide canvas with a dedicated colour‑bar row."""
        height_inches = 3.5  # free choice as only width is prescribed
        fig = plt.figure(figsize=(5, height_inches), dpi=mpl.rcParams["figure.dpi"])
        gs = GridSpec(nrows=2, ncols=1, height_ratios=[0.1, 0.9], figure=fig)
        return fig, fig.add_subplot(gs[1]), fig.add_subplot(gs[0])

    def _scatter(self, ax, data):
        """Scatter plot with velocity colouring and custom axes formatting."""
        # Shift X so the minimum becomes 0, satisfying *"resetting the smallest value to zero"*
        x_raw = data[:, 0]
        x = x_raw - x_raw.min()
        y = data[:, 1]  # Elevation above channel bottom
        vel = data[:, 2]

        # Colour map and scatter
        cmap = self._create_custom_cmap()
        ax.scatter(x,
                   y,
                   c=vel,
                   cmap=cmap,
                   vmin=0,
                   vmax=vmax,
                   alpha=1.0,
                   s=np.pi * (0.1 * radius) ** 2)

        # Axis labels
        ax.set_xlabel("Channel width (m)")
        ax.set_ylabel("Elevation above bottom (m)")

        # Axis limits – requested behaviour
        ax.set_xlim(0, x.max())
        ax.set_ylim(0, y.max())

        # Grid and tick layout
        ax.grid(True, which="both", linestyle="--", color="grey", linewidth=0.4)
        # X: only every 5th value labeled (e.g., 0.0, 0.5, 1.0, ...)
        x_tick_step = 0.1
        x_ticks = np.arange(0, x.max() + x_tick_step, x_tick_step)
        def every_fifth_x(val, _):
            return f"{val:.1f}" if np.isclose(val % 0.5, 0, atol=1e-8) else ""
        ax.xaxis.set_major_locator(MultipleLocator(x_tick_step))
        ax.xaxis.set_major_formatter(FuncFormatter(every_fifth_x))
        # Y: only every 5th tick labeled (0.00, 0.05, 0.10, …)
        y_tick_step = 0.01
        def every_fifth(val, _):
            return f"{val:.2f}" if (round(val * 100) % 5 == 0) else ""
        ax.yaxis.set_major_locator(MultipleLocator(y_tick_step))
        ax.yaxis.set_major_formatter(FuncFormatter(every_fifth))
        # Thinner ticks, set ticks inside
        ax.tick_params(axis="both", labelsize=mpl.rcParams["font.size"], width=0.4, length=3, direction="in")

    # ------------------------------------------------------------------
    # Ancillary elements
    # ------------------------------------------------------------------
    @staticmethod
    def _add_colourbar(fig, ax):
        scatter = fig.axes[0].collections[0]
        cbar = fig.colorbar(scatter, cax=ax, orientation="horizontal", pad=0.0)
        cbar.set_label("Velocity (m/s)", labelpad=4)
        cbar.ax.xaxis.set_label_position("top")
        cbar.ax.tick_params(labelsize=mpl.rcParams["font.size"])

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
            y=0.01  # Keeping low so it stays under the colour‑bar row
        )

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    @staticmethod
    def _save(fig, section_number: int):
        filename = f"section_plot_{section_number}.png"
        fig.savefig(filename, format="png", bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Utilities preserved from the original script (untouched)
    # ------------------------------------------------------------------
    @staticmethod
    def reduce_particles(data: np.ndarray, limit: float):
        """Filter out particles with velocity below *limit* (unchanged)."""
        if data.size == 0:
            return data
        return data[data[:, 2] >= limit]

    @staticmethod
    def subtract_global_var():
        """Demonstrates calculation with globals (unchanged)."""
        print(var1 - var2 - var3)
