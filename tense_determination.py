#!/usr/bin/env python


"""
"""


# Python Standard Library
from termcolor import colored

# Other dependencies
import nltk

# Local files


__author__ = 'Leonardo van der Laat'
__email__ = 'laat@umich.edu'


def determine_tense(sentence):
    text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(text)

    out = []
    for word, tag in tagged:
        if tag == 'MD':
            out.append(colored(word, 'red'))
        elif tag in 'VBP VBZ':
            out.append(colored(word, 'blue'))
        elif tag in 'VBD VBN':
            out.append(colored(word, 'green'))
        else:
            out.append(word)
    print(*out, sep=' ')
    return


if __name__ == '__main__':
    with open('text.tex') as f:
        for line in f:
            for sentence in line.split('.'):
                determine_tense(sentence)
