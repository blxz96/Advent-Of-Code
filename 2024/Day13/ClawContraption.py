from dataclasses import dataclass
from sympy import symbols, Eq, solve
import Utils


class ClawContraption:
    @dataclass
    class ClawMachine:
        displacement_ax: int = 0
        displacement_ay: int = 0
        displacement_bx: int = 0
        displacement_by: int = 0
        price_x: int = 0
        price_y: int = 0

    def __init__(self):
        self.machines = list()

    def read_file(self, filename):
        with open(filename, 'r') as f:
            machine = ClawContraption.ClawMachine()
            for line in f:
                line_strip = line.strip()
                if len(line_strip) == 0:
                    machine = ClawContraption.ClawMachine()
                    continue
                key, values = line_strip.split(':')
                x, y = values.strip().split(',')
                x, y = x[2:], y[3:]
                if key == 'Button A':
                    machine.displacement_ax = int(x)
                    machine.displacement_ay = int(y)
                elif key == 'Button B':
                    machine.displacement_bx = int(x)
                    machine.displacement_by = int(y)
                elif key == 'Prize':
                    machine.price_x = int(x)
                    machine.price_y = int(y)
                    self.machines.append(machine)
        return self.machines

    def read_file_part_2(self, filename):
        with open(filename, 'r') as f:
            machine = ClawContraption.ClawMachine()
            for line in f:
                line_strip = line.strip()
                if len(line_strip) == 0:
                    machine = ClawContraption.ClawMachine()
                    continue
                key, values = line_strip.split(':')
                x, y = values.strip().split(',')
                x, y = x[2:], y[3:]
                if key == 'Button A':
                    machine.displacement_ax = int(x)
                    machine.displacement_ay = int(y)
                elif key == 'Button B':
                    machine.displacement_bx = int(x)
                    machine.displacement_by = int(y)
                elif key == 'Prize':
                    machine.price_x = int(x) + 10000000000000
                    machine.price_y = int(y) + 10000000000000
                    self.machines.append(machine)
        return self.machines

    def find_ans(self):
        ans = 0
        for machine in self.machines:
            a, b = ClawContraption.solve_simultaneous_equations(machine)
            if a.is_Integer and b.is_Integer:
                ans += a * 3 + b * 1
        return ans

    @classmethod
    def solve_simultaneous_equations(cls, machine):
        a, b = symbols('a, b')
        eqn1 = Eq(machine.displacement_ax * a + machine.displacement_bx * b, machine.price_x)
        eqn2 = Eq(machine.displacement_ay * a + machine.displacement_by * b, machine.price_y)
        solution = solve((eqn1, eqn2), (a, b))
        return solution[a], solution[b]


if __name__ == '__main__':
    p = ClawContraption()
    p.read_file('input13.txt')
    Utils.eval_and_time_function(p.find_ans)
    # reset machines
    p.machines = []
    p.read_file_part_2('input13.txt')
    Utils.eval_and_time_function(p.find_ans)
