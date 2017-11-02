This GitHub repository is created for use on the NREL High-Throughput Experimental Materials Database (https://htem.nrel.gov/). While the database offers a number of visualization tools for various types of materials tests, an advanced user may desire a more hands-on approach. This repository offers a number of Jupyter notebooks that interact directly with the API in order to do more advanced statistical analysis and graphical visualization. The Jupyter notebooks allow one to read and digest blocks of code while learning more about how various statistical techniques may be applied to this dataset. This repository is currently broken into several Python files and then five Jupyter Notebooks. They are:




library.py: See the "lib" folder. This file contains a class that is designed to query data from the API at the library level (all 44 points).

sample.py: See the "lib" folder. This file contains a class that is designed to query data from the API at the sample level (individual points).




1_Basic_Queries.ipynb: Gives a brief introduction of how to use the Library and Sample modules to query information at different levels.

2_XRD_Plotting.ipynb: Takes a look at how x-ray diffraction spectra may be easily plotted and how basic peak detection may be implemented.

3_XRF_Plotting.ipynb: Analyzes how data from x-ray fluorescence measurements (including thickness, composition, etc.), heat maps are used to reveal gradients across substrates and other phenomena.

4_Four_Point_Plotting.ipynb: Analyzes data from four-point probe (4PP) measurements, which yields electrical measurements such as sheet resistance, conductivity, etc. Heatmap plots may be made to show how conductivity changes with respect to composition and position.

5_Optical_Plotting.ipynb: Analyzes optical measurements, which includes spectra from near-infrared ranges to ultra-violet ranges. Demonstrates some basic plotting as well as absorption coefficient calculations and basic Tauc plotting.

To get started, download Anaconda or another distribution of Python. Make sure that pandas, numpy, and scipy are all included in the distribution. One can then clone the repository using the command:

git clone https://github.com/NREL/htem-api-examples.git
cd htem-api-examples.git

The updated repository should then be available.

Finally, you can use Jupyter Notebook to view the example notebooks. First, navigate to the directory, then enter:
cd notebooks
jupyter notebook
