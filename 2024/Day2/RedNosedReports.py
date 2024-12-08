import Utils

def is_within_bound(report):
    for i in range(1, len(report)):
        if abs(report[i] - report[i - 1]) < 1 or abs(report[i] - report[i - 1]) > 3:
            return False
    return True


def is_monotonic_increasing_or_decreasing(report):
    sorted_parts_asc = sorted(report)
    sorted_parts_desc = sorted(report, reverse=True)
    return report == sorted_parts_asc or report == sorted_parts_desc


class RedNosedReports:
    def __init__(self):
        # reports contain levels
        self.reports = []

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = [int(part) for part in line.strip().split()]
                self.reports.append(parts)

    def find_part1_ans(self):
        ans = 0
        for report in self.reports:
            if is_monotonic_increasing_or_decreasing(report) and is_within_bound(report):
                ans += 1
        return ans

    def find_part2_ans(self):
        ans = 0
        for report in self.reports:
            for index, level in enumerate(report):
                report.pop(index)
                if is_monotonic_increasing_or_decreasing(report) and is_within_bound(report):
                    ans += 1
                    break
                report.insert(index, level)
        return ans


if __name__ == '__main__':
    p = RedNosedReports()
    p.read_file('input2.txt')
    Utils.eval_and_time_function(p.find_part1_ans)
    Utils.eval_and_time_function(p.find_part2_ans)
