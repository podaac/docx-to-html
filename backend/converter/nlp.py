from __future__ import unicode_literals

import spacy
from spacy.matcher import Matcher
import re

nlp = spacy.load('en_core_web_lg')


# strip all numbers and special characters and return an nlp vector string
def prepare_string_for_nlp(string):
    s = str(string)
    for k in s.split("\n"):
        s = re.sub(r"[^a-zA-Z]+", ' ', k)
    s = nlp(s)
    return s


# compares two words and returns their similarity score
# allows for passing in strings - does the nlp() for you
def compare_words(w1, w2):
    w1 = nlp(w1)
    w2 = nlp(w2)

    return w1.similarity(w2)


# takes in a word and returns a replacement word if sim score is >.9 or phrase match
def get_replacement_word(word):
    # ##################### #
    # Exact Phrase Matching #
    # ##################### #

    # search for exact phrase 'Mission Description' and change it 
    md_matcher = Matcher(nlp.vocab)
    md_matcher.add("Mission Description", None, [{"LOWER": "mission"}, {"LOWER": "description"}])
    is_match = md_matcher(word)
    if is_match:
        return "Mission Description"

    # ########################### #
    # Similarity Score on Phrases #
    # ########################### #

    # search for >.9 similarity score on a phrase and change it to a different phrase
    processing_methodology = nlp('Processing Methodology')
    sim_score = word.similarity(processing_methodology)

    if sim_score > .9:
        return 'Processing Methodology'

    # ####################################### #
    # Similarity Score on each word in a list #
    # ####################################### #

    # search for >.9 similarities to 'Abstract' and change it to 'Abstract'
    summary_key = nlp('abstract summary overview document introduction \
        abridgment brief compendium condensation conspectus digest \
            outline synopsis')
    for token in summary_key:
        sim_score = word.similarity(token)
        if sim_score > .9:
            return "Abstract"

    # search for >.9 similarities to 'Acknowledgements' and change it to 'Acknowledgements'
    acknowledgements_key = nlp('credit acknowledgements citations')
    for token in acknowledgements_key:
        sim_score = word.similarity(token)
        if sim_score > .9:
            return "Acknowledgements"


# cool stuff in nltk:
# bigrams/trigrams etc - finding collections of words
# creating our own Corpus with the User Guides we have, we can do NLP on them
# ie, from nltk.corpus import PlaintextCorpusReader -> http://www.nltk.org/book/ch02.html#loading-your-own-corpus
# http://www.nltk.org/book/ch02.html#wordnet ->
# http://www.nltk.org/book/ch02.html#semantic-similarity -> similar to spaCy sim scores
# http://www.nltk.org/book/ch05.html -> NLP Pipeling: tokenization, tagging


# gensim potential -> word 2 vectors
# could potentially look into different sections of text and compare them across documents or something





