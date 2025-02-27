## Code Description


>	***Purpose***: This project provides post-processing tools for Unreal Engine (UE) simulations, specifically targeting fluid particle 
> simulations for a 50m technical fish pass. The code is designed to extract, analyze,
> and visualize particle data from simulation log files, enabling validation of physical accuracy through comparisons with OpenFOAM results.


>	***Motivation***: Unreal Engine 5 provides powerful simulation capabilities, particularly with the Niagara Fluids Plugin, 
> which can simulate up to 2 million particles. However, raw simulation logs contain a large amount of continuous text that needs to be properly
> separated to extract useful information. A key advantage of this approach is the significantly faster rendering time compared to OpenFOAM, which requires
> extensive computational resources and long processing times to generate fluid simulation sequences. While real-time rendering in Unreal Engine allows for quick
> iteration and previews, the best results are achieved through high-quality offline rendering, ensuring detailed and visually accurate outputs while still
> maintaining a significant speed advantage over OpenFOAM.


>	***Goals***: 
> * Automate log parsing: Filter and extract relevant particle data.
> * Compute statistical metrics: Calculate average particle counts, velocity distributions, and standard velocity deviation per section.
> * Generate structured plots: Provide high-quality visual representations of particle movement using color mapping.




## Requirements
A data file must be available containing particle data in the following format:  

`LogBlueprintUserMessages` `KEY:` `VECTOR: X= Y= Z=` `VELOCITY` `POSITION`  

Refer to the image below for reference. Each section in the data file is separated by a **STOP**.  
Lines that do not follow this format will be ignored by the program.  



For more details, you can check the example data file `TechnicalFishPassOneSectionC150KShort.log`.

![datafile](https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations/blob/main/images/dataFileExample.png)
*<sub>A section of a sample data file. (source: Benjamin Kemmler 2025).</sub>*

Ensure you have the following dependencies installed before running the script:

### Standard Libraries:
* `os`- Interact with the operating system.
* `re`- Handle regular expressions.
* `csv`- Read and write CSV files.
* `math`- Perform mathematical operations.

### Non-Standard Python Libraries:
* `numpy`- Handle numerical computations efficiently.
* `pandas`- Process and analyze structured data.
* `matplotlib`-  Create static, animated, and interactive plots.


## Usage Instructions


### Running the Script

1. Ensure that the `config.py` file is correctly set up with required variables like `file_path`

2. Place the `.log` file in the expected location.

3. Run the script using:

`python main.py`

### Expected Output

* If enabled in config: Scatter plots saved as PNG files

![section_plot](https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations/blob/main/images/section_plot_1.png)
*<sub>A sample plot. (source: Benjamin Kemmler 2025).</sub>*
* Processed data saved as `Values.csv`

### Customization

Modify multiple parameters in `config.py` to adjust the in- and output

* Input File Path – Define the datalog file path.
* XS Limits – Set x-axis limits for each cross-section.
* Vmax – Specify the maximum value for the colorbar.
* Radius – Determine the radius of each point in the scatterplot.
* Limit Data – Exclude particles below a specified velocity threshold.
* Limit – Set the threshold value for Limit Data.


* var1 – Globally used variable for calculations.
* var2 – Globally used variable for calculations.
* var3 – Globally used variable for calculations.



## Code diagram

For further details about the workflow of the code, please refer to the flowchart below.

The `auxiliary component variable` is highlighted in green.

![flowChart](https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations/blob/main/images/flowChart.png)
*<sub>General flow chart of the provided code (source: Benjamin Kemmler 2025).</sub>*



Get ready by cloning the repository:

```
git clone https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations.git
```


## Documentation

