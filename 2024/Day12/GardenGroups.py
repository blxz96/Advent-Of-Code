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


if __name__ == '__main__':
    p = GardenGroups()
    p.read_file('input12.txt')
    Utils.eval_and_time_function(p.find_part_1_ans)
    p.is_visited = set()
