import re
import pandas as pd
from collections import defaultdict
import random

data = pd.read_csv('pie_recipes.csv')
data = data.dropna(subset=['recipe_name', 'ingredients', 'directions'])

recipe_name_list = data['recipe_name'].head(1000).tolist()
recipe_name_list = [line.split() for line in recipe_name_list]

ingredients_before = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split(" ") for line in ingredients_before]
ingredient_starter = [line.split(",") for line in ingredients_before]

directions_list = data['directions'].head(1000).tolist()
directions_list = [line.split(" ") for line in directions_list]

print(directions_list)

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
markov_ingredient_starter = markov_chain_generator(ingredient_starter)
markov_directions = markov_chain_generator(directions_list)

recipe_start_word = random.choice(list(markov_recipe_name.keys()))
recipe_name_result = generate_ingredient_list(markov_recipe_name, start_word=recipe_start_word, length=80)


print('\nRECIPE NAME: ')
print(recipe_name_result)

ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
invalid_ingredient_list = ['1', '1/4', '10', '12', '18', '2', '20', '3', '4', '5', '6', '7', '8', '9',
                            'peeled', 'sliced', 'cored', 'softened', 'halved', 'crushed', 'shredded',
                            'chopped', 'grated', 'lightly', 'firm', 'thinly', 'beaten', 'drained',
                            'packed', 'desired', 'prepared', 'freshly', 'quartered', 'needed', 'ripe',
                            'frozen', 'baked', 'split', 'melted', 'salted', 'unbaked', 'warmed', 'mixed',
                            'ground', 'inch', 'pieces', 'tablespoon', 'tablespoons', 'cup', 'cups', 'ounce',
                            'ounces', 'cold', 'a', 'd', "with", 'dried', 'pinch', 'fresh']

def ingredient_end(ingredient):
    last_word = ingredient.strip().split()[-1]
    return last_word 

def truncate_invalid_ingredients(ingredients):
    valid_ingredients = []
    seen_ingredients = set()
    for ingredient in ingredients:
        if ingredient_end(ingredient) not in invalid_ingredient_list and ingredient not in seen_ingredients:
            valid_ingredients.append(ingredient)
            seen_ingredients.add(ingredient)
    return valid_ingredients
     

for word in recipe_name_result.lower().split():
    matching_key = next((key for key, ingredients in markov_ingredient_starter.items() if any(word in ingredient for ingredient in ingredients)), None)
    print(matching_key)
    ingredients_starter = generate_ingredient_list(markov_ingredient_list, start_word=word, length=10)
    ingredients = generate_ingredient_list(markov_ingredient_list, start_word=word, length=20)
    ingredients = re.findall(ingredient_pattern, ingredients)
    ingredients = truncate_invalid_ingredients(ingredients)
    for item in ingredients:
        print("-", item.strip())


awkward_endings = {"and", "for", "or", "into", "in", "a", "an", "before", "after", "with", "without", "not", "so", "if", "when", "while"}

def add_bullet_points(paragraph, bullet='•'):
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    valid_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) <= 2:
            continue
        
        last_word = sentence.split()[-1].strip('.!?').lower()
        if last_word in awkward_endings:
            continue
        
        valid_sentences.append(sentence)
    
    bullet_points = [f"{bullet} {sentence.capitalize()}" for sentence in valid_sentences]
    return '\n'.join(bullet_points)

def capitalize_abbreviations(text, abbreviations=['f', 'c']):
    pattern = r'\b(' + '|'.join(re.escape(abbr) for abbr in abbreviations) + r')\b'
    return re.sub(pattern, lambda match: match.group(0).upper(), text)

print("\nDIRECTIONS: \n")

directions_start_words = ['Mix', 'Bake', 'Serve']
directions_results = []

for start_word in directions_start_words:
    if start_word not in markov_directions:
        start_word = random.choice(list(markov_directions.keys()))
    directions_result = generate_ingredient_list(markov_directions, start_word=start_word, length=70)
    cleaned_directions = re.sub(r'\s+', ' ', directions_result).strip()
    directions_results.append(add_bullet_points(cleaned_directions))

directions_results = '\n'.join(directions_results)
directions_results = capitalize_abbreviations(directions_results)
print(directions_results)


print("\n-------test for slides--------\n")
words = ["The fox jumps over the dog.", "The cat runs around the dog"]
words = [line.split() for line in words]
print(words)
slides_markov = markov_chain_generator(words)
print(slides_markov)
