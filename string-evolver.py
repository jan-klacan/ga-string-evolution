import sys
import string
import math
import random
import argparse
import matplotlib.pyplot as plt

# --- ENCODING ---
alphabet = " " + string.ascii_letters + string.digits + ".,?!"

def random_char():
    return random.choice(alphabet)

def random_string(length):
    return "".join(random.choices(alphabet, k= length))

# --- FITNESS ---

def fitness_Matches_Exact(candidate, target):
    """
    Purpose: count exact character matches between a candidate and target
                - if lengths of the strings differ, compare up to the shorter length
    Returns: integer
    """
    exact_matches = 0
    length = min(len(candidate), len(target))
    for i in range(length):
        if candidate[i] == target[i]:
            exact_matches += 1
    return exact_matches


def fitness_Matches_Normalized(candidate, target):
    """
    Purpose: normalize exact matches for a string to an interval <0.0, 1.0>
                - 1.0 means 100% match on all target characters
    Returns: float between 0.0 and 1.0
    """
    if len(target) == 0:
        return 1.0 # this is an edge case (empty target as already matched)
    matches = fitness_Matches_Exact(candidate, target)
    return matches / len(target)