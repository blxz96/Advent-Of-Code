from collections import deque, Counter

import Utils


class PlutonianPebbles:
    def __init__(self):
        pass
    def read_file(self, filename):
        pebbles = []
        with open(filename, 'r') as f:
            file_str_split = f.read().strip().split()
            pebbles.extend(file_str_split)
        return pebbles

    def find_part_1_answer(self, pebbles: list, number_of_blink: int) -> int:
        """
        Rules for stone transformation:
        0 -> 1
        Even number of digit -> split to 2 stones (left stone is first half, right stone is second half)
        Others -> multiplied by 2024

        Algorithm:
        Have a function which use a queue to capture the transform stones at each iteration
        After x iteration, return the length of the queue
        """
        pebbles_queue = deque(pebbles)
        transformed_pebbles = self.transform_stones(pebbles_queue, number_of_blink)
        return len(transformed_pebbles)

    def transform_stones(self, pebbles: deque, number_of_blinks: int) -> deque:
        for i in range(number_of_blinks):
            number_of_pebbles = len(pebbles)
            for _ in range(number_of_pebbles):
                pebble = pebbles.popleft()
                if pebble == '0':
                    pebbles.append('1')
                elif len(pebble) % 2 == 0:
                    left_pebble = str(int(pebble[:len(pebble) // 2]))
                    right_pebble = str(int(pebble[len(pebble) // 2:]))
                    pebbles.append(left_pebble)
                    pebbles.append(right_pebble)
                else:
                    new_pebble = str(int(pebble) * 2024)
                    pebbles.append(new_pebble)
        return pebbles

    def find_part_2_answer(self, pebbles: list, number_of_blinks: int) -> int:
        """
        Optimized algorithm for 75 iterations.
        Tracks the count of different types of pebbles instead of managing all pebbles explicitly.
        """
        pebble_counts = Counter(pebbles)

        for _ in range(number_of_blinks):
            new_counts = Counter()
            for pebble, count in pebble_counts.items():
                if pebble == '0':
                    new_counts['1'] += count
                elif len(pebble) % 2 == 0:
                    left_pebble = str(int(pebble[:len(pebble) // 2]))
                    right_pebble = str(int(pebble[len(pebble) // 2:]))
                    new_counts[left_pebble] += count
                    new_counts[right_pebble] += count
                else:
                    new_pebble = str(int(pebble) * 2024)
                    new_counts[new_pebble] += count
            pebble_counts = new_counts

        return sum(pebble_counts.values())


if __name__ == '__main__':
    pl = PlutonianPebbles()
    original_pebbles = pl.read_file('input11.txt')
    # Note: Don't do it this for part 2, this exponential time
    Utils.eval_and_time_function(pl.find_part_1_answer, original_pebbles, 25)
    Utils.eval_and_time_function(pl.find_part_2_answer, original_pebbles, 75)
