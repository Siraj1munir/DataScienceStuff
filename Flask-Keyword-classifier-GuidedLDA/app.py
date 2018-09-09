# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import numpy as np
import pandas as pd
import random
import sys
import io
import guidedlda
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report,f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string
    data = pd.read_csv('text data.csv')

    texts = data['Article'] 
    labels = data['Class'] 
    profession =  data['Profession']
    stop = stopwords.words('english')
    stemmer = SnowballStemmer("english")
    preprocess = data['Article'].apply(lambda x: [item for item in x if item not in stop])
    preprocess = data["Article"].apply(lambda x: [stemmer.stem(y) for y in x])
    preprocess= data['Article'].str.replace("Context\n"," ")
    preprocess= data['Article'].str.replace("Context:"," ")
    preprocess= data['Article'].str.replace("CONTEXT:"," ")
    preprocess= data['Article'].str.replace("Context:"," ")
    preprocess= data['Article'].str.replace("Context."," ")
    path = 'record.txt'
    with io.open(path, encoding='utf-8') as f:
        text = f.read().lower()
    print('corpus length:', len(text))
    chars = sorted(list(set(text)))
    print('total chars:', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 40
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])

    print('Vectorization...')
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        y[i, char_indices[next_chars[i]]] = 1
        
    vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.REUTERS)
    # Guided LDA Implementation
    model = guidedlda.GuidedLDA(n_topics=52, n_iter=100, random_state=7, refresh=20)
    model.fit(y)
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1] 
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    dataSet = pd.read_csv("new_topics.csv")
    def text_process(mess):
        nopunc = [char for char in mess if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=text_process)),
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
    ])
    pipeline.fit(dataSet["Topics"],dataSet["Profession"])
    a = dataSet["Topics"]
    prediction = pipeline.predict(a)
    print(classification_report(dataSet["Profession"],prediction))
    b = ["Data"]
    prediction = pipeline.predict(b)
    print("Predicted Profession:" , prediction)

@app.route("/prediction")
def getPrediction():
    dataSet = pd.read_csv("new_topics.csv")
    def text_process(mess):
        nopunc = [char for char in mess if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=text_process)),
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
    ])
    pipeline.fit(dataSet["Topics"],dataSet["Profession"])
    a = dataSet["Topics"]
    prediction = pipeline.predict(a)
    print(classification_report(dataSet["Profession"],prediction))
    b = ["Artificial"]
    prediction = pipeline.predict(b)
    return render_template(
        'prediction.html',prediction=prediction)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)