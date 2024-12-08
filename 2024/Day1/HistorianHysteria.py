from collections import Counter
import Utils

class HistorianHysteria:

    def __init__(self):
        self.column1 = []
        self.column2 = []

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                self.column1.append(int(parts[0]))
                self.column2.append(int(parts[1]))

    def find_part_1_ans(self):
        ans = 0
        sorted_column1 = sorted(self.column1)
        sorted_column2 = sorted(self.column2)
        for i in range(len(sorted_column1)):
            ans += abs(sorted_column1[i] - sorted_column2[i])
        return ans

    def find_part_2_ans(self):
        ans = 0
        column2_freq = Counter(self.column2)
        for element in self.column1:
            ans += element * column2_freq[element]
        return ans


if __name__ == '__main__':
    p = HistorianHysteria()
    p.read_file('input1.txt')

    # Note that parameter is callable function so don't put bracket
    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