For any issues, please refer to the comments from the script listed below.
### Calculation Class
```
    def __call__(self, section):
        
        Extracts valid particle data from a section.

        Args:
            section (list): List of strings representing lines from a section.

        Returns:
            np.ndarray: Array of valid particle data.
        
```
```
    def extract_sections(self):
        
        Reads the file and splits its content into sections based on "STOP" markers.

        :return: List of sections, each containing lines from the file.
        
```
```
    def extract_valid_particles(self, section):
        
        Filters and parses valid particles from the section.

        Args:
            section (list): List of lines to analyze.

        Returns:
            np.ndarray: Array containing valid particles with attributes [Y, Z, Velocity, XS].
        
```
```
    def parse_line(self, line):

        Parses a line to extract valid particle data.

        Args:
            line (str): String containing particle data.

        Returns:
            list or None: [Y, Z, Velocity, XS] if valid, otherwise None.

```
```
    def extract_vector_components(self, line):

        Extracts Y and Z components from a vector string.

        Args:
            line (str): String containing vector information.

        Returns:
            tuple: (Y, Z) values as floats.

```
```
    def extract_velocity(self, line):

        Extracts velocity value from a line.

        Args:
            line (str): String containing velocity information.

        Returns:
            float: Velocity value.
```
```   
    def calculate_average_velocity(self, data):

        Calculates the average velocity of particles.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Average velocity rounded to 3 decimal places.

```
```
    def calculate_standard_deviation(self, data):

        Calculates the standard deviation of particle velocities.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Standard deviation rounded to 3 decimal places.

```
```
    def calculate_average_particle_count(self, sections):

        Calculates the average number of particles for each cross-section (XS).

        Args:
            sections (list): List of sections containing particle data.

        Returns:
            dict: Dictionary with average particle counts for each XS category.

```
```
    def determine_xs(self, data, section_number):

        Determines the cross-section (XS) key based on the mean XS value in the data and section number.

        The XS key is determined based on predefined thresholds related to section numbers.

        Args:
            data (np.ndarray): Particle data array, where the fourth column contains XS values.
            section_number (int): The current section number.

        Returns:
            int or None: XS key (e.g., 11, 41) or None if no match is found.

```
```
    def sum_global_var(self):

        Calculates the sum of three global variables defined in the config file.

        Global Variables (imported from config):
            var1 (float or int): The first variable.
            var2 (float or int): The second variable.
            var3 (float or int): The third variable.

        Returns:
            None (Prints the computed sum).

```
### Plotter Class
```
    def __call__(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity, section_number, xlim_left,
                 xlim_right):

        Creates a plot for the given particle data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.

```
```        
    def create_custom_cmap(self):

        Creates a custom rainbow colormap.

        :return: LinearSegmentedColormap object.

```
```
    def plot_data(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity,
                  section_number, xlim_left, xlim_right):

        Creates and saves a scatter plot for the data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.

```
```
    def setup_figure(self):

        Sets up the figure and axes for plotting.

        :return: Tuple (Figure, scatter axis, colorbar axis).

```
```
    def create_scatter_plot(self, ax, data, xlim_left, xlim_right):

        Generates a scatter plot of particle data, where colors represent velocity.

        Args:
            ax (matplotlib.axes.Axes): Matplotlib Axes object where the scatter plot will be drawn.
            data (numpy.ndarray): NumPy array containing particle data with columns [y, z, velocity].
            xlim_left (float): Left boundary for the x-axis.
            xlim_right (float): Right boundary for the x-axis.

        Returns:
            None (Modifies the provided Matplotlib Axes object with the scatter plot.)

```
```
    def reduce_particles(self, data, limit):

        Filters out particles with velocities below the specified limit.

        Args:
            data (np.ndarray): Array of particle data with attributes [Y, Z, Velocity, XS].
            limit (float): Minimum velocity threshold. Particles with velocities below this value are removed.

        Returns:
            np.ndarray: Filtered array containing only particles with velocities >= limit.

```
```
    def add_colorbar(self, fig, ax):

        Adds a colorbar to the plot.

        :param fig: Matplotlib Figure object.
        :param ax: Matplotlib Axes object for colorbar.

```
```
    def add_titles(self, fig, count, avg_particle, avg_velocity, sd_velocity, section_number):

        Adds titles to the plot.

        Args:
            fig (matplotlib.figure.Figure): Matplotlib figure object.
            count (int): Number of valid particles.
            avg_particle (float): Average particle count for the current XS.
            avg_velocity (float): Average velocity of particles.
            sd_velocity (float): Standard deviation of velocity.
            section_number (int): Section number being processed.

```
```
    def save_plot(self, section_number):

        Saves the plot as a PNG file.

        :param section_number: Section number for naming the file.

```
```
    def subtract_global_var(self):

        Calculates the difference of three global variables defined in the config file.

        Global Variables (imported from config):
            var1 (float or int): The first variable.
            var2 (float or int): The second variable.
            var3 (float or int): The third variable.

        Returns:
            None (Prints the computed difference).
```
### Main Class
```
    def __init__(self):

        Initializes the main class.

        Initializes data_list (list): A list to store data elements.
```
```

    def __call__(self):

        Main execution method that processes the log file, analyzes sections, and generates plots.

```
```     
    def calculate_panda_values(self):

        Processes collected particle data using Pandas for statistical analysis and storage.

        Args:
            None (Relies on self.data_list, which contains processed section data.)

        Returns:
            None (Outputs results to a CSV file and prints key statistical values.)

```
```
    def setup_section(self, section, calculation):

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

```
```
    def create_pictures(self, data, plotter, avg_particle, sd_velocity, valid_particle_count,
                        avg_velocity, left_value, right_value, section_number):

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

```
```        
    def process_section(self, section, calculation, plotter, avg_particles, section_number):

        Processes a single section of data.
        
        Args:
            section (list): List of strings representing the section.
            calculation (Calculation): Instance of the Calculation class.
            plotter (Plotter): Instance of the Plotter class.
            avg_particles (list): Average particle count across sections.
            section_number (int): Section number being processed.

```
