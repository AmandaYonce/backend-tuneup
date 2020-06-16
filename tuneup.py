#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Amanda Yonce"

import cProfile
import pstats
import io
from pstats import SortKey
import timeit
from functools import partial


def decorator_profile(orig_function):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def measure_perf(*args, **kwargs):
        print("called measure")
        prof = cProfile.Profile()
        prof.enable()
        orig_function(*args, **kwargs)
        prof.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(prof, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return ps
    return measure_perf


# @decorator_profile
def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


# @decorator_profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if movie in movies:
            duplicates.append(movie)
    return duplicates


def timeit_helper(func):
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(partial(func)).repeat(repeat=7, number=3)
    times = min(t)/1
    output = (f'Best time across 7 repeats of 5 runs per repeat: {times} sec')
    print(output)
    return output


@decorator_profile
def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


timeit_helper(main)


if __name__ == '__main__':
    main()
