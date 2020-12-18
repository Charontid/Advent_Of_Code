#Advent of Code 2020: Day 17
#https://adventofcode.com
#Counting living cells in a 3d / 4d - version of "Conways Game of Life"

import sys
from itertools import product
from copy import copy
import time

def main():


    data = [
        ".#.",
        "..#",
        "###"
    ]
    data = read_input(data=data)
    """
    use the read_input(), to get input-data from sys.stdin
    """
    #data = read_input()

    start_time = time.time()
    print("ReflectionCube")
    cube = ReflectionConway_n_Cube(data=data, dim=4)
    cube.simulate(cycles=6)
    print(len(cube.alive))
    end_time = time.time()
    print(end_time - start_time)


    start_time = time.time()
    print("RegularCube")
    cube = Conway_n_Cube(data, dim=4)
    cube.simulate(cycles=6)
    print(len(cube.alive))
    end_time = time.time()
    print(end_time - start_time)


def read_input(data=None):
    if data is None:
        data = sys.stdin.readlines()
    alive = set()
    for i, line in enumerate(data):
        for j, val in enumerate(line.strip()):
            if val == '#':
                alive.add((j,i))
    return alive


class Conway_n_Cube:
    """
    small class to keep track of living cells in Conways Game of life in
    an n cube.
    Could be further optimized by using the xy-Hyperplane
    as a reflection plane, however
    """
    def __init__(self, data, dim=3):
        self.dim = dim
        self.alive = {
            tuple([*p]+[0 for _ in range(self.dim-2)]) for p in data
        }


    def scan_neighbours(self, pos):
        count = 0
        s = self.get_neighbours(pos)
        s.remove(pos)
        return len(s.intersection(self.alive))


    def get_neighbours(self, pos):
        iterables = [[x-1, x, x+1] for x in pos]
        return set(product(*iterables))


    def simulate(self, cycles=6):
        for _ in range(cycles):
            checked = set()
            turn_active = set()
            turn_inactive = set()
            for p in self.alive:
                s = self.get_neighbours(p)
                #s = {pos for pos in s if pos not in checked}
                s = s.difference(checked)
                for pos in s:
                    count = self.scan_neighbours(pos)
                    if count not in {2,3} and pos in self.alive:
                        turn_inactive.add(pos)
                    if count == 3 and pos not in self.alive:
                        turn_active.add(pos)
                    checked.add(pos)
            self.alive = self.alive.difference(turn_inactive)
            self.alive = self.alive.union(turn_active)


class ReflectionConway_n_Cube:
    """
    Kinda depressing: Seems like generating the reflections is slightly slower then the brute force :()
    """
    def __init__(self, data, dim=3):
        self.dim = dim
        self.alive = {
            tuple([*p]+[0 for _ in range(self.dim-2)]) for p in data
        }
        self._reflection_patterns = set(product([1,-1], repeat = self.dim-2))


    def scan_neighbours(self, pos):
        count = 0
        s = self.get_neighbours(pos)
        s.remove(pos)
        return len(s.intersection(self.alive))


    def get_neighbours(self, pos):
        iterables = [[x-1, x, x+1] for x in pos]
        return set(product(*iterables))


    def simulate(self, cycles=6):
        for _ in range(cycles):
            checked = set()
            turn_active = set()
            turn_inactive = set()
            to_check = copy(self.alive)
            for p in to_check:
                s = self.get_neighbours(p)
                s = s.difference(checked)
                s = self.reflections(s)
                to_check = to_check.difference(s)
                #s = s.difference(checked) # most likely not necessary :)
                for pos in s:
                    count = self.scan_neighbours(pos)
                    if count not in {2,3} and pos in self.alive:
                        turn_inactive.add(pos)
                    if count == 3 and pos not in self.alive:
                        turn_active.add(pos)
                    checked.add(pos)
            self.alive = self.alive.difference(turn_inactive)
            self.alive = self.alive.union(turn_active)


    def reflections(self, s):
        refl = set()
        for pos in s:
            x,y, *vals = pos
            for r in self._reflection_patterns:
                p = [x,y]
                p.extend([a*b for a,b in zip(vals, r)])
                refl.add(tuple(p))
        return refl



if __name__ == '__main__':
    main()
