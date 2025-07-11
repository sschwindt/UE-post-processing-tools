from config import *


class ParticleAttibuteCalculator:
    """
    Processes sections to extract valid particles and calculates relevant metrics.
    """

    def __call__(self, section):
        """
        Extracts valid particle data from a section.

        Args:
            section (list): List of strings representing lines from a section.

        Returns:
            np.ndarray: Array of valid particle data.
        """Class
        return self.extract_valid_particles(section)

    def extract_sections(self):
        """
        Reads the file and splits its content into sections based on "STOP" markers.

        :return: List of sections, each containing lines from the file.
        """
        sections = []
        current_section = []

        with open(file_path, 'r') as file:
            for line in file:
                if "STOP" in line:          #check if section is concluded
                    sections.append(current_section)
                    current_section = []
                else:
                    current_section.append(line)

        if current_section:
            sections.append(current_section)

        return sections

    def extract_valid_particles(self, section):
        """
        Filters and parses valid particles from the section.

        Args:
            section (list): List of lines to analyze.

        Returns:
            np.ndarray: Array containing valid particles with attributes [Y, Z, Velocity, XS].
        """
        valid_particles = [self.parse_line(line) for line in section if "LogBlueprintUserMessages" in line]
        return np.array([particle for particle in valid_particles if particle])

    def parse_line(self, line):
        """
        Parses a line to extract valid particle data.

        Args:
            line (str): String containing particle data.

        Returns:
            list or None: [Y, Z, Velocity, XS] if valid, otherwise None.
        """

        # check for matches in red line
        key_match = re.search(r'KEY: \d+', line)
        vector_match = re.search(r'VECTOR: X=[-.\d]+ Y=[-.\d]+ Z=[-.\d]+', line)
        velocity_match = re.search(r'VELOCITY: [-.\d]+', line)
        xs_match = re.search(r"XS(\d+)", line)

        #extract data from lines
        if key_match and vector_match and velocity_match and xs_match:
            y, z = self.extract_vector_components(line)
            velocity = self.extract_velocity(line)
            xs_value = int(xs_match.group(1))
            return [y, z, velocity, xs_value]
        return None

    def extract_vector_components(self, line):
        """
        Extracts Y and Z components from a vector string.

        Args:
            line (str): String containing vector information.

        Returns:
            tuple: (Y, Z) values as floats.
        """
        y_match = re.search(r'Y=([-\d.]+)', line)
        z_match = re.search(r'Z=([-\d.]+)', line)
        return float(y_match.group(1)) / 100, float(z_match.group(1)) / 100

    def extract_velocity(self, line):
        """
        Extracts velocity value from a line.

        Args:
            line (str): String containing velocity information.

        Returns:
            float: Velocity value.
        """
        velocity_match = re.search(r'VELOCITY: [-.\d]+', line)
        return round(float(velocity_match.group(0).split(": ")[1]) / 100, 3)

    def calculate_average_velocity(self, data):
        """
        Calculates the average velocity of particles.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Average velocity rounded to 3 decimal places.
        """
        return round(np.mean(data[:, 2]), 3) if data.size > 0 else 0

    def calculate_standard_deviation(self, data):
        """
        Calculates the standard deviation of particle velocities.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Standard deviation rounded to 3 decimal places.
        """
        return round(np.std(data[:, 2]), 3) if data.size > 0 else 0

    def calculate_average_particle_count(self, sections):
        """
        Calculates the average number of particles for each cross-section (XS).

        Args:
            sections (list): List of sections containing particle data.

        Returns:
            dict: Dictionary with average particle counts for each XS category.
        """
        xs_totals = {11: 0, 41: 0, 21: 0, 31: 0, 12: 0, 42: 0, 22: 0, 32: 0}
        xs_counts = {11: 0, 41: 0, 21: 0, 31: 0, 12: 0, 42: 0, 22: 0, 32: 0}

        for section_number, section in enumerate(sections, start=1):
            data = self.extract_valid_particles(section)
            valid_particle_count = len(data)

            if valid_particle_count > 0:
                xs_key = self.determine_xs(data, section_number)
                if xs_key in xs_totals:
                    xs_totals[xs_key] += valid_particle_count       #sum up all valid particles
                    xs_counts[xs_key] += 1

        xs_averages = {}
        for xs_key in xs_totals:
            if xs_counts[xs_key] > 0:
                xs_averages[xs_key] = round(xs_totals[xs_key] / xs_counts[xs_key], 1) #calculate average particles per xs
            else:
                xs_averages[xs_key] = 0
        return xs_averages

    def determine_xs(self, data, section_number):
        """
        Determines the cross-section (XS) key based on the mean XS value in the data and section number.

        The XS key is determined based on predefined thresholds related to section numbers.

        Args:
            data (np.ndarray): Particle data array, where the fourth column contains XS values.
            section_number (int): The current section number.

        Returns:
            int or None: XS key (e.g., 11, 41) or None if no match is found.
        """

        xs_value = int(data[:, 3].mean())  # Get the XS value
        if xs_value == 1:
            return 11 if section_number < 20 else 12
        elif xs_value == 4:
            return 41 if section_number < 40 else 42
        elif xs_value == 2:
            return 21 if section_number < 50 else 22
        elif xs_value == 3:
            return 31 if section_number < 60 else 32
        return None

    def sum_global_var(self):
        """
        Calculates the sum of three global variables defined in the config file.

        Global Variables (imported from config):
            var1 (float or int): The first variable.
            var2 (float or int): The second variable.
            var3 (float or int): The third variable.

        Returns:
            None (Prints the computed sum).
        """
        print(var1 + var2 + var3)