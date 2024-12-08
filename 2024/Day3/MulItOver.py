import re
from collections import defaultdict
import Utils

class MulItOver:
    def __init__(self):
        self.corrupted_memory = ""
        self.multiplied_pattern = r'\bmul\(\d+,\d+\)'
        self.do_pattern = r'\bdo\(\)'
        self.dont_pattern = r'\bdon\'t\(\)'

    def read_file(self, filename):
        with open(filename, 'r') as f:
            self.corrupted_memory = f.read()

    def find_part_1_ans(self):
        ans = 0
        content = self.corrupted_memory
        # Note the pattern need to be stripped of "" at both sides
        matches = re.findall(self.multiplied_pattern, content)
        for match in matches:
            pairStr = match[4:-1]
            a, b = pairStr.split(',')
            ans += int(a) * int(b)
        return ans

    def find_part_2_ans(self):
        start_index_to_mul_mappings = self.find_matching_patterns_and_indices(self.multiplied_pattern)
        start_index_to_do_mappings = self.find_matching_patterns_and_indices(self.do_pattern)
        start_index_to_dont_mappings = self.find_matching_patterns_and_indices(self.dont_pattern)
        merged_sorted_dict = dict(sorted(
            {**start_index_to_mul_mappings, **start_index_to_do_mappings, **start_index_to_dont_mappings}.items()))
        instruction = merged_sorted_dict.values()

        enabled = True
        ans = 0
        for instruction in instruction:
            if instruction == "do()":
                enabled = True
            elif instruction == "don't()":
                enabled = False
            else:
                if enabled:
                    pairStr = instruction[4:-1]
                    a, b = pairStr.split(',')
                    ans += int(a) * int(b)
        return ans

    def find_matching_patterns_and_indices(self, pattern):
        content = self.corrupted_memory
        matches = re.finditer(pattern, content)
        start_index_to_match_mappings = defaultdict(str)
        for match in matches:
            start_index_to_match_mappings[match.start()] = match.group()
        return start_index_to_match_mappings


if __name__ == '__main__':
    p = MulItOver()
    p.read_file("input3.txt")
    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
