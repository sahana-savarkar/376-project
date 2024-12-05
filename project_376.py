import re
import pandas as pd
from collections import defaultdict
import random

data = pd.read_csv('recipes.csv')
recipe_list = data['recipe_name'].head(1000).tolist()
ingredient_list = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split(",") for line in ingredient_list]

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


def generate_ingredient_list(chain, start_word, length):
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

# print("INGREDIENT LIST: ")
print('RECIPE LIST: ')
start_word = "Apple Pie"
generated_list = generate_ingredient_list(markov_chain, start_word=start_word, length=8)


#ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
#ingredients_list = re.findall(ingredient_pattern, generated_list)
recipe_pattern = r'(\d+\s?\d*\/?\d*\s*(?:apple|warm|caramel|turnover|crisp|pie|crumb|cake)(?:\s?(?:apple|warm|caramel|turnover|crisp|pie|crumb|cake))*)'
recipes_list = re.findall(recipe_pattern, generated_list)


# Print each ingredient on a new line
#for ingredient in ingredients_list:
 #   print(ingredient.strip())

for recipe in recipes_list:
    print(recipe.strip())
