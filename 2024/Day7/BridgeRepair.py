from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product

import Utils


class BridgeRepair:
    def __init__(self):
        self.calibration_list = list()
        self.valid_calibration_map = defaultdict(list)

    def read_file(self, filename) -> None:
        with open(filename, 'r') as f:
            for line in f:
                row = line.strip().split(':')
                lhs, rhs = row[0], row[1]
                final_rhs = [int(i) for i in rhs.split()]
                # There are repeated keys, so don't use map
                self.calibration_list.append((int(lhs), final_rhs))

    def find_ans_recursive(self):
        ans = 0
        for lhs, rhs in self.calibration_list:
            ans += self.check_valid_calibration_recursive(lhs, rhs)
        return ans

    def find_ans_recursive_multi_threading(self):
        ans = 0
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.check_valid_calibration_recursive, lhs, rhs) for lhs, rhs in
                       self.calibration_list]
            for future in as_completed(futures):
                if future.result():
                    ans += future.result()
        return ans

    @staticmethod
    def check_valid_calibration_recursive(lhs, rhs) -> int:
        max_operators_allowed = len(rhs) - 1

        def recurse(result, operators_used):
            # Base case 1: When we have reached max_operators_allowed and results match LHS
            # Base case 2: When we have reached max_operators_allowed and results do not match LHS
            # Base case 3: When we have not yet reached max_operators_allowed but result > LHS
            if operators_used >= max_operators_allowed:
                return result == lhs
            if result > lhs:  # This step is considered as pruning
                return False
            operators_used += 1
            return (recurse(result * rhs[operators_used], operators_used)
                    or recurse(result + rhs[operators_used], operators_used)
                    or recurse(int(str(result) + str(rhs[operators_used])), operators_used)  # part 2 only
                    )

        return lhs if recurse(rhs[0], 0) else 0

    def find_ans_iter(self) -> int:
        ans = 0
        # Check for each input
        for lhs, rhs in self.calibration_list:
            ans += self.check_valid_calibration_iter(lhs, rhs)
        return ans

    def find_ans_iter_multi_threading(self):
        ans = 0
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.check_valid_calibration_iter, lhs, rhs) for lhs, rhs in
                       self.calibration_list]
            for future in as_completed(futures):
                if future.result():
                    ans += future.result()
        return ans

    def check_valid_calibration_iter(self, lhs, rhs):
        ans = 0
        # itertools.product can be used to generate all possible combination of '+', '*', '||'
        # for a given number of gaps between numbers in rhs
        # operators_combinations = product(['+', '*'], repeat=len(rhs) - 1)

        # Brute-force
        # 3^n combinations - Combinatorial explosion is expensive
        # itertools.product incur expensive overhead
        operators_combinations = product(['+', '*', '||'], repeat=len(rhs) - 1)
        for ops in operators_combinations:
            if self.evaluate_expression(lhs, rhs, ops) == lhs:
                ans += lhs
                break
        return ans

    @staticmethod
    def evaluate_expression(lhs, rhs, ops):
        result = rhs[0]
        for i in range(len(ops)):
            if ops[i] == '+':
                result += rhs[i + 1]
            elif ops[i] == '*':
                result *= rhs[i + 1]
            elif ops[i] == '||':
                result = int(str(result) + str(rhs[i + 1]))
            # Late pruning since combination is still generated by itertools.product
            if result > lhs:
                break
        return result

    def find_ans_iter_optimized(self) -> int:
        ans = 0
        for lhs, rhs in self.calibration_list:
            if self.check_valid_calibration_optimized(lhs, rhs):
                ans += lhs
        return ans

    def find_ans_iter_optimized_multi_threading(self):
        ans = 0
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.check_valid_calibration_optimized, lhs, rhs) for lhs, rhs in
                       self.calibration_list]
            for future in as_completed(futures):
                if future.result():
                    ans += future.result()
        return ans
    @staticmethod
    def check_valid_calibration_optimized(lhs, rhs) -> bool:
        # Use a stack to simulate recursion-like behavior
        stack = [(rhs[0], 0)]  # (current result, index of the next operator)
        while stack:
            current_result, idx = stack.pop()

            # If we have used all operators and match lhs, it's valid
            if idx == len(rhs) - 1:
                if current_result == lhs:
                    return True
                continue

            # Try all operators dynamically and prune
            next_val = rhs[idx + 1]
            if current_result + next_val <= lhs:  # Prune addition
                stack.append((current_result + next_val, idx + 1))
            if current_result * next_val <= lhs:  # Prune multiplication
                stack.append((current_result * next_val, idx + 1))
            concatenated = int(str(current_result) + str(next_val))
            if concatenated <= lhs:  # Prune concatenation
                stack.append((concatenated, idx + 1))

        return False


if __name__ == '__main__':
    p = BridgeRepair()
    p.read_file('input7.txt')
    Utils.eval_and_time_function(p.find_ans_recursive)
    Utils.eval_and_time_function(p.find_ans_recursive_multi_threading)
    Utils.eval_and_time_function(p.find_ans_iter)
    Utils.eval_and_time_function(p.find_ans_iter_multi_threading)
    Utils.eval_and_time_function(p.find_ans_iter_optimized)
    Utils.eval_and_time_function(p.find_ans_iter_optimized_multi_threading)