import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

from double_edges import choose_double_edges
from euler_path import euler_path

CIRCLE_SIZE = 10
DOUBLE_EDGE_WIDTH = 5
FILENAME = "data/map.png"
# PRELOADED_EDGES = [[(484, 468), (431, 422)], [(484, 468), (441, 488)], [(484, 468), (481, 526)], [(481, 526), (404, 549)], [(404, 549), (332, 523)], [(332, 523), (359, 490)], [(359, 490), (400, 499)], [(400, 499), (441, 488)], [(441, 488), (427, 505)], [(427, 505), (400, 499)], [(359, 490), (382, 463)], [(382, 463), (361, 425)], [(382, 463), (431, 422)], [(431, 422), (459, 379)], [(361, 425), (415, 350)], [(415, 350), (459, 379)], [(415, 350), (376, 330)], [(415, 350), (427, 300)], [(427, 300), (397, 300)], [(397, 300), (376, 330)], [(427, 300), (468, 294)], [(468, 294), (470, 357)], [(470, 357), (459, 379)], [(484, 468), (522, 440)], [(522, 440), (506, 415)], [(506, 415), (509, 364)], [(509, 364), (470, 357)], [(522, 440), (545, 418)], [(545, 418), (561, 395)], [(561, 395), (585, 410)], [(481, 526), (510, 547)], [(510, 547), (487, 590)], [(487, 590), (528, 549)], [(528, 549), (510, 547)], [(528, 549), (543, 548)], [(543, 548), (536, 509)], [(543, 548), (587, 540)], [(587, 540), (575, 481)], [(575, 481), (589, 456)], [(545, 418), (585, 410)], [(585, 410), (589, 456)], [(575, 481), (522, 440)], [(589, 456), (630, 467)], [(630, 467), (674, 456)], [(674, 456), (678, 439)], [(727, 472), (661, 507)], [(661, 507), (674, 456)], [(661, 507), (645, 531)], [(645, 531), (620, 536)], [(620, 536), (627, 584)], [(620, 536), (587, 540)], [(627, 584), (685, 573)], [(685, 573), (726, 494)], [(726, 494), (727, 472)], [(727, 472), (737, 456)], [(737, 456), (731, 417)], [(731, 417), (717, 388)], [(717, 388), (703, 349)], [(703, 349), (660, 290)], [(660, 290), (633, 328)], [(633, 328), (619, 321)], [(619, 321), (601, 360)], [(660, 290), (582, 259)], [(582, 259), (550, 249)], [(550, 249), (527, 245)], [(527, 245), (467, 243)], [(383, 236), (311, 332)], [(311, 332), (274, 383)], [(311, 332), (350, 364)], [(350, 364), (376, 330)], [(468, 294), (467, 243)], [(468, 294), (530, 283)], [(530, 283), (527, 245)], [(530, 283), (534, 294)], [(534, 294), (537, 304)], [(537, 304), (518, 309)], [(534, 294), (553, 290)], [(553, 290), (619, 321)], [(633, 328), (654, 348)], [(654, 348), (668, 398)], [(668, 398), (678, 439)], [(668, 398), (717, 388)], [(668, 398), (628, 411)], [(628, 411), (616, 370)], [(616, 370), (601, 360)], [(601, 360), (566, 347)], [(566, 347), (551, 352)], [(551, 352), (561, 395)], [(551, 352), (537, 304)], [(551, 352), (509, 364)], [(585, 410), (604, 418)], [(604, 418), (628, 411)], [(627, 584), (534, 605)], [(534, 605), (488, 609)], [(488, 609), (487, 590)], [(487, 590), (452, 614)], [(452, 614), (455, 590)], [(455, 590), (487, 590)], [(488, 609), (450, 633)], [(450, 633), (452, 614)], [(361, 425), (336, 382)], [(336, 382), (350, 364)], [(450, 633), (434, 645)], [(434, 645), (311, 557)], [(311, 557), (332, 523)], [(332, 523), (307, 499)], [(307, 499), (282, 537)], [(282, 537), (311, 557)], [(307, 499), (278, 466)], [(278, 466), (314, 413)], [(314, 413), (274, 383)], [(274, 383), (237, 433)], [(237, 433), (278, 466)], [(237, 433), (206, 475)], [(206, 475), (247, 508)], [(247, 508), (278, 466)], [(247, 508), (282, 537)], [(314, 413), (336, 382)], [(307, 499), (324, 476)], [(324, 476), (359, 490)], [(324, 476), (334, 437)], [(334, 437), (314, 413)], [(334, 437), (361, 425)], [(427, 241), (427, 300)], [(383, 236), (427, 241)], [(427, 241), (467, 243)]]


ACTUAL_WIDTH = 2.8   # Campbell
# ACTUAL_WIDTH = 1.4 # Aranda bushland


