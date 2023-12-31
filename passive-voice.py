#!/usr/bin/env python


"""
Adapted from:
    https://github.com/flycrane01/nltk-passive-voice-detector-for-English/tree/master
"""


# Python Standard Library

# Other dependencies
import nltk

# Local files


__author__ = 'Leonardo van der Laat'
__email__ = 'laat@umich.edu'


def isPassive(sentence):
    # all forms of "be"
    beforms = ['am', 'is', 'are', 'been', 'was', 'were', 'be', 'being']

    # NLTK tags "do" and "have" as verbs,
    # which can be misleading in the following section.
    aux = ['do', 'did', 'does', 'have', 'has', 'had']

    words = nltk.word_tokenize(sentence)
    tokens = nltk.pos_tag(words)
    tags = [i[1] for i in tokens]

    # no PP, no passive voice.
    if tags.count('VBN') == 0:
        return False
    # one PP "been", still no passive voice.
    elif tags.count('VBN') == 1 and 'been' in words:
        return False
    else:
        # gather all the PPs that are not "been".
        pos = [
            i for i in range(len(tags))
            if tags[i] == 'VBN'
            and words[i] != 'been'
        ]
        for end in pos:
            chunk = tags[:end]
            start = 0
            for i in range(len(chunk), 0, -1):
                last = chunk.pop()
                if last == 'NN' or last == 'PRP':
                    # get the chunk between PP and the previous NN or PRP
                    # (which in most cases are subjects)
                    start = i
                    break
            sentchunk = words[start:end]
            tagschunk = tags[start:end]
            # get all the verbs in between
            verbspos = [
                i for i in range(len(tagschunk))
                if tagschunk[i].startswith('V')
            ]
            # if there are no verbs in between, it's not passive
            if verbspos != []:
                for i in verbspos:
                    # check if they are all forms of "be" or auxiliaries such
                    # as "do" or "have".
                    if sentchunk[i].lower() not in beforms \
                       and sentchunk[i].lower() not in aux:
                        break
                else:
                    return True
    return False


if __name__ == '__main__':
    with open('text.tex') as f:
        sents = nltk.sent_tokenize(
            f.read().replace('\n', ' ').replace('\r', '')
        )
        for sent in sents:
            if isPassive(sent):
                print(sent)
