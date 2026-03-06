import numpy as np


def compute_precision(tp, fp):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)


def compute_recall(tp, fn):
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)


def compute_f1(p, r):
    if p + r == 0:
        return 0
    return 2 * (p * r) / (p + r)