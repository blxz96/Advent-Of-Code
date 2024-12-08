import Utils


class GuardGallivant:
    def __init__(self):
        self.maze = []
        self.visited = set()  # position (for part 1)
        self.obstacles = set()
        self.visited_with_state = set()  # position, orientation (for part 2_
        self.num_rows = 0
        self.num_cols = 0
        self.starting_position = (-1, -1)
        self.starting_orientation = (-1, 0)
        self.current_to_next_orientation = {
            (-1, 0): (0, 1),  # UP -> RIGHT
            (0, 1): (1, 0),  # RIGHT -> DOWN
            (1, 0): (0, -1),  # DOWN -> LEFT
            (0, -1): (-1, 0)  # LEFT -> UP
        }

    def read_file(self, filename) -> None:
        with open(filename, 'r') as f:
            for line in f:
                row = list(line.strip())
                self.maze.append(row)

    def initialize_maze_and_starting_position(self) -> None:
        self.num_rows, self.num_cols = len(self.maze), len(self.maze[0])
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.maze[row][col] == '#':
                    self.obstacles.add((row, col))
                elif self.maze[row][col] == '^':
                    self.starting_position = (row, col)

    def find_part_1_ans(self) -> int:
        self.navigate_maze_iter(self.starting_position, self.starting_orientation)
        return len(self.visited)

    def navigate_maze_iter(self, position, orientation) -> set:
        while not self.has_exited_maze(position):
            self.visited.add(position)
            while (not self.has_exited_maze((position[0] + orientation[0], position[1] + orientation[1])) and
                   self.maze[position[0] + orientation[0]][position[1] + orientation[1]] == '#'):
                orientation = self.current_to_next_orientation[orientation]
            position = (position[0] + orientation[0], position[1] + orientation[1])
        return self.visited

    # Note: This works on small input, but for large input, it will get too deep into recursion and throw error
    def navigate_maze_recursive(self, position, orientation) -> None:
        self.visited.add(position)
        if self.has_exited_maze((position[0] + orientation[0], position[1] + orientation[1])):
            return
        if self.maze[position[0] + orientation[0]][position[1] + orientation[1]] == '#':
            orientation = self.current_to_next_orientation[orientation]
        new_position = (position[0] + orientation[0], position[1] + orientation[1])
        self.navigate_maze_recursive(new_position, orientation)

    def has_exited_maze(self, position) -> bool:
        if position[0] < 0 or position[0] >= self.num_rows or position[1] < 0 or position[1] >= self.num_cols:
            return True
        return False

    def find_part_2_ans(self) -> int:
        """
        - Condition that cause infinite loop : 
            1. Guard has reached a position that he had already visited
            2. Guard is facing the same orientation at the last time he visited the position
        - Brute-force solution is try putting obstacles at every grid every time - this is inefficient
        - A more optimal approach is shrinking the problem space 
            1. We should only place obstacles at position we know he went to (from part 1) - starting position(constraint from puzzle)
        - Implement a state where state = (position, orientation)
        - If state has been visited, it will result in an infinite loop
        """
        return self.navigate_maze_iter_infinite_loop(self.starting_position, self.starting_orientation)

    def navigate_maze_iter_infinite_loop(self, starting_position, starting_orientation) -> int:
        possible_obstacle_position = self.navigate_maze_iter(starting_position, starting_orientation) - {
            self.starting_position}
        ans = 0
        position = starting_position
        orientation = starting_orientation
        for obstacle_position in possible_obstacle_position:
            # Set up problem space
            self.maze[obstacle_position[0]][obstacle_position[1]] = '#'
            while not self.has_exited_maze(position):
                # Infinite loop causing condition, exit
                if (position, orientation) in self.visited_with_state:
                    ans += 1
                    break
                self.visited_with_state.add((position, orientation))
                while (not self.has_exited_maze((position[0] + orientation[0], position[1] + orientation[1])) and
                       self.maze[position[0] + orientation[0]][position[1] + orientation[1]] == '#'):
                    orientation = self.current_to_next_orientation[orientation]
                    self.visited_with_state.add((position, orientation))
                position = (position[0] + orientation[0], position[1] + orientation[1])

            # Reset for next problem space
            self.maze[obstacle_position[0]][obstacle_position[1]] = '.'
            self.visited_with_state = set()
            position = starting_position
            orientation = starting_orientation
        return ans


if __name__ == '__main__':
    p = GuardGallivant()
    p.read_file('input6.txt')
    p.initialize_maze_and_starting_position()

    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
