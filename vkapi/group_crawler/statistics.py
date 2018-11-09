from math import sqrt, log

def get_proba(x, N):
    p = x / N
    return p - 3 * sqrt(p - p * p) / sqrt(N)

def quality(N):
    return log(N + 1)

def trivial_points(x, N):
    return 1

def points(x, N):
    return (N - x) ** 2

def relation(intersection, size):
    return get_proba(intersection, size) * quality(size)