class Radpath:

    # We need this to be a class so that we can access the canvas from outside functions
    def __init__(self):
        root = tk.Tk()
        # With this current system, you need to enter full screen mode for it to work properly
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        background_image = Image.open(FILENAME)
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
        self.number_drawings = []

        self.double_edges = []
        self.last_press = None
        self.last_line = None
        self.new_node = True

        try:
            self.preload_edges(PRELOADED_EDGES)
        except:
            pass
        self.initial_nodes(self.edges)
        # self.show_double_edges("bla")   # for debugging
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

    def preload_edges(self, edges):
        """Load from a previously saved set of edges"""
        self.edges = edges
        for edge in self.edges:
            line = self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
            self.edge_drawings.append(line)

    def initial_nodes(self, edges):
        """Extract nodes from the edges without duplicates. If no edges then the list starts empty"""
        nodes = set()
        for edge in edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        self.nodes = list(nodes)
        for node in self.nodes:
            circle = self.draw_node(node)
            self.node_drawings.append(circle)

    def mouse_press(self, event):
        """If we press somewhere that doesn't yet have a node, then place a node there"""
        node = (event.x, event.y)
        self.new_node = self.node_is_new(node)
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
        """Create a new node if there wasn't one. Then create a new edge if there wasn't one."""
        node = self.snap_to_node(event)
        edge = [self.last_press, node]
        reverse_edge = [node, self.last_press]
        if not self.new_node and edge[0] == edge[1]:
            # TODO: Need to make sure I can still create new nodes
            edge_nodes = [node for edge in self.edges for node in edge]
            if node not in edge_nodes:
                # Remove the node
                index = self.nodes.index(node)
                del self.nodes[index]
                self.canvas.delete(self.node_drawings[index])
                del self.node_drawings[index]
        elif edge not in self.edges and reverse_edge not in self.edges and edge[0] != edge[1]:
            # Add the edge
            line = self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
            self.edges.append(edge)
            self.edge_drawings.append(line)
        else:
            # Remove the edge
            # TODO: Found an error here where I could not index the error. Need to figure out how to reproduce
            index = self.edges.index(edge if edge in self.edges else reverse_edge)
            del self.edges[index]
            self.canvas.delete(self.edge_drawings[index])
            del self.edge_drawings[index]
            # TODO: I also need to delete the number
        self.canvas.delete(self.last_line)

    def node_is_new(self, node):
        """Checks if we already have a node that covers this position"""
        for old_node in self.nodes:
            euclidian_distance = np.sqrt(np.square(node[0] - old_node[0]) + np.square(node[1] - old_node[1]))
            if euclidian_distance < CIRCLE_SIZE:
                return False
        return True

    def overlapping_node(self, node):
        """returns the centre coordinates of the node that overlaps"""
        for old_node in self.nodes:
            euclidian_distance = np.sqrt(np.square(node[0] - old_node[0]) + np.square(node[1] - old_node[1]))
            if euclidian_distance < CIRCLE_SIZE:
                return old_node
        return None

    def snap_to_node(self, event):
        """Create a new node, or return an existing node if it overlaps"""
        node = (event.x, event.y)
        if self.node_is_new(node):
            circle = self.draw_node(node)
            self.nodes.append(node)
            self.node_drawings.append(circle)
        else:
            node = self.overlapping_node(node)
        return node

    def draw_node(self, node):
        """Draw the node centred at the coordinate"""
        return self.canvas.create_oval(node[0] - CIRCLE_SIZE / 2, node[1] - CIRCLE_SIZE / 2, node[0] + CIRCLE_SIZE / 2,
                                node[1] + CIRCLE_SIZE / 2)

    # Need to handle exceptions, e.g. empty graph
    def calculate_route(self, event):
        """Make the edges that need to be repeated get drawn in bold"""
        print("Enter pressed")
        for number in self.number_drawings:
            self.canvas.delete(number)
        self.double_edges = choose_double_edges(self.edges)

        # Make the double edges bold
        # for edge in self.double_edges:
        #     self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1], width=DOUBLE_EDGE_WIDTH)
        # print(self.double_edges)

        self.path = euler_path(self.edges, self.double_edges)
        used_edges = set()

        # line_colours = self.generate_colours(len(self.path))
        for i, edge in enumerate(self.path):
            midpoint = ((edge[0][0] + edge [1][0])/2, (edge[0][1] + edge [1][1])/2)
            gradient = np.array(edge[1]) - np.array(edge[0])
            unit_vector = gradient / np.linalg.norm(gradient)

            rotation_matrix = [[0, 1], [-1, 0]]
            if edge in used_edges:
                # Place the number on the other side of the double edge
                rotation_matrix = [[0, -1], [1, 0]]
            new_vector = np.dot(rotation_matrix, unit_vector)

            dist = 5
            x_change = dist * new_vector[0]
            y_change = dist * new_vector[1]
            offset_midpoint = (midpoint[0] + x_change, midpoint[1] + y_change)

            # self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1], width=1, fill='black')
            number = self.canvas.create_text(offset_midpoint[0], offset_midpoint[1], fill="darkblue", font="Times 10 bold",
                                    text=i)
            self.number_drawings.append(number)
            used_edges.add(edge)
        # print(f"path: {self.path}")

        # Calculate the total length of the path
        route_length = total_length(self.edges + self.double_edges, self.background.width(), ACTUAL_WIDTH)
        print(f"Total length is about {round(route_length)}km, based on the 'ACTUAL_WIDTH'")
        print(f"PRELOADED_EDGES = {self.edges}")

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