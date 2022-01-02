# RadPath

The purpose of this program is to generate a route through an area that covers every path specified, while minimising doing the same path twice (The Chinese Postman Problem).

## Dependencies
Python 3.9  
pip install numpy scipy pillow networkx

## Usage

* Step 1: Place the image you want to draw on into the "data" directory with the name "map.png"

* Step 2: Start the program (python src/main.py)

* Step 3: Click to place circles at any intersections you want

* Step 4: Click and drag to draw edges between the intersections

* Step 5: Press Enter to create a Radpath


Other notes:
- You can also click on existing nodes or click and drag on existing edges to remove them.
- The path will start from the first node you place
- After pressing Enter, you can save your radpaths by copying the edges.json file to somewhere else
- You can get an estimate for the length of your radpath by specifying the width of the map in main.py ACTUAL_WIDTH before you generate the radpath.