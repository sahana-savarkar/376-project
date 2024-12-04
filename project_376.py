corpus_string = ""
corpus = []

with open('short_ingredient_list.csv', 'r') as f:
    corpus_string = f.readline()
    corpus_string = corpus_string.replace('\n',' ')
    corpus_string = corpus_string.replace('\t',' ')
    corpus = corpus_string.split(";")
    corpus = [item.strip() for item in corpus]

print(corpus)

