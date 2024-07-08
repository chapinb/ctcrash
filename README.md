# ctcrash

Notebooks and utilities for analyzing data from the UCONN CT Crash Data Repository.

## Repository structure

Data is stored in `data/` with exported CSVs from the https://www.ctcrash.uconn.edu/ site.

Utilities for loading the data, generating pivot tables, charts, and maps are located in `src/ctcrash/`

Notebooks, in `notebooks/` use the utilities to load the CSV data and create charts and visualizations to help interpret the data.

## Use

To run the notebooks locally, install [rye](https://rye.astral.sh/) and run the following from the same directory as this README:
1. `rye install`
2. `rye run jupyter lab`

Open the browser to view the Jupyter lab, and run the cells to generate the visualization.
