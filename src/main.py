import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import json
import matplotlib.pyplot as plt

from double_edges import choose_double_edges
from euler_path import euler_path
from path_variables import data_folder

CIRCLE_SIZE = 10
DOUBLE_EDGE_WIDTH = 5
BACKGROUND_FILENAME = data_folder / "map.png"
EDGES_FILENAME = data_folder / "edges.json"

# ACTUAL_WIDTH = 5.6   # Pinnacle
# ACTUAL_WIDTH = 2.7 # Black Mountain
# ACTUAL_WIDTH = 3.1 # Red Hill
# ACTUAL_WIDTH = 3.4 # Ainslie
ACTUAL_WIDTH = 3.1 # New Campbell
# ACTUAL_WIDTH = 2.8 # Campbell, Mt Rogers, Civic
# ACTUAL_WIDTH = 1.4 # Aranda bushland
# ACTUAL_WIDTH = 0.7 # Botanic gardens
# ACTUAL_WIDTH = 0.75 # Botanic gardens


class Radpath:

    # We need this to be a class so that we can access the canvas from outside functions
    def __init__(self):
        root = tk.Tk()
        # With this current system, you need to enter full screen mode for it to work properly
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        background_image = Image.open(BACKGROUND_FILENAME)
        background_image = self.rescale_background(background_image, screen_width, screen_height)
        self.background = ImageTk.PhotoImage(background_image)

        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.grid()
        self.canvas.bind('<ButtonPress-1>', self.mouse_press)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)
        self.canvas.bind('<KeyPress-Return>', self.calculate_route)
        self.canvas.focus_set()
        self.canvas.create_image(0, 0, image=self.background, anchor='nw')

        self.nodes = []
        self.node_drawings = []
        self.edges = []
        self.edge_drawings = []
        self.loop_drawings = []

        self.double_edges = []
        self.last_press = None
        self.last_line = None
        self.new_node = True

        self.preload_edges()
        root.mainloop()

    def rescale_background(self, background_image, screen_width, screen_height):
        """Adjust the image size to use the full screen width/height but without distorting the image"""
        screen_ratio = screen_width/screen_height
        image_width = background_image.width
        image_height = background_image.height
        image_ratio = image_width/image_height
        if image_ratio >= screen_ratio:
            image_width = screen_width
            image_height = image_width/image_ratio
        else:
            image_height = screen_height
            image_width = image_height * image_ratio
        background_image = background_image.resize((int(image_width), int(image_height)), Image.ANTIALIAS)
        return background_image
    
    def clear_nodes_and_edges(self):
        for edge_drawing in self.edge_drawings:
            self.canvas.delete(edge_drawing)
        for node_drawing in self.node_drawings:
            self.canvas.delete(node_drawing)

    def preload_edges(self):
        """Load from a previously saved set of edges"""
        self.clear_nodes_and_edges()
        # Load in the edges from file if the file exists
        try:
            with open(EDGES_FILENAME, 'r') as file:
                self.edges = json.load(file)
                # Nodes need to be tuples for dictionary hashing to work
                self.edges = [[tuple(edge[0]),tuple(edge[1])] for edge in self.edges]
        except:
            print("There is no edges.json file for preloading, so we are starting from scratch")
            return

        # Draw the edges
        for edge in self.edges:
            line = self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
            self.edge_drawings.append(line)

        # Extract and draw the nodes
        nodes = set()
        for edge in self.edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        self.nodes = list(nodes)
        for node in self.nodes:
            circle = self.draw_node(node)
            self.node_drawings.append(circle)

    def mouse_press(self, event):
        """If we press somewhere that doesn't yet have a node, then place a node there"""
        node = (event.x, event.y)
        self.new_node = self.overlapping_node(node) is None
        if self.new_node:
            circle = self.draw_node(node)
            self.nodes.append(node)
            self.node_drawings.append(circle)
        else:
            node = self.overlapping_node(node)
        self.last_press = node

    def mouse_drag(self, event):
        """If we press and drag, then draw a line from the last press position to the current mouse position"""
        self.canvas.delete(self.last_line)
        self.last_line = self.canvas.create_line(self.last_press[0], self.last_press[1], event.x, event.y)

    def mouse_release(self, event):
        """Create and delete a node and or edge based on this logic:
            1. if the 1st and 2nd nodes are the same and the 1st node is new then ignore it, otherwise delete it
            2. if the second node is new then create and draw it, if not then centre it
            3. if the edge is old then delete it, if not then create and draw it"""
        node1 = self.last_press
        node2 = (event.x, event.y)
        node2_centred = self.overlapping_node(node2)

        # 1. if the 1st and 2nd nodes are the same and the 1st node is new then ignore it, otherwise delete it
        if node1 == node2_centred:
            if self.new_node:
                self.canvas.delete(self.last_line)
                return
            # Don't delete a node if it's connected to an edge
            edge_nodes = {node for edge in self.edges for node in edge}
            if node1 in edge_nodes:
                self.canvas.delete(self.last_line)
                return
            else:
                index = self.nodes.index(node1)
                del self.nodes[index]
                self.canvas.delete(self.node_drawings[index])
                del self.node_drawings[index]

                self.canvas.delete(self.last_line)
                return

        # 2. if the second node is new then create and draw it, if not then centre it
        if node2_centred is None:
            circle = self.draw_node(node2)
            self.nodes.append(node2)
            self.node_drawings.append(circle)
        else:
            node2 = node2_centred

        # 3. if the edge is old then delete it, if not then create and draw it
        edge = [node1,node2]
        reverse_edge = [node2, node1]
        if edge in self.edges or reverse_edge in self.edges:
            edge = edge if edge in self.edges else reverse_edge
            index = self.edges.index(edge)
            del self.edges[index]
            self.canvas.delete(self.edge_drawings[index])
            del self.edge_drawings[index]
        else:
            line = self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
            self.edges.append(edge)
            self.edge_drawings.append(line)

        self.canvas.delete(self.last_line)

    def overlapping_node(self, node):
        """returns the centre coordinates of the node that overlaps, or None if none overlap"""
        for old_node in self.nodes:
            euclidian_distance = np.sqrt(np.square(node[0] - old_node[0]) + np.square(node[1] - old_node[1]))
            if euclidian_distance < CIRCLE_SIZE:
                return old_node
        return None

    def draw_node(self, node):
        """Draw the node centred at the coordinate"""
        return self.canvas.create_oval(node[0] - CIRCLE_SIZE / 2, node[1] - CIRCLE_SIZE / 2, node[0] + CIRCLE_SIZE / 2,
                                node[1] + CIRCLE_SIZE / 2)

    # Need to handle exceptions, e.g. empty graph
    def calculate_route(self, event):
        """Make the edges that need to be repeated get drawn in bold"""
        if self.edges == []:
            print("Cannot calculate route for an empty network")
            return

        for loop_drawing in self.loop_drawings:
            self.canvas.delete(loop_drawing)
        self.double_edges = choose_double_edges(self.edges)
        if self.double_edges is None:
            print("Cannot generate route if the graph is disjoint")
            return

        self.path, self.colours = euler_path(self.edges, self.double_edges)

        colour_map = plt.get_cmap('tab20').colors * 10
        rainbow = colour_map[6:8] + colour_map[2:6] + colour_map[0:2] + colour_map[8:]
        colour_ints = [[int(c*255) for c in colour] for colour in rainbow]
        colour_hex = ["#" + ''.join('%02x'%i for i in colour) for colour in colour_ints]

        # Draw each edge with it's given colours
        used_edges = set()
        for i, edge in enumerate(self.path):
            gradient = np.array(edge[1]) - np.array(edge[0])
            unit_vector = gradient / np.linalg.norm(gradient)
            rotation_matrix = [[0, 1], [-1, 0]]
            if edge in used_edges:
                rotation_matrix = [[0, -1], [1, 0]]
            new_vector = np.dot(rotation_matrix, unit_vector)
            dist = 3
            x_change = dist * new_vector[0]
            y_change = dist * new_vector[1]
            line = self.canvas.create_line(edge[0][0] + x_change,
                                    edge[0][1] + y_change, 
                                    edge[1][0] + x_change, 
                                    edge[1][1] + y_change, 
                                    width=DOUBLE_EDGE_WIDTH, 
                                    fill=colour_hex[self.colours[i]])
            self.loop_drawings.append(line)
            used_edges.add(edge)

        # Calculate the total length of the path
        route_length = total_length(self.path, self.background.width(), ACTUAL_WIDTH)
        print(f"Total length is about {round(route_length)}km, based on the 'ACTUAL_WIDTH'")
        
        # Save the edges to file
        with open(EDGES_FILENAME, 'w') as file:
            json.dump(self.edges, file)
        self.preload_edges()

def total_length(edges, window_width, real_life_width):
    """Calculate the total length of the route"""
    total_length = 0
    for edge in edges:
        total_length += np.linalg.norm(np.array(edge[0]) - np.array(edge[1]))   # Euclidean distance
    scaling_factor = real_life_width / window_width
    actual_length = total_length * scaling_factor
    return actual_length

if __name__ == '__main__':
    Radpath()