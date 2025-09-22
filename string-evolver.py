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

def fitness_Matches_Exact(candidate, target) -> int:
    """
    Purpose: count exact character matches between a candidate and target
                - if lengths of the strings differ, compare up to the shorter length
    """
    exact_matches = 0
    length = min(len(candidate), len(target))
    for i in range(length):
        if candidate[i] == target[i]:
            exact_matches += 1
    return exact_matches


def fitness_Matches_Normalized(candidate, target) -> float:
    """
    Purpose: normalize exact matches for a string to an interval <0.0, 1.0>
                - 1.0 means 100% match on all target characters
    """
    if len(target) == 0:
        return 1.0 # this is an edge case (empty target as already matched)
    matches = fitness_Matches_Exact(candidate, target)
    return matches / len(target)

# --- POPULATION ---

def initial_population(population_size, length) -> list[str]:
    """
    Purpose: create a population_size number of random individuals
                - each is a randomly assembled string of chosen length
                - idea: provide starting genetic diversity so that GA has things to select and recombine
    """
    return [random_string(length) for i in range(population_size)]

def tournament_selection(population, fitnesses, n_indices) -> str:
    """
    Purpose:
                - randomly select n_indices of indices
                - from n_indices, select one with the highest fitness
    """
    indices = random.sample(range(len(population)), n_indices)
    best_indices = min(indices, key= lambda x: -fitnesses[x])
    return population[best_indices]

def single_point_crossover(parent1, parent2) -> tuple[str, str]:
    """
    Purpose: combine 2 parents to create 2 children by mixing segments of both parents
    """
    if len(parent1) <= 1: # Note: parents will hame the same length, so checking parent1 is enough
        return parent1, parent2
    index_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[ :index_point] + parent2[index_point: ]
    child2 = parent2[ :index_point] + parent1[index_point: ]
    return child1, child2

def uniform_crossover(parent1, parent2, probability= 0.5) -> tuple[str, str]:
    """
    Purpose: build 1 child by choosing each character independently from 1 of the 2 parents
    """
    child = ""
    for p1, p2 in zip(parent1, parent2):
        if random.random() < probability:
            child += p1
        else:
            child += p2
    return child

def mutate(candidate, mut_rat= 0.01) -> str:
    """
    Purpose: based on a mutation rate, either randomly mutate a character of an individual or keep it unchanged
    """
    new_chars = []
    for a in candidate:
        if random.random() < mut_rat:
            new_chars.append(random_char())
        else:
            new_chars.append(a)
    return "".join(new_chars)