import re
import pandas as pd
from collections import defaultdict
import random

corpus_string = ""
corpus = []
dct = {}
i = 0

data = pd.read_csv('recipes.csv')
recipe_list = data['recipe_name'].head(100).tolist()
ingredient_list = data['ingredients'].head(100).tolist()
ingredient_list = [line.split() for line in ingredient_list]


markov_chain = defaultdict(lambda: defaultdict(int))

for tokens in ingredient_list:
    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]
        markov_chain[current_word][next_word] += 1

for current_word, transitions in markov_chain.items():
    total_transitions = sum(transitions.values())
    for next_word in transitions:
        transitions[next_word] /= total_transitions


def generate_ingredient_list(chain, start_word, length=15):
    word = start_word
    result = [word]
    for _ in range(length - 1):
        if word not in chain:
            break
        next_word = random.choices(
            list(chain[word].keys()),
            weights=list(chain[word].values())
        )[0]
        result.append(next_word)
        word = next_word
    return ' '.join(result)

print("INGREDIENT LIST: ")
for i in range(6):
    start_word = "1"
    generated_list = generate_ingredient_list(markov_chain, start_word=start_word)
    print(generated_list)

