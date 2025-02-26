from config import *



class Plotter:
    """
    Generates scatter plots visualizing particle data.
    """

    def __call__(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity, section_number, xlim_left,
                 xlim_right):
        """
        Creates a plot for the given particle data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.
        """
        self.plot_data(data, avg_particles, sd_velocity, valid_particle_count, avg_velocity,
                       section_number, xlim_left, xlim_right)


    def create_custom_cmap(self):
        """
        Creates a custom rainbow colormap.

        :return: LinearSegmentedColormap object.
        """
        colors = [
            (0.0, (0, 0, 0.5)),
            (0.125, (0, 0, 1.0)),
            (0.375, (0, 1.0, 1.0)),
            (0.5, (0, 1.0, 0)),
            (0.625, (1.0, 1.0, 0)),
            (0.875, (1.0, 0, 0)),
            (1.0, (0.5, 0, 0))
        ]
        return LinearSegmentedColormap.from_list('custom_rainbow', colors)

    def plot_data(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity,
                  section_number, xlim_left, xlim_right):
        """
        Creates and saves a scatter plot for the data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.
        """
        fig, ax_scatter, ax_colorbar = self.setup_figure()
        self.create_scatter_plot(ax_scatter, data, xlim_left, xlim_right)
        self.add_colorbar(fig, ax_colorbar)
        self.add_titles(fig, valid_particle_count, avg_particles, avg_velocity, sd_velocity, section_number)
        self.save_plot(section_number)

    def setup_figure(self):
        """
        Sets up the figure and axes for plotting.

        :return: Tuple (Figure, scatter axis, colorbar axis).
        """
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        gs = GridSpec(2, 1, height_ratios=[0.1, 0.9])
        return fig, fig.add_subplot(gs[1]), fig.add_subplot(gs[0])

    def create_scatter_plot(self, ax, data, xlim_left, xlim_right):
        """
        Generates a scatter plot of particle data, where colors represent velocity.

        Args:
            ax (matplotlib.axes.Axes): Matplotlib Axes object where the scatter plot will be drawn.
            data (numpy.ndarray): NumPy array containing particle data with columns [y, z, velocity].
            xlim_left (float): Left boundary for the x-axis.
            xlim_right (float): Right boundary for the x-axis.

        Returns:
            None (Modifies the provided Matplotlib Axes object with the scatter plot.)
        """
        y, z, velocity = data[:, 0], data[:, 1], data[:, 2]
        cmap = self.create_custom_cmap()
        ax.scatter(y, z, c=velocity, cmap=cmap, vmin=0, vmax=vmax, alpha=1.0, s=np.pi * (0.1 * radius) ** 2)
        ax.set_facecolor('white')
        ax.set_xlabel('Y Values (m)', fontsize=18)
        ax.set_ylabel('Z Values (m)', fontsize=18)
        ax.yaxis.set_major_locator(MultipleLocator(0.01))
        ax.grid(True, which='both', linestyle='--', color='gray', linewidth=0.7)
        ax.set_ylim(0, 0.8)
        ax.set_xlim(xlim_left, xlim_right)
        ax.tick_params(labelsize=10)

    def reduce_particles(self, data, limit):
        """
        Filters out particles with velocities below the specified limit.

        Args:
            data (np.ndarray): Array of particle data with attributes [Y, Z, Velocity, XS].
            limit (float): Minimum velocity threshold. Particles with velocities below this value are removed.

        Returns:
            np.ndarray: Filtered array containing only particles with velocities >= limit.
        """
        if data.size == 0:
            return data  # Return the original array if empty

        reduced_data = data[data[:, 2] >= limit]
        return reduced_data

    def add_colorbar(self, fig, ax):
        """
        Adds a colorbar to the plot.

        :param fig: Matplotlib Figure object.
        :param ax: Matplotlib Axes object for colorbar.
        """
        scatter = fig.axes[0].collections[0]
        cbar = fig.colorbar(scatter, cax=ax, orientation='horizontal', pad=0.0)
        cbar.set_label('Velocity (m/s)', fontsize=18, labelpad=10)
        cbar.ax.xaxis.set_label_position('top')
        cbar.ax.tick_params(labelsize=8)

    def add_titles(self, fig, count, avg_particle, avg_velocity, sd_velocity, section_number):
        """
        Adds titles to the plot.

        Args:
            fig (matplotlib.figure.Figure): Matplotlib figure object.
            count (int): Number of valid particles.
            avg_particle (float): Average particle count for the current XS.
            avg_velocity (float): Average velocity of particles.
            sd_velocity (float): Standard deviation of velocity.
            section_number (int): Section number being processed.
        """
        fig.suptitle(f'Section {section_number} Results\n'
                     f'Particles: {count}, Average particles: {avg_particle},\n'
                     f'Average velocity: {avg_velocity:.3f} m/s, sd velocity: {sd_velocity:.3f}',
                     fontsize=18, y=0.01)

    def save_plot(self, section_number):
        """
        Saves the plot as a PNG file.

        :param section_number: Section number for naming the file.
        """

        output_filename = f'section_plot_{section_number}.png'
        plt.savefig(output_filename, format='png', bbox_inches='tight')
        plt.close()

    def subtract_global_var(self):
        """
        Calculates the difference of three global variables defined in the config file.

        Global Variables (imported from config):
            var1 (float or int): The first variable.
            var2 (float or int): The second variable.
            var3 (float or int): The third variable.

        Returns:
            None (Prints the computed difference).
        """
        print(var1-var2-var3)

