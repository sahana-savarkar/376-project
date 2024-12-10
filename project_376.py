import re
import pandas as pd
from collections import defaultdict
import random

data = pd.read_csv('pie_recipes.csv')
data = data.dropna(subset=['recipe_name', 'ingredients', 'directions'])

recipe_name_list = data['recipe_name'].head(1000).tolist()
recipe_name_list = [line.split() for line in recipe_name_list]

ingredient_list = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split(",") for line in ingredient_list]

directions_list = data['directions'].head(1000).tolist()
directions_list = [line.split(" ") for line in directions_list]



def markov_chain_generator(data_list):
    markov_chain = defaultdict(lambda: defaultdict(int))
    for tokens in data_list:
        for i in range(len(tokens) - 1):
            current_word = tokens[i]
            next_word = tokens[i + 1]
            markov_chain[current_word][next_word] += 1
    for current_word, transitions in markov_chain.items():
        total_transitions = sum(transitions.values())
        for next_word in transitions:
            transitions[next_word] /= total_transitions
    return markov_chain

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


markov_recipe_name = markov_chain_generator(recipe_name_list)
markov_ingredient_list = markov_chain_generator(ingredient_list)
markov_directions = markov_chain_generator(directions_list)

recipe_start_word = "Apple"
ingredient_start_word = "½ cup unsalted butter"
ingredient2_start_word =  "6 cups thinly sliced apples"
directions1_start_word = "Peel"
directions2_start_word = "Mix"
directions3_start_word = "Beat"



recipe_name_result = generate_ingredient_list(markov_recipe_name, start_word=recipe_start_word, length=80)

ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
ingredients_result = generate_ingredient_list(markov_ingredient_list, start_word=ingredient_start_word, length=20)
ingredients_result2 = generate_ingredient_list(markov_ingredient_list, start_word=ingredient2_start_word, length=20)

ingredients_result = re.findall(ingredient_pattern, ingredients_result)
ingredients_result2 = re.findall(ingredient_pattern, ingredients_result2)

directions_result1 = generate_ingredient_list(markov_directions, start_word=directions1_start_word, length=100)
directions_result2 = generate_ingredient_list(markov_directions, start_word=directions2_start_word, length=100)
directions_result3 = generate_ingredient_list(markov_directions, start_word=directions3_start_word, length=100)


def add_bullet_points(paragraph, bullet='•'):
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    bullet_points = [f"{bullet} {sentence.strip()}" for sentence in sentences if sentence]
    return '\n'.join(bullet_points)

directions_bulleted1 = add_bullet_points(directions_result1)
directions_bulleted2 = add_bullet_points(directions_result2)
directions_bulleted3 = add_bullet_points(directions_result3)


print('\nRECIPE NAME: ')
print(recipe_name_result)


print("\nINGREDIENT LIST: \n")
for ingredient in ingredients_result:
    print("-", ingredient.strip())
for ingredient in ingredients_result2:
    print("-", ingredient.strip())


print("\nDIRECTIONS: \n")
print(directions_bulleted1)
print(directions_bulleted2)
print(directions_bulleted3)
