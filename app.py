#!/usr/bin/env python3
import nltk
import sqlite3
import string
import operator
from nltk.corpus import stopwords


LANGUAGE = 'english'
DB_NAME = 'db/demo.db'
SAMPLE_DATA = 'data/data.txt'
DEFAULT_RESPONSE = 'Sorry. We cannot help you at the moment. Please, try again later.'


def auto_reply(question):
    if question == '' or question is None:
        return 'Sorry, I do not comprehend the question as asked..'

    tokens = cleanup(question)
    if tokens:
        freq = nltk.FreqDist(tokens)
        # plot token by frequency
        answer = input('\nWould like to plot result? [Y/N]: ')
        if answer.upper() == 'Y':
            # using matplotlib to display result.. a new window should open
            freq.plot(15, cumulative=False, title='Word count', linewidth=3)
        # get most repeated the word/token
        word = max(freq.items(), key=operator.itemgetter(1))[0]
        # fetch automated response
        return fetch_response(word)
    return 'Please provide more details in your question.'

    
def cleanup(sentence):
    tokens = nltk.word_tokenize(sentence)
    # do some cleanup - remove unecessary word(s) e.g ?,.@#%...
    punctuation = string.printable
    for token in tokens:
        if token.lower() in stopwords.words(LANGUAGE) or token in punctuation:
            tokens.remove(token)
    return tokens if len(tokens) > 0 else None


def fetch_response(keyword):
    query = 'SELECT response FROM automated_responses WHERE tag=:tag ORDER BY 1 LIMIT 1'
    conn = None
    response = DEFAULT_RESPONSE

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(query, {'tag': keyword.lower()})
        raw_data = c.fetchone() 
        response = raw_data[0] if raw_data is not None else 'No data found. You query couldn\'t be processed at the moment.' 
    except Exception as e:
        pass # we should avoid doing this.
    # close connection -- ALWAYS!!!!
    if conn is not None:
        conn.close()
    return response


if __name__ == '__main__':
    try:
        with open(SAMPLE_DATA, 'r') as f:
            text = ''.join(f.readlines()).replace('\n', '')
            if text:
                print('\n** Auto-Reply: {}'.format(auto_reply(text)))
            else:
                print('No data to analyze')
    except KeyboardInterrupt:
        pass  # not good, we'd do better
