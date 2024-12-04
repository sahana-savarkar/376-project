import re
import pandas as pd

corpus_string = ""
corpus = []
dct = {}
i = 0

data = pd.read_csv('recipes.csv')
recipe_list = data['recipe_name'].head(10).tolist()
ingredient_list = data['ingredients'].head(10).tolist()
tokenized = [line.split() for line in ingredient_list]

print(recipe_list)
print(tokenized)

with open('short_ingredient_list.csv', 'r') as f:
    for line in f:
        corpus_string = line.replace('\n',' ')
        corpus_string = corpus_string.replace('\t',' ')
        corpus = corpus_string.split(";")
        corpus = [item.strip() for item in corpus]
        corpus = [
            re.sub(r'[^\w\s,.\-()\u00BC-\u00BE\u2150-\u215E]+', '', item).strip()
            for item in corpus
        ]
        dct[recipe_list[i]] = corpus
        i = i+1
            

        
# for key, value in dct.items():
#    print(f"Key: {key}, Value: {value}")