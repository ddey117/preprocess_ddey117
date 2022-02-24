import re
import os
import sys

import pandas as pd
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
import unicodedata

from bs4 import BeautifulSoup
from textblob import TextBlob

# nlp = spacy.load('en_core_web_sm')

def _get_wordcounts(x):
    length = len(str(x).split())
    return length

def _get_charcounts(x):
    s = x.split()
    x = ''.join(s)
    return len(x)

def _get_avg_wordlen(x):
    count = _get_charcounts(x)/_get_wordcounts(x)
    return count

def _get_stopwords_counts(x):
    stop_count = len([t for t in x.split() if t in stopwords])
    return stop_count

def _get_hashtag_counts(x):
    hash_counts = len([t for t in x.split() if t.startswith('#')])
    return hash_counts

def _get_mention_counts(x):
    mention_counts = len([t for t in x.split() if t.startswith('@')])
    return mention_counts

def _get_digit_counts(x):
    return len([t for t in x.split() if t.isdigit()])

def _get_uppercase_counts(x):
    return len([t for t in x.split() if t.isupper()])

def _get_expan(x):

    str(x).lower()

    contractions = {
    "a'ight": "alright",
    "ain't": "am not",
    "amn't": "am not",
    "arencha": "are not you",
    "aren't": "are not",
    "‘bout": "about",
    "can't": "cannot",
    "cap’n": "captain",
    "'cause": "because",
    "’cept" : "except",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "cuppa": "cup of",
    "dammit": "damn it",
    "daren't": "dared not",
    "daresn't": "dare not",
    "dasn't": "dare not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "dunno" : "do not know",
    "d'ye": "do you",
    "e'en": "even",
    "e'er": "ever",
    "'em": "them",
    "everybody's": "everybody is",
    "everyone's": "everyone is",
    "finna": "fixing to",
    "fo’c’sle": "forecastle",
    "’gainst": "against",
    "g'day": "good day",
    "gimme": "give me",
    "giv'n": "given",
    "gi'": "give us",
    "gonna": "going to",
    "gon't": "go not" ,
    "gotta": "got to",
    "hadn't": "had not",
    "had've": "had have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd":  "he would",
    "he'll": "he will",
    "helluva": "hell of a",
    "he's": "he is",
    "here's": "here is",
    "how'd" : "how would",
    "howdy" : "how do you fare",
    "how'll": "how will",
    "how're": "how are",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'd'nt": "i would not",
    "i'd'nt've": "i would not have",
    "i'll": "i will",
    "i'm": "i am",
    "imma": "i am about to",
    "i'm'o": "i am going to",
    "innit": "is it not it",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "idunno": "i do not know",
    "kinda" : "kind of",
    "let's": "let us",
    "loven't": "love not",
    "ma'am": "madam",
    "mayn't": "may not",
    "may've": "may have",
    "methinks":" i think",
    "mightn't": "might not",
    "might've": "might have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "must've": "must have",
    "‘neath": "beneath",
    "needn't": "need not",
    " nal ": " and all ",
    "ne'er": "never",
    " o'er" : " over ",
    " ol '": " old ",
    "oughtn'": "ought not",
    "‘round": "around",
    "shalln't": "shall not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "he will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "somebody's": "somebody is",
    "someone's": "someone is",
    "something's": "something is",
    "so're": "so are",
    "so's": "so is",
    "so've": "so have",
    "that'll": "that shall",
    "that're": "that are",
    "that's": "that is",
    "that'd": "that would",
    "there'd": "there had",
    "there'll": "there shall",
    "there're": "there are",
    "there's": "there is",
    "these're": "these are",
    "these've": "these have",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "this's": "this is",
    "those're": "those are",
    "those've": "those have",
    "'thout": "without",
    "’til": "until",
    "'tis": "it is",
    "to've": "to have",
    "'twas": "it was",
    "'tween": "between",
    "'twere": "it were",
    "w'all": "we all",
    "wanna": "want to",
    "wasn't": "was not",
    " we'd ": " we would ",
    "we'd've": "we would have",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "whatcha": "what are you",
    "what'd": "what did",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "where'd": "where did",
    "where'll": "where will",
    "where're": "where are",
    "where's": "where is",
    "where've": "where have",
    "which'd": "which would",
    "which'll": "which will",
    "which're": "which are",
    "which's": "which is",
    "which've": "which have",
    "who'd": "who would",
    "who'd've": "who would have",
    "who'll": "who will",
    "who're":" who are",
    "who's": "who is ",
    "who've": "who have",
    "why'd": "why did",
    "why're": "why are",
    "why's": "why has ",
    "willn't": "will not",
    "won't": "will not",
    "wonnot": "will not",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all ",
    "y'all'd've": "you all would have",
    "y'all'd'n't've": "you all would not have",
    "y'all're": "you all are" ,
    "y'all'ren't": "you all are not",
    " y'at ": " you at ",
    "yes'm": "yes madam",
    "y'know": "you know",
    " yessir ": " yes sir ",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "when'd": "when did",
    "willn't": "will not",
    #append extra web lingo
    " u ": " you ",
    " ur ": " your ",
    " n ": " and ",
    " dis ": " this ",
    " bak ": " back ",
    " brng ": " bring ",
    "sux": "sucks",
    "gr8": "great",
    " amzing ": " amazing ",
    " k ": "ok",
    " kk ": "ok",
    " il ": "i will"}

    if type(x) is str:
        for key in contractions:
            value = contractions[key]
            x = x.replace(key, value)
        return x
    else:
        return x

def _get_emails(x):
    emails = re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)', x)
    counts = len(emails)

    return counts, emails

def _remove_emails(x):
    return re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", x)

def _get_urls(x):
    urls = re.findall(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', x)
    counts = len(urls)

    return counts, urls

def _remove_urls(x):
    return re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '' , x)

def _remove_rt(x):
    return re.sub(r'rt\ ', '', x).strip()

def _remove_special_chars(x):
    x = re.sub(r'[^\w ]+', "", x)
    x = ' '.join(x.split())
    return x

def _remove_html_tags(x):
    return BeautifulSoup(x, 'lxml').get_text().strip()

def _remove_accented_chars(x):
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return x

def _remove_stopwords(x):
    return ' '.join([t for t in x.split() if t not in stopwords])

# def _make_base(x):
#     x = str(x)
#     x_list = []
#     doc = nlp(x)

#     for token in doc:
#         lemma = token.lemma_
#         if lemma == '-PRON-' or lemma == 'be':
#             lemma = token.text

#         x_list.append(lemma)
#     return ' '.join(x_list)

def _get_value_counts(df, col):
    text = ' '.join(df[col])
    text = x.split()
    freq = pd.Series(text).value_counts()
    return freq
    

def _remove_common_words(x, freq, n=20):
    fn = freq[:n]
    x = ' '.join([t for t in x.split() if t not in fn])
    return x

def _remove_rarewords(x, freq, n=20):
    fn = freq.tail(n)
    x = ' '.join([t for t in x.split() if t not in fn])
    return x

def _spelling_correction(x):
    x = TextBlob(x).correct()
    return x
