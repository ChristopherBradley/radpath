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
    - You can also click on existing edges or click and drag on existing nodes to remove them.

* Step 5: Press Enter to create a Radpath


Other notes:
- The path will start from the first node you place