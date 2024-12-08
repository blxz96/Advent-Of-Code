from collections import defaultdict
import Utils

class CeresSearch:

    def __init__(self):
        self.grid = []
        self.rows_length = 0
        self.cols_length = 0
        # Used for part 1
        self.octagonal_displacements = {
            (0, 1),  # Right
            (0, -1),  # Left
            (1, 0),  # Down
            (-1, 0),  # Up
            (1, 1),  # Down-right
            (1, -1),  # Down-left
            (-1, 1),  # Up-right
            (-1, -1)  # Up-left
        }
        # Used for part 2
        self.diagonal_displacements = {
            (1, 1),  # Down-right
            (1, -1),  # Down-left
            (-1, 1),  # Up-right
            (-1, -1)  # Up-left
        }

    def read_file_and_initialize_variables(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                row = list(line.strip())
                self.grid.append(row)
        self.rows_length = len(self.grid)
        self.cols_length = len(self.grid[0])

    def find_part_1_ans(self, word):
        ans = 0
        for r in range(self.rows_length):
            for c in range(self.cols_length):
                # Only check if the first word matches before proceeding
                if self.grid[r][c] == word[0]:
                    for dr, dc in self.octagonal_displacements:
                        if self.check_word_part_1(r, c, dr, dc, word):
                            ans += 1
        return ans

    def check_word_part_1(self, row, col, row_displacement, col_displacement, word):
        for idx, char in enumerate(word):
            new_row = row + row_displacement * idx
            new_col = col + col_displacement * idx
            if not self.is_valid(new_row, new_col, lambda: char == self.grid[new_row][new_col]):
                return False
        return True

    def is_valid(self, row, col, lazy_eval_condition):
        # Note lazy_eval_condition() , the bracket is important to execute it, if not it won't be executed
        return 0 <= row < self.rows_length and 0 <= col < self.cols_length and lazy_eval_condition()

    def find_part_2_ans(self):
        ans = 0
        for r in range(self.rows_length):
            for c in range(self.cols_length):
                if self.grid[r][c] == 'A' and self.check_word_part_2(r, c):
                    ans += 1
        return ans

    def check_word_part_2(self, row, col):
        permissible = {'M', 'S'}
        mappings = defaultdict(str)
        for row_displacement, col_displacement in self.diagonal_displacements:
            new_row = row + row_displacement
            new_col = col + col_displacement
            # Beyond the bound or not permissible char found
            if not self.is_valid(new_row, new_col, lambda: self.grid[new_row][new_col] in permissible):
                return False
            mappings[(row_displacement, col_displacement)] = self.grid[new_row][new_col]
        # Polar opposite coordinates should not be the same character
        if mappings[(1, 1)] == mappings[(-1, -1)] or mappings[(1, -1)] == mappings[(-1, 1)]:
            return False
        return True


if __name__ == '__main__':
    p = CeresSearch()
    p.read_file_and_initialize_variables('input4.txt')
    Utils.eval_and_time_function(p.find_part_1_ans,'XMAS')
    Utils.eval_and_time_function(p.find_part_2_ans)
