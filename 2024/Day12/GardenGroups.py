import Utils


class GardenGroups:
    def __init__(self):
        self.grid = []
        self.is_visited = set()
        self.row_length = 0
        self.col_length = 0
        self.direction = {
            (-1, 0),  # UP
            (1, 0),  # DOWN
            (0, -1),  # LEFT
            (0, 1),  # RIGHT
        }
        self.current_area = 0
        self.current_number_of_fences = 0
        self.current_number_of_sides = 0

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                row = list(line)
                self.grid.append(row)
        self.row_length, self.col_length = len(self.grid), len(self.grid[0])
        return self.grid

    def find_part_1_ans(self):
        """
        1. need is_valid function to check if a location is within bound
        2. dfs - is_visited set
        3. direction - UP, DOWN, LEFT, RIGHT
        4. function to compute how many fence a position needs - need to get neighbour too
        :return:
        """
        ans = 0
        for row in range(self.row_length):
            for col in range(self.col_length):
                if (row, col) not in self.is_visited:
                    # reset
                    self.current_area = 0
                    self.current_number_of_fences = 0
                    self.compute_area_and_number_of_fences(row, col)
                    ans += self.current_area * self.current_number_of_fences

        return ans

    def is_valid(self, row, col, letter):
        # if is_valid, then return true and don't need to add fence
        return 0 <= row < self.row_length and 0 <= col < self.col_length and self.grid[row][col] == letter

    def compute_number_of_fences(self, row, col):
        # check the different direction and see if there's a need to add fence
        number_of_fences = 0
        letter = self.grid[row][col]
        for dr, dc in self.direction:
            new_row = row + dr
            new_col = col + dc
            if not self.is_valid(new_row, new_col, letter):
                number_of_fences += 1
        return number_of_fences

    def compute_area_and_number_of_fences(self, row, col):
        self.is_visited.add((row, col))
        self.current_number_of_fences += self.compute_number_of_fences(row, col)
        self.current_area += 1
        letter = self.grid[row][col]
        for dr, dc in self.direction:
            new_row = row + dr
            new_col = col + dc
            if self.is_valid(new_row, new_col, letter) and (new_row, new_col) not in self.is_visited:
                self.compute_area_and_number_of_fences(new_row, new_col)

    def find_part_2_ans(self):
        """
        1. same thing, but now we compute number of sides (corner) of a region
        :return:
        """
        ans = 0
        for row in range(self.row_length):
            for col in range(self.col_length):
                if (row, col) not in self.is_visited:
                    # reset
                    self.current_area = 0
                    self.current_number_of_sides = 0
                    self.compute_area_and_number_of_sides(row, col)
                    ans += self.current_area * self.current_number_of_sides

        return ans

    def compute_number_of_sides(self, row, col):
        # number of sides = number of corners
        number_of_corners = 0
        letter = self.grid[row][col]

        displacement_up = (-1, 0)
        displacement_down = (1, 0)
        displacement_left = (0, -1)
        displacement_right = (0, 1)
        displacement_up_left = (-1, -1)
        displacement_up_right = (-1, 1)
        displacement_down_left = (1, -1)
        displacement_down_right = (1, 1)

        is_valid_up = self.is_valid(row + displacement_up[0], col + displacement_up[1], letter)
        is_valid_down = self.is_valid(row + displacement_down[0], col + displacement_down[1], letter)
        is_valid_left = self.is_valid(row + displacement_left[0], col + displacement_left[1], letter)
        is_valid_right = self.is_valid(row + displacement_right[0], col + displacement_right[1], letter)
        is_valid_up_left = self.is_valid(row + displacement_up_left[0], col + displacement_up_left[1], letter)
        is_valid_up_right = self.is_valid(row + displacement_up_right[0], col + displacement_up_right[1], letter)
        is_valid_down_left = self.is_valid(row + displacement_down_left[0], col + displacement_down_left[1], letter)
        is_valid_down_right = self.is_valid(row + displacement_down_right[0], col + displacement_down_right[1], letter)

        if not is_valid_left and not is_valid_up:
            number_of_corners += 1
        if not is_valid_up and not is_valid_right:
            number_of_corners += 1
        if not is_valid_down and not is_valid_right:
            number_of_corners += 1
        if not is_valid_left and not is_valid_down:
            number_of_corners += 1
        if is_valid_left and is_valid_up and not is_valid_up_left:
            number_of_corners += 1
        if is_valid_up and is_valid_right and not is_valid_up_right:
            number_of_corners += 1
        if is_valid_down and is_valid_right and not is_valid_down_right:
            number_of_corners += 1
        if is_valid_left and is_valid_down and not is_valid_down_left:
            number_of_corners += 1

        return number_of_corners

    def compute_area_and_number_of_sides(self, row, col):
        self.is_visited.add((row, col))
        self.current_number_of_sides += self.compute_number_of_sides(row, col)
        self.current_area += 1
        letter = self.grid[row][col]
        for dr, dc in self.direction:
            new_row = row + dr
            new_col = col + dc
            if self.is_valid(new_row, new_col, letter) and (new_row, new_col) not in self.is_visited:
                self.compute_area_and_number_of_sides(new_row, new_col)

if __name__ == '__main__':
    p = GardenGroups()
    p.read_file('input12.txt')
    Utils.eval_and_time_function(p.find_part_1_ans)
    p.is_visited = set()
    Utils.eval_and_time_function(p.find_part_2_ans)