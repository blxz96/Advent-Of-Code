from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

import Utils


class RestroomRedoubt:
    @dataclass
    class Robot:
        # Note: coordinates is viewed from top, i.e. (0,0) means top left corner
        # Velocity is per iteration
        starting_x: int = 0
        starting_y: int = 0
        current_x: int = 0
        current_y: int = 0
        velocity_x: int = 0
        velocity_y: int = 0

    def __init__(self):
        self.robots = []
        self.map_width: int = 0
        self.map_height: int = 0
        # for part 2
        self.directions = (
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
            (1, -1),
            (-1, -1),
            (-1, 1),
            (1, 1)
        )

    def read_file(self, filename: str, map_width: int, map_height: int) -> None:
        self.robots = [] # So that we can reinitialise
        self.map_width = map_width
        self.map_height = map_height
        with open(filename, 'r') as f:
            for line in f:
                robot = RestroomRedoubt.Robot()
                raw_position, raw_velocity = line.strip().split()
                position, velocity = raw_position[2:].split(","), raw_velocity[2:].split(",")
                robot.starting_x = int(position[0])
                robot.starting_y = int(position[1])
                robot.current_x = int(position[0])
                robot.current_y = int(position[1])
                robot.velocity_x = int(velocity[0])
                robot.velocity_y = int(velocity[1])
                self.robots.append(robot)

    def find_part_1_ans(self, iterations: int) -> int:

        """
        Need to simulate robot position per iteration
        Need for teleportation cross boundary
        Need to split the map into 4 quadrants
        Need to exclude robots at the middle portions
        Need to calculate number of robots at each quadrant
        Need to multiply the quadrants
        :return: ans
        """
        for i in range(iterations):
            for robot in self.robots:
                self.navigate_robot_per_iter(robot)
        number_of_robots_in_each_quadrant = self.find_number_of_robots_in_each_quadrant()
        return reduce(lambda x, y: x * y, number_of_robots_in_each_quadrant.values())

    def navigate_robot_per_iter(self, robot: Robot) -> tuple[int, int]:
        robot.current_x = (robot.current_x + robot.velocity_x) % self.map_width
        robot.current_y = (robot.current_y + robot.velocity_y) % self.map_height
        return robot.current_x, robot.current_y

    def find_number_of_robots_in_each_quadrant(self) -> defaultdict:
        mid_width = self.map_width // 2
        mid_height = self.map_height // 2
        # range allowed in each quadrant in terms of width(x) from left and height(y) from top
        quad_top_left = (range(0, mid_width), range(0, mid_height))
        quad_top_right = (range(mid_width + 1, self.map_width), range(0, mid_height))
        quad_bottom_left = (range(0, mid_width), range(mid_height + 1, self.map_height))
        quad_bottom_right = (range(mid_width + 1, self.map_width), range(mid_height + 1, self.map_height))

        number_of_robots_in_each_quadrant = defaultdict(int)

        for robot in self.robots:
            if robot.current_x in quad_top_left[0] and robot.current_y in quad_top_left[1]:
                number_of_robots_in_each_quadrant['top_left'] += 1
            elif robot.current_x in quad_top_right[0] and robot.current_y in quad_top_right[1]:
                number_of_robots_in_each_quadrant['top_right'] += 1
            elif robot.current_x in quad_bottom_left[0] and robot.current_y in quad_bottom_left[1]:
                number_of_robots_in_each_quadrant['bottom_left'] += 1
            elif robot.current_x in quad_bottom_right[0] and robot.current_y in quad_bottom_right[1]:
                number_of_robots_in_each_quadrant['bottom_right'] += 1
        return number_of_robots_in_each_quadrant

    def find_part_2_ans(self, iterations) -> None:
        for i in range(iterations):
            grid = [['.'] * self.map_width for _ in range(self.map_height)]
            for robot in self.robots:
                x, y = self.navigate_robot_per_iter(robot)
                grid[y][x] = '#'
            largest_connected_component_area = self.find_area_of_largest_connected_component(grid)
            # This is just some heuristic
            if largest_connected_component_area >= 50:
                print("Iteration: {}, Largest Connected Area: {}".format(i + 1, largest_connected_component_area))
                for row in grid:
                    print(''.join(row))
                # This is actually an infinite loop that repeats - commented out the break to see
                break

    def find_area_of_largest_connected_component(self, grid: list[list[str]]):
        ans = []
        visited = set()
        num_rows = len(grid)
        num_cols = len(grid[0])
        curr_area = 0

        def is_valid(row, col):
            return 0 <= row < num_rows and 0 <= col < num_cols and grid[row][col] == '#'

        def dfs(row, col):
            nonlocal curr_area
            curr_area += 1
            visited.add((row, col))
            for dr, dc in self.directions:
                new_r = row + dr
                new_c = col + dc
                if (new_r, new_c) not in visited and is_valid(new_r, new_c):
                    dfs(new_r, new_c)

        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) not in visited and is_valid(row, col):
                    curr_area = 0
                    dfs(row, col)
                    ans.append(curr_area)

        return max(ans)


if __name__ == '__main__':
    p = RestroomRedoubt()
    p.read_file('small.txt',map_width=11, map_height=7)
    Utils.eval_and_time_function(p.find_part_1_ans,iterations=100)
    # Re-initialization - for actual input part 1
    p.read_file('input14.txt', map_width=101, map_height=103)
    Utils.eval_and_time_function(p.find_part_1_ans,iterations=100)
    # Re-initialization - for actual input part 2
    p.read_file('input14.txt', map_width=101, map_height=103)
    Utils.eval_and_time_function(p.find_part_2_ans, iterations=100000)
