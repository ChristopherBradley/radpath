import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

from double_edges import choose_double_edges
from euler_path import euler_path
from path_variables import data_folder

CIRCLE_SIZE = 10
DOUBLE_EDGE_WIDTH = 5
FILENAME = data_folder / "map.png"

# Ainslie bug
# PRELOADED_EDGES = [[(398, 766), (412, 745)], [(412, 745), (443, 763)], [(443, 763), (398, 766)], [(398, 766), (393, 731)], [(393, 731), (412, 745)], [(412, 745), (429, 697)], [(429, 697), (484, 754)], [(484, 754), (443, 763)], [(484, 754), (515, 738)], [(515, 738), (480, 694)], [(480, 694), (429, 697)], [(480, 694), (500, 673)], [(500, 673), (523, 726)], [(523, 726), (515, 738)], [(515, 738), (532, 771)], [(532, 771), (513, 783)], [(513, 783), (484, 754)], [(532, 771), (571, 782)], [(571, 782), (535, 796)], [(535, 796), (532, 771)], [(535, 796), (513, 783)], [(535, 796), (592, 830)], [(592, 830), (593, 805)], [(593, 805), (618, 840)], [(618, 840), (592, 830)], [(593, 805), (571, 782)], [(571, 782), (594, 731)], [(594, 731), (576, 725)], [(576, 725), (603, 683)], [(603, 683), (594, 731)], [(576, 725), (543, 707)], [(543, 707), (523, 726)], [(543, 707), (546, 669)], [(546, 669), (536, 582)], [(536, 582), (521, 593)], [(521, 593), (521, 615)], [(521, 615), (492, 592)], [(492, 592), (503, 627)], [(503, 627), (500, 673)], [(603, 683), (584, 636)], [(584, 636), (619, 592)], [(619, 592), (600, 572)], [(600, 572), (546, 669)], [(600, 572), (584, 478)], [(584, 478), (557, 495)], [(557, 495), (527, 488)], [(527, 488), (536, 582)], [(557, 495), (582, 461)], [(582, 461), (596, 406)], [(596, 406), (553, 312)], [(553, 312), (527, 329)], [(527, 329), (512, 386)], [(512, 386), (489, 391)], [(489, 391), (442, 421)], [(442, 421), (527, 488)], [(442, 421), (400, 485)], [(400, 485), (422, 561)], [(422, 561), (442, 611)], [(442, 611), (503, 627)], [(422, 561), (393, 608)], [(393, 608), (391, 557)], [(391, 557), (422, 561)], [(391, 557), (371, 553)], [(371, 553), (374, 669)], [(374, 669), (394, 662)], [(394, 662), (393, 608)], [(374, 669), (378, 686)], [(378, 686), (429, 697)], [(393, 731), (378, 707)], [(378, 707), (378, 686)], [(618, 840), (623, 859)], [(623, 859), (596, 862)], [(596, 862), (592, 830)], [(623, 859), (640, 862)], [(640, 862), (657, 729)], [(657, 729), (646, 683)], [(646, 683), (603, 683)], [(646, 683), (646, 623)], [(646, 623), (701, 478)], [(701, 478), (654, 413)], [(654, 413), (622, 398)], [(622, 398), (614, 411)], [(614, 411), (584, 478)], [(371, 553), (362, 507)], [(362, 507), (397, 472)], [(397, 472), (400, 485)], [(397, 472), (372, 410)], [(372, 410), (352, 449)], [(352, 449), (362, 507)], [(362, 507), (335, 451)], [(335, 451), (352, 449)], [(335, 451), (332, 404)], [(332, 404), (350, 386)], [(350, 386), (385, 397)], [(385, 397), (372, 410)], [(385, 397), (442, 421)], [(332, 404), (340, 373)], [(340, 373), (350, 386)], [(350, 386), (369, 372)], [(369, 372), (340, 373)], [(369, 372), (378, 349)], [(378, 349), (398, 294)], [(398, 294), (382, 289)], [(382, 289), (340, 373)], [(398, 294), (414, 321)], [(414, 321), (408, 336)], [(408, 336), (378, 349)], [(414, 321), (428, 326)], [(428, 326), (408, 336)], [(408, 336), (405, 366)], [(405, 366), (385, 397)], [(428, 326), (489, 391)], [(512, 386), (445, 310)], [(445, 310), (428, 326)], [(445, 310), (428, 287)], [(428, 287), (414, 321)], [(428, 287), (395, 271)], [(395, 271), (382, 289)], [(395, 271), (437, 237)], [(437, 237), (428, 287)], [(437, 237), (452, 229)], [(452, 229), (487, 270)], [(487, 270), (445, 310)], [(487, 270), (558, 230)], [(558, 230), (570, 267)], [(570, 267), (527, 329)], [(570, 267), (613, 309)], [(613, 309), (553, 312)], [(613, 309), (635, 308)], [(635, 308), (680, 380)], [(680, 380), (617, 367)], [(617, 367), (595, 378)], [(595, 378), (596, 406)], [(680, 380), (706, 308)], [(706, 308), (658, 285)], [(658, 285), (635, 308)], [(658, 285), (654, 239)], [(654, 239), (614, 214)], [(614, 214), (558, 230)], [(452, 229), (488, 144)], [(488, 144), (490, 122)], [(490, 122), (588, 164)], [(588, 164), (614, 214)], [(558, 230), (488, 144)], [(490, 122), (576, 78)], [(576, 78), (600, 87)], [(600, 87), (588, 164)], [(600, 87), (625, 91)], [(625, 91), (717, 168)], [(717, 168), (614, 214)], [(717, 168), (785, 213)], [(785, 213), (804, 222)], [(804, 222), (810, 246)], [(810, 246), (813, 358)], [(813, 358), (797, 509)], [(797, 509), (788, 657)], [(788, 657), (787, 698)], [(787, 698), (789, 822)], [(789, 822), (732, 857)], [(732, 857), (684, 731)], [(684, 731), (787, 698)], [(684, 731), (657, 729)], [(732, 857), (721, 883)], [(721, 883), (640, 862)], [(721, 883), (642, 898)], [(642, 898), (623, 859)], [(642, 898), (640, 862)], [(788, 657), (737, 601)], [(737, 601), (701, 478)], [(788, 657), (712, 412)], [(712, 412), (793, 349)], [(793, 349), (813, 358)], [(793, 349), (680, 380)], [(793, 349), (804, 277)], [(804, 277), (749, 234)], [(749, 234), (706, 308)], [(749, 234), (754, 223)], [(754, 223), (810, 246)], [(749, 234), (705, 192)], [(705, 192), (614, 214)]]

ACTUAL_WIDTH = 5.6   # Mt Ainslie
# ACTUAL_WIDTH = 2.8   # Campbell
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
        print(self.nodes, self.edges)
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
        print(f"PRELOADED_EDGES = {self.edges}")
        if self.edges == []:
            print("Cannot calculate route for an empty network")
            return

        for number_drawing in self.number_drawings:
            self.canvas.delete(number_drawing)
        self.double_edges = choose_double_edges(self.edges)
        if self.double_edges is None:
            print("Cannot generate route if the graph is disjoint")
            return

        # Make the double edges bold
        for edge in self.double_edges:
            self.canvas.create_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1], width=DOUBLE_EDGE_WIDTH)

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
            number_drawing = self.canvas.create_text(offset_midpoint[0], offset_midpoint[1], fill="darkblue", font="Times 10 bold",
                                    text=i)
            self.number_drawings.append(number_drawing)
            used_edges.add(edge)
        # print(f"path: {self.path}")

        # Calculate the total length of the path
        route_length = total_length(self.edges + self.double_edges, self.background.width(), ACTUAL_WIDTH)
        print(f"Total length is about {round(route_length)}km, based on the 'ACTUAL_WIDTH'")

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