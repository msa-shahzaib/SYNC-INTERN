import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
stemmer = PorterStemmer()


# nltk.download('punkt')
def tokenize(prompt):
    return nltk.word_tokenize(prompt)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_prompt, all_words):
    stemmed_prompt = [stem(word) for word in tokenized_prompt]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for i, word in enumerate(all_words):
        if word in stemmed_prompt:
            bag[i] = 1.0

    return bag
