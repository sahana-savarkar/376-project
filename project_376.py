import re
import pandas as pd
from collections import defaultdict
import random

def markov_chain_generator(data_list):
    markov_chain = defaultdict(lambda: defaultdict(int))
    for tokens in data_list: # tokens are sentences, data_list is big list containing all sentences
        for i in range(len(tokens) - 1):
            current_word = tokens[i]
            next_word = tokens[i + 1]
            markov_chain[current_word][next_word] += 1 # counts the occurances of words following a particular word 
    for current_word, transitions in markov_chain.items():
        total_transitions = sum(transitions.values())
        for next_word in transitions:
            transitions[next_word] /= total_transitions #normalizing the probability 
    return markov_chain

def generate_text(chain, word, length): # uses the markov chain to generate text
    if word not in chain:
        word = random.choice(list(chain.keys())) # chooses a random word if the given word was invalid
    result = [word]
    for _ in range(length - 1):
        if word not in chain: # if a word ONLY corresponds to the END of a sentence structure
            break
        next_word = random.choices( # takes a list of words & their probabilities and makes a choice 
            list(chain[word].keys()),
            weights=list(chain[word].values())
        )[0]
        result.append(next_word)
        word = next_word
    return ' '.join(result)


def sentence_end(sentence): # returns the last word of a sequence
    last_word = sentence.strip().split()[-1]
    return last_word 


def truncate_invalid_ingredients(ingredients):
    valid_ingredients = []
    seen_ingredients = []
    for ingredient in ingredients:
        last_word_of_ingredient = sentence_end(ingredient)
        if last_word_of_ingredient not in invalid_ingredient_list and last_word_of_ingredient not in seen_ingredients:
            valid_ingredients.append(ingredient)
            seen_ingredients.append(last_word_of_ingredient)
    return valid_ingredients


def add_bullet_points(paragraph, bullet='•'):
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    valid_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        split_sentence = sentence.split(" ")
        if len(split_sentence) <= 2:
            continue
        last_word = sentence_end(sentence)
        if last_word in invalid_direction_endings:
            continue
        if sentence[-1] != '.':
            sentence = sentence + '!'
        valid_sentences.append(sentence)
    bullet_points = [f"{bullet} {sentence.capitalize()}" for sentence in valid_sentences]
    return '\n'.join(bullet_points)


def capitalize_abbreviations(text, abbreviations=['f', 'c']):
    pattern = r'\b(' + '|'.join(re.escape(abbr) for abbr in abbreviations) + r')\b'
    return re.sub(pattern, lambda match: match.group(0).upper(), text)

def most_frequent(mylist):
    big_list = []
    for l in mylist:
        for t in l:
            big_list.append(t)

    most_common = max(set(big_list), key=big_list.count)
    count = big_list.count(most_common)
    return most_common, count


data = pd.read_csv('pie_recipes.csv')
data = data.dropna(subset=['recipe_name', 'ingredients', 'directions'])

recipe_name_before = data['recipe_name'].head(1000).tolist()
recipe_name_list = [line.split() for line in recipe_name_before]

ingredients_before = data['ingredients'].head(1000).tolist()
ingredient_list = [line.split() for line in ingredients_before]


directions_list = data['directions'].head(1000).tolist()
directions_list = [line.split(" ") for line in directions_list]



print(most_frequent(recipe_name_list))
print(most_frequent(ingredient_list))
print(most_frequent(directions_list))

#recipe_most_common = most_frequent(big_recipe_list)
#prob_most_common = round((recipe_most_common[1] / len(big_recipe_list)), 4)
#print("probability of pie: " + str(prob_most_common))

# ingredient_string = ' '.join(ingredients_before).strip()
# recipe_string = ' '.join(recipe_name_before)
# ingredient_tokens = ingredient_string.split(",")
# recipe_tokens = recipe_string.split(",")




# print("Recipes:",most_frequent(recipe_tokens))
# print("Ingredients:",most_frequent(ingredient_tokens))


#print(most_frequent(recipe_name_list))
#print(most_frequent(ingredient_list))



markov_recipe_name = markov_chain_generator(recipe_name_list)
markov_ingredient_list = markov_chain_generator(ingredient_list)
markov_directions = markov_chain_generator(directions_list)


recipe_tokens = len(markov_recipe_name)
ingredient_tokens = len(markov_ingredient_list)
direction_tokens = len(markov_directions)

#pie_occurrence = 

print('\nRECIPE NAME: \n')
recipe_name_result = generate_text(markov_recipe_name, "", length=80)
print(recipe_name_result, "\n" + "-"*len(recipe_name_result))

ingredient_pattern = r'(\d+\s?\d*\/?\d*\s*(?:tablespoon|tbsp|teaspoon|tsp|cup|pounds|ounce|gram|g|liter|l)?\s*[a-zA-Z\-]+(?:\s?[a-zA-Z\-]+)*)'
invalid_ingredient_list = ['1', '1/4', '10', '12', '18', '2', '20', '3', '4', '5', '6', '7', '8', '9',
                            'peeled', 'sliced', 'cored', 'softened', 'halved', 'crushed', 'shredded',
                            'chopped', 'grated', 'lightly', 'firm', 'thinly', 'beaten', 'drained',
                            'packed', 'desired', 'prepared', 'freshly', 'quartered', 'needed', 'ripe',
                            'frozen', 'baked', 'split', 'melted', 'salted', 'unbaked', 'warmed', 'mixed',
                            'ground', 'inch', 'pieces', 'tablespoon', 'tablespoons', 'cup', 'cups', 'ounce',
                            'ounces', 'cold', 'a', 'd', "with", 'dried', 'pinch', 'fresh']

ingredients = generate_text(markov_ingredient_list, "", length=80)
ingredients = re.findall(ingredient_pattern, ingredients)
ingredients  = truncate_invalid_ingredients(ingredients)
for item in ingredients:
    print("-", item.strip())


invalid_direction_endings = ["and", "for", "or", "into", "in", "a", "an", "before", "after",
                    "with", "without", "not", "so", "if", "when", "while", "until", "the"]


print("\nDIRECTIONS: \n")

directions_start_words = ['Mix', 'Bake', 'Serve']
directions_results = []

for start_word in directions_start_words:
    directions_result = generate_text(markov_directions, start_word, length=70)
    cleaned_directions = re.sub(r'\s+', ' ', directions_result).strip()
    directions_results.append(add_bullet_points(cleaned_directions))

directions_results = '\n'.join(directions_results)
directions_results = capitalize_abbreviations(directions_results)
print(directions_results)

