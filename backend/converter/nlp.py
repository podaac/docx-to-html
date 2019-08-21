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


# possible callback function with matcher -- might use this
def on_match(matcher, doc, id, matches):
    print("Matched!", matches)


# compares two words and returns their similarity score
def compare_words(w1, w2):
    w1 = nlp(w1)
    w2 = nlp(w2)

    return w1.similarity(w2)


def get_replacement_word(word):
    md_matcher = Matcher(nlp.vocab)
    md_matcher.add("Mission Description", None, [{"LOWER": "mission"}, {"LOWER": "description"}])
    md_matches = md_matcher(word)
    if md_matches:
        return "Mission Description"

    ms_matcher = Matcher(nlp.vocab)
    ms_matcher.add("Sensor Overview", None, [{"LOWER": "sensor"}, {"LOWER": "overview"}])
    ms_matches = ms_matcher(word)
    if ms_matches:
        return "Sensor Overview"

    summary_key = nlp('abstract summary overview document introduction, \
        abridgment, brief, compendium,condensation, conspectus, digest, \
            outline, synopsis')
    for token in summary_key:
        sim_score = word.similarity(token)
        # print(word, " <-> ", token, "=> ", sim_score)
        if sim_score > .9:
            # print("Similarity Score:", sim_score)
            return "Abstract"

    acknowledgements_key = nlp('credit acknowledgements citations')
    for token in acknowledgements_key:
        sim_score = word.similarity(token)
        # print(word, " <-> ", token, "=> ", sim_score)
        if sim_score > .9:
            # print("Similarity Score:",sim_score)
            return "Acknowledgements"
    
    return

# cool stuff in nltk:
# bigrams/trigrams etc - finding collections of words
# creating our own Corpus with the User Guides we have, we can do NLP on them
# ie, from nltk.corpus import PlaintextCorpusReader -> http://www.nltk.org/book/ch02.html#loading-your-own-corpus
# http://www.nltk.org/book/ch02.html#wordnet ->
# http://www.nltk.org/book/ch02.html#semantic-similarity -> similar to spaCy sim scores
# http://www.nltk.org/book/ch05.html -> NLP Pipeling: tokenization, tagging


# gensim potential -> word 2 vectors
# could potentially look into different sections of text and compare them across documents or something





