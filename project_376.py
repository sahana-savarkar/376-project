import re
import pandas as pd
from collections import defaultdict
import random

data = pd.read_csv('pie_recipes.csv')
data = data.dropna(subset=['recipe_name', 'ingredients', 'directions'])

recipe_name_list = data['recipe_name'].head(1000).tolist()
recipe_name_list = [line.split() for line in recipe_name_list]

ingredient_list = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split(" ") for line in ingredient_list]

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
        start_word = random.choice(list(chain.keys()))
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

recipe_start_word = random.choice(list(markov_recipe_name.keys()))
recipe_name_result = generate_ingredient_list(markov_recipe_name, start_word=recipe_start_word, length=80)

print('\nRECIPE NAME: ')
print(recipe_name_result)

ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
invalid_ingredient_list = ['1', '1/4', '10', '12', '18', '2', '20', '3', '4', '5', '6', '7', '8', '9', 'peeled', 'sliced', 'cored', 'softened', 'halved', 'crushed', 'shredded', 'chopped', 'grated', 'lightly', 'firm', 'thinly', 'beaten', 'drained', 'packed', 'desired', 'prepared', 'freshly', 'quartered', 'needed', 'ripe', 'frozen', 'baked', 'split', 'melted', 'salted', 'unbaked', 'warmed', 'mixed', 'ground', 'inch', 'pieces', 'tablespoon', 'tablespoons', 'cup', 'cups', 'ounce', 'cold', 'a', 'd', "with", 'dried']

def ingredient_end(ingredient):
    last_word = ingredient.strip().split()[-1]
    return last_word 

def truncate_invalid_ingredients(ingredients):
    valid_ingredients = []
    for ingredient in ingredients:
        if ingredient_end(ingredient) not in invalid_ingredient_list:
            valid_ingredients.append(ingredient)
    return valid_ingredients

for word in recipe_name_result.lower().split():
    ingredients = generate_ingredient_list(markov_ingredient_list, start_word=word, length=20)
    ingredients = re.findall(ingredient_pattern, ingredients)
    ingredients = truncate_invalid_ingredients(ingredients)
    for item in ingredients:
        print("-", item.strip())

def add_bullet_points(paragraph, bullet='•'):
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    bullet_points = [f"{bullet} {sentence.strip()}" for sentence in sentences if sentence]
    return '\n'.join(bullet_points)


print("\nDIRECTIONS: \n")

directions1_start_word = 'Mix'
directions2_start_word = 'Bake'
directions3_start_word = 'Serve'

directions_result1 = generate_ingredient_list(markov_directions, start_word=directions1_start_word, length=70)
directions_result2 = generate_ingredient_list(markov_directions, start_word=directions2_start_word, length=70)
directions_result3 = generate_ingredient_list(markov_directions, start_word=directions3_start_word, length=70)


directions_bulleted1 = add_bullet_points(directions_result1)
directions_bulleted2 = add_bullet_points(directions_result2)
directions_bulleted3 = add_bullet_points(directions_result3)


print(directions_bulleted1)
print(directions_bulleted2)
print(directions_bulleted3)


