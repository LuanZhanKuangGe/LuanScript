import itertools

def generate_sorting_combinations(children):
    all_combinations = list(itertools.permutations(children))
    valid_combinations = []

    for combination in all_combinations:
        valid = True
        for i in range(len(combination) - 1):
            if abs(combination[i] - combination[i+1]) == 1:
                valid = False
                break
        if valid:
            valid_combinations.append(combination)

    return valid_combinations

if __name__ == "__main__":
    children = list(range(1, 5))
    sorting_combinations = generate_sorting_combinations(children)

    print("Number of valid sorting combinations:", len(sorting_combinations))
    for combination in sorting_combinations:
        print(combination)