import Utils


class HoofIt:
    def __init__(self):
        self.grid = []
        self.row_length = 0
        self.col_length = 0
        self.trailheads_pos = set()
        self.endpoints_pos = set()
        self.displacement = {
            (-1, 0),  # UP
            (1, 0),  # DOWN
            (0, -1),  # LEFT
            (0, 1)  # RIGHT
        }

    def read_file(self, filename: str) -> list[list]:
        with open(filename, 'r') as f:
            for line in f:
                row_str = line.strip()
                row = [int(i) for i in row_str]
                self.grid.append(row)
            self.row_length = len(self.grid)
            self.col_length = len(self.grid[0])
            return self.grid

    def find_part_1_ans(self):
        # need 4 directions
        # we can have many trailheads
        # score of a trailhead (0) is the number of different endpoints (9) reachable

        # need a function to get all the trailheads and endpoints
        # need a function to stimulate path navigation from a trailhead and computing the score
        # need to add all the score of trailhead
        ans = 0
        self.retrieve_trailheads_and_endpoints_pos()
        for pos in self.trailheads_pos:
            ans += self.navigate_and_compute_score_for_trailhead(pos)
        return ans

    def retrieve_trailheads_and_endpoints_pos(self) -> None:
        for row in range(self.row_length):
            for col in range(self.col_length):
                if self.grid[row][col] == 0:
                    self.trailheads_pos.add((row, col))
                if self.grid[row][col] == 9:
                    self.endpoints_pos.add((row, col))

    def is_valid(self, position: tuple) -> bool:
        return 0 <= position[0] < self.row_length and 0 <= position[1] < self.col_length

    def is_endpoint(self, position: tuple) -> bool:
        return position in self.endpoints_pos

    def navigate_and_compute_score_for_trailhead(self, trailhead: tuple) -> int:
        is_visited = set()

        def dfs(position: tuple) -> int:
            if self.is_endpoint(position):
                return 1
            current_number = self.grid[position[0]][position[1]]
            total_score = 0
            for dr, dc in self.displacement:
                neighbour = (position[0] + dr, position[1] + dc)
                if self.is_valid(neighbour) and neighbour not in is_visited and self.grid[neighbour[0]][
                    neighbour[1]] == current_number + 1:
                    is_visited.add(neighbour)
                    total_score += dfs(neighbour)
            return total_score

        return dfs(trailhead)

    def find_part_2_ans(self):
        # need 4 directions
        # we can have many trailheads
        # score of a trailhead (0) is the number of different endpoints (9) reachable

        # need a function to get all the trailheads and endpoints
        # need a function to stimulate path navigation from a trailhead and computing the rating
        # need to add all the score of trailhead
        ans = 0
        self.retrieve_trailheads_and_endpoints_pos()
        for pos in self.trailheads_pos:
            ans += self.navigate_and_compute_rating_for_trailhead(pos)
        return ans

    def navigate_and_compute_rating_for_trailhead(self, trailhead: tuple) -> int:
        def dfs(position: tuple) -> int:
            if self.is_endpoint(position):
                return 1
            current_number = self.grid[position[0]][position[1]]
            total_score = 0
            for dr, dc in self.displacement:
                neighbour = (position[0] + dr, position[1] + dc)
                if self.is_valid(neighbour) and self.grid[neighbour[0]][neighbour[1]] == current_number + 1:
                    total_score += dfs(neighbour)
            return total_score

        return dfs(trailhead)


if __name__ == '__main__':
    p = HoofIt()
    p.read_file('input10.txt')
    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
