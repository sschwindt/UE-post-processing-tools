# post-processing-tools-for-Unreal-Engine-simulations

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
> * Compute statistical metrics: Calculate average particle counts, velocity distributions, and standard deviations per section.
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

`python dataProcessing(new).py`

### Expected Output

* If enabled in config: Scatter plots saved as PNG files

![section_plot](https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations/blob/main/images/section_plot_1.png)
*<sub>A sample plot. (source: Benjamin Kemmler 2025).</sub>*
* Processed data saved as `Values.csv`

Customization

Modify parameters in config.py to adjust the input file path and settings for processing and visualization.


For any issues, please refer to the script comments and error messages stated below.

The process sequence of the program is shown in the flow chart below
![flowChart](https://github.com/Benni1998/post-processing-tools-for-Unreal-Engine-simulations/blob/main/images/flowChart.png)
*<sub>General flow chart of the provided code in `dataProcessing` (source: Benjamin Kemmler 2025).</sub>*

TODO COMMENTS

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-SequentPeak.git
```




![sequentpeak](https://github.com/Ecohydraulics/media/raw/main/png/sequent_peak.png)

The sequent peak algorithm repeats this calculation over multiple years and the highest volume observed determines the required volume.

In this exercise, we use daily flow measurements from Vanilla River (in Vanilla-arid country with monsoon periods) and target outflow volumes to supply farmers and the population of Vanilla-arid country with sufficient water during the dry seasons. This exercise guides you through loading the daily discharge data, creating the monthly *SD* (storage) curve, and calculating the required storage volume.

