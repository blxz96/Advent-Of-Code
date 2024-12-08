from collections import defaultdict
import Utils

class ResonantCollinearity:

    def __init__(self):
        self.grid = []
        self.rows_length = 0
        self.cols_length = 0
        self.element_to_locations = defaultdict(list)
        self.anti_nodes = set()

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                row = list(line)
                self.grid.append(row)
        self.rows_length = len(self.grid)
        self.cols_length = len(self.grid[0])

    # Populate location of each element
    def populate_location_of_element(self):
        for row in range(self.rows_length):
            for col in range(self.cols_length):
                element = self.grid[row][col]
                if element != '.':
                    self.element_to_locations[element].append((row, col))
    def find_part_1_ans(self):
        # Retrieve location of elements
        elements = self.element_to_locations.keys()
        for element in elements:
            self.compute_anti_node_locations_of_element(element)
        return len(self.anti_nodes)

    def compute_anti_node_locations_of_element(self, element):
        locations_of_element = self.element_to_locations[element]
        if len(locations_of_element) < 2:
            return
        # We compare 2 locations every time
        for i in range(len(locations_of_element)):
            for j in range(i + 1, len(locations_of_element)):
                location1 = locations_of_element[i]
                location2 = locations_of_element[j]
                dr = abs(location1[0] - location2[0])
                dc = abs(location1[1] - location2[1])
                location1_row_is_greater = location1[0] >= location2[0]
                location1_col_is_greater = location1[1] >= location2[1]
                location1_anti_node = self.generate_new_anti_node_location1(dc, dr, location1,
                                                                            location1_row_is_greater,
                                                                            location1_col_is_greater)
                location2_anti_node = self.generate_new_anti_node_location2(dc, dr, location2,
                                                                            location1_row_is_greater,
                                                                            location1_col_is_greater)
                # We need to check if anti-node location is within bound
                if self.is_valid(location1_anti_node):
                    self.anti_nodes.add(location1_anti_node)
                if self.is_valid(location2_anti_node):
                    self.anti_nodes.add(location2_anti_node)

    def is_valid(self, location):
        return 0 <= location[0] < self.rows_length and 0 <= location[1] < self.cols_length

    def find_part_2_ans(self):
        # An element can be an anti-node itself too (as long as there is more than 1 of it)
        # We also need to take care of resonant harmonics
        elements = self.element_to_locations.keys()
        for element in elements:
            self.compute_anti_node_locations_of_element_part_2(element)
        return len(self.anti_nodes)

    def compute_anti_node_locations_of_element_part_2(self, element):
        locations_of_element = self.element_to_locations[element]
        # We compare 2 locations every time
        if len(locations_of_element) < 2:
            return
        for i in range(len(locations_of_element)):
            for j in range(i + 1, len(locations_of_element)):
                location1 = locations_of_element[i]
                location2 = locations_of_element[j]
                dr = abs(location1[0] - location2[0])
                dc = abs(location1[1] - location2[1])
                location1_row_is_greater = location1[0] >= location2[0]
                location1_col_is_greater = location1[1] >= location2[1]
                # For part 2, original location can also be anti-nodes
                location1_anti_node = location1
                location2_anti_node = location2
                # While anti node generated is valid, add to set and generate more anti-node
                while self.is_valid(location1_anti_node):
                    self.anti_nodes.add(location1_anti_node)
                    location1_anti_node = self.generate_new_anti_node_location1(dc, dr, location1_anti_node,
                                                                                location1_row_is_greater,
                                                                                location1_col_is_greater)

                while self.is_valid(location2_anti_node):
                    self.anti_nodes.add(location2_anti_node)
                    location2_anti_node = self.generate_new_anti_node_location2(dc, dr, location2_anti_node,
                                                                                location1_row_is_greater,
                                                                                location1_col_is_greater)

    def generate_new_anti_node_location1(self, dc, dr, original_location1_anti_node, condition1, condition2):
        location1_anti_node_row = original_location1_anti_node[0] + dr if condition1 else original_location1_anti_node[0] - dr
        location1_anti_node_col = original_location1_anti_node[1] + dc if condition2 else original_location1_anti_node[1] - dc
        location1_anti_node = (location1_anti_node_row, location1_anti_node_col)
        return location1_anti_node

    def generate_new_anti_node_location2(self, dc, dr, original_location_2_anti_node, condition1, condition2):
        location2_anti_node_row = original_location_2_anti_node[0] - dr if condition1 else original_location_2_anti_node[0] + dr
        location2_anti_node_col = original_location_2_anti_node[1] - dc if condition2 else original_location_2_anti_node[1] + dc
        location2_anti_node = (location2_anti_node_row, location2_anti_node_col)
        return location2_anti_node


if __name__ == '__main__':
    p = ResonantCollinearity()
    p.read_file('input8.txt')
    p.populate_location_of_element()
    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
