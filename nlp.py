from textblob import TextBlob
import nltk
import pandas as pd
import datetime

string = "There are two hundred eggs and they are great but they also are old and worthless."

tagged = nltk.pos_tag(nltk.word_tokenize(string))

adjectives = []
proper_nouns = []
nouns = []
for token, tag in tagged:
    if tag == "NN":
        nouns.append(token)
    elif tag == "NNP":
        proper_nouns.append(token)
    elif tag == "JJ":
        adjectives.append(token)
    
# print(adjectives)
# print(proper_nouns)
# print(nouns)

tb = TextBlob(string)
print(tb.words)
print(tb.sentiment.polarity)