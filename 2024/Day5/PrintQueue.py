from collections import defaultdict
import Utils


class PrintQueue:
    def __init__(self):
        self.rules = []
        self.updates = []
        self.after_to_before = defaultdict(list)
        self.correct_indices = []

    def read_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            read_rules = True
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    read_rules = False
                    continue
                if read_rules:
                    self.rules.append(line)
                else:
                    self.updates.append([int(i) for i in line.split(',')])

    def build_mappings(self) -> None:
        for rule in self.rules:
            pairs = rule.split('|')
            before, after = int(pairs[0]), int(pairs[1])
            self.after_to_before[after].append(before)

    def find_part_1_ans_and_correct_indices(self) -> int:
        ans = 0
        for i, update in enumerate(self.updates):
            valid = True
            for j, current in enumerate(update):
                elements_after_current = set(update[j + 1:])
                elements_before_current_based_on_rules = set(self.after_to_before[current])
                intersection = elements_after_current.intersection(elements_before_current_based_on_rules)
                if len(intersection) > 0:
                    valid = False
                    break
            if valid:
                mid_value_idx = len(update) // 2
                ans += update[mid_value_idx]
                self.correct_indices.append(i)
        return ans

    def find_part_2_ans(self) -> int:
        ans = 0
        incorrect_indices = set(range(0, len(self.updates))) - set(self.correct_indices)
        for i in incorrect_indices:
            incorrect_update = self.updates[i]
            corrected_update = self.sort_based_on_rules(incorrect_update)
            mid_value_idx = len(incorrect_update) // 2
            ans += corrected_update[mid_value_idx]
        return ans

    def sort_based_on_rules(self, incorrect_update: list[int]) -> [int]:
        ans = len(incorrect_update) * [-1]
        for element in incorrect_update:
            complement = set(incorrect_update) - {element}
            intersection = complement.intersection(set(self.after_to_before[element]))
            number_of_elements_before = len(intersection)
            ans[number_of_elements_before] = element
        return ans


if __name__ == '__main__':
    p = PrintQueue()
    p.read_file('input5.txt')
    p.build_mappings()

    Utils.eval_and_time_function(p.find_part_1_ans_and_correct_indices)
    Utils.eval_and_time_function(p.find_part_2_ans)
