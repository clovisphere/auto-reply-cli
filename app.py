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
        return 'Sorry, I do not comprehend the question as asked.. Please rephrase.'
    tokens = cleanup(question.lower())
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
    return DEFAULT_RESPONSE

    
def cleanup(sentence):
    tmp = [ token for token in nltk.word_tokenize(sentence) if token not in string.punctuation]
    tokens = []
    for token in tmp: #TODO: figure out 'nested list comprehension', and make this bit more pythonic
        if token not in stopwords.words(LANGUAGE):
            tokens.append(token)
    return tokens

def fetch_response(keyword):
    query = 'SELECT response FROM automated_responses WHERE tag=:tag ORDER BY 1 LIMIT 1'
    conn = None
    response = DEFAULT_RESPONSE

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(query, {'tag': keyword.lower()})
        raw_data = c.fetchone() 
        response = raw_data[0] if raw_data is not None else 'No data found.' 
    except Exception as e:
        pass #TODO: log exception, perhaps
    # close connection
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
                print('No data to analyze.')
    except KeyboardInterrupt:
        pass  # in case, someone does a CTRL-C/CTRL-Z, just in case
