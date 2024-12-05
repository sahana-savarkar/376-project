import re
import pandas as pd
from collections import defaultdict
import random

data = pd.read_csv('dessert_recipes.csv')

recipe_list = data['recipe_name'].head(1000).tolist()
recipe_list = [line.split() for line in recipe_list]

ingredient_list = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split(",") for line in ingredient_list]

markov_chain = defaultdict(lambda: defaultdict(int))
markov_chain_recipe_name = defaultdict(lambda: defaultdict(int))

for tokens in recipe_list:
    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]
        markov_chain_recipe_name[current_word][next_word] += 1

for tokens in ingredient_list:
    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]
        markov_chain[current_word][next_word] += 1

for current_word, transitions in markov_chain_recipe_name.items():
    total_transitions = sum(transitions.values())
    for next_word in transitions:
        transitions[next_word] /= total_transitions


for current_word, transitions in markov_chain.items():
    total_transitions = sum(transitions.values())
    for next_word in transitions:
        transitions[next_word] /= total_transitions

def generate_ingredient_list(chain, start_word, length):
    if start_word not in chain:
        raise ValueError(f"Start word '{start_word}' not found in the markov chain.")
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




recipe_start_word = "Apple"
ingredient_start_word = "8 small Granny Smith apples"
ingredient2_start_word =  "1 cup sliced fresh peaches"



recipe_name = generate_ingredient_list(markov_chain_recipe_name, start_word=recipe_start_word, length=80)

ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
generated_list = generate_ingredient_list(markov_chain, start_word=ingredient_start_word, length=20)
generated_list2 = generate_ingredient_list(markov_chain, start_word=ingredient2_start_word, length=20)

ingredients_list = re.findall(ingredient_pattern, generated_list)
ingredients_list2 = re.findall(ingredient_pattern, generated_list2)



print('\nRECIPE NAME: ')
print(recipe_name)


print("INGREDIENT LIST: \n")
for ingredient in ingredients_list:
    print(ingredient.strip())
for ingredient in ingredients_list2:
    print(ingredient.strip())

