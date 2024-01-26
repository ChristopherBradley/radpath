# RadPath
This app aims to generate a nice route through every path on a map.

## Setup
Download miniconda: https://docs.conda.io/projects/miniconda/en/latest/
Download homebrew: https://brew.sh/
Create an environment: `conda create --name radpath`
Activate environment:  `conda activate radpath`
Install dependencies: `pip install numpy scipy pillow networkx matplotlib` 
Install ghostscript: `brew install ghostscript`

## Usage
 
* Step 1: Start the program `python src/main.py`

* Step 2: Upload an image of a map with the "Upload Basemap" button

* Step 3: Click and drag on the map to draw (or remove) nodes and edges

* Step 4: Click "Generate Route" and wait for the algorithm to finish

* Step 5: Click "Download Route" (or take a screenshot) to save a copy

Happy running!