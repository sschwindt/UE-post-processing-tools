from calculation import *
from plotter import *



class Main:
    """
    Main driver class to process the log file, analyze sections, and generate plots.
    """

    def __init__(self):
        """
        Initializes the main class.

        Initializes data_list (list): A list to store data elements.
        """
        self.data_list: list = []


    def __call__(self):
        """
        Main execution method that processes the log file, analyzes sections, and generates plots.

        """

        calculation = Calculation()
        plotter = Plotter()

        sections = calculation.extract_sections()

        # Calculate average particle counts using the new method
        avg_particles = calculation.calculate_average_particle_count(sections)

        # Process each section and generate plots
        for section_number, section in enumerate(sections, start=1):
            self.process_section(section, calculation, plotter, avg_particles, section_number)

        self.calculate_panda_values()
        calculation.sum_global_var()
        plotter.subtract_global_var()

    def calculate_panda_values(self):
        """
        Processes collected particle data using Pandas for statistical analysis and storage.

        Args:
            None (Relies on self.data_list, which contains processed section data.)

        Returns:
            None (Outputs results to a CSV file and prints key statistical values.)
        """
        df = pd.DataFrame(self.data_list)
        df_sorted = df.sort_values(by=['sd_velocity'], ascending=False)
        mean_value = df['sd_velocity'].mean()
        df.to_csv('Values.csv', index=False)
        print(df.head(5))
        print("mean sd_velocity: " + str(mean_value))
        print(df_sorted.head(5))

    def setup_section(self, section, calculation):
        """
        Processes a section of data to extract relevant particle information.

        Args:
            section (list): List of strings representing a section of the log file.
            calculation (Calculation): Instance of the Calculation class used for computations.

        Returns:
            tuple: (data, valid_particle_count, avg_velocity, sd_velocity)
                - data (list): Processed particle data extracted from the section.
                - valid_particle_count (int): Number of valid particles in this section.
                - avg_velocity (float): Average velocity of particles in this section.
                - sd_velocity (float): Standard deviation of particle velocities.
        """

        data = calculation(section)
        valid_particle_count = len(data)
        avg_velocity = calculation.calculate_average_velocity(data)
        sd_velocity = calculation.calculate_standard_deviation(data)

        return data, valid_particle_count, avg_velocity, sd_velocity


    def create_pictures(self, data, plotter, avg_particle, sd_velocity, valid_particle_count,
                        avg_velocity, left_value, right_value, section_number):
        """
        Generates and saves plots for a given section of particle data.

        Args:
            data (list): List of particle data points.
            plotter (Plotter): Instance of the Plotter class used for visualization.
            avg_particle (float): Average number of particles in this section.
            sd_velocity (float): Standard deviation of particle velocities.
            valid_particle_count (int): Number of valid particles in this section.
            avg_velocity (float): Average velocity of particles in this section.
            left_value (float): Left boundary for the x-section.
            right_value (float): Right boundary for the x-section.
            section_number (int): The section number being processed.
        """

        if limit_Data:
            reduced_data = plotter.reduce_particles(data, limit)
            plotter(reduced_data, avg_particle, sd_velocity, valid_particle_count, avg_velocity,
                    section_number, left_value, right_value)
        else:
            plotter(data, avg_particle, sd_velocity, valid_particle_count, avg_velocity,
                    section_number, left_value, right_value)


    def process_section(self, section, calculation, plotter, avg_particles, section_number):
        """
        Processes a single section of data.

        TODO: Implemented auxiliary component as create_pictures

        Args:
            section (list): List of strings representing the section.
            calculation (Calculation): Instance of the Calculation class.
            plotter (Plotter): Instance of the Plotter class.
            avg_particles (list): Average particle count across sections.
            section_number (int): Section number being processed.
        """

        # Whether to create plots for each section (True to create plots, False to skip plotting)
        # auxiliary component
        create_pictures = True

        data,valid_particle_count, avg_velocity, sd_velocity = self.setup_section(section, calculation)

        if valid_particle_count > 0:
            current_xs = calculation.determine_xs(data, section_number)
            left_value, right_value = xs_limits.get(current_xs)
            avg_particle = avg_particles.get(current_xs, 0)

            print(f'Section {section_number}: Count of valid particles: {valid_particle_count}')
            print(f'Section {section_number}: Average Velocity: {avg_velocity:.3f} m/s')

            self.data_list.append({
                "xs": current_xs,
                "valid_particle_count": valid_particle_count,
                "avg_particle": avg_particle,
                "sd_velocity": sd_velocity,
                "avg_velocity": avg_velocity
            })

            if create_pictures:
                self.create_pictures(data, plotter, avg_particle, sd_velocity, valid_particle_count,
                                     avg_velocity, left_value, right_value, section_number)


if __name__ == "__main__":
    main = Main()
    main()
