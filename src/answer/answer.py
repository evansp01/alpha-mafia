#!/usr/bin/env python
import nltk
from tfidf import tfidf_list
from nltk.stem.snowball import SnowballStemmer
from coref import get_resolved_sentence
from coref import pronouns
stemmer = SnowballStemmer('english')

CONTEXT_LENGTH=6

def snowball_input(sentences, question):
    sentences = [[stemmer.stem(word) for word in nltk.word_tokenize(sentence)] for sentence in sentences]
    question = [stemmer.stem(word) for word in nltk.word_tokenize(question)]
    return sentences, question

def snowball_count(word, sentence):
    if word in sentence:
        return 1
    return 0

def max_sentence(sentences):
    answer = max(enumerate(sentences), key=lambda x: sum(x[1][1]))
    return answer

def get_context(index, sentences):
    begin = max(index-CONTEXT_LENGTH, 0)
    return sentences[begin:index+1]

def answer(article, question):
    sentences = nltk.sent_tokenize(article.strip())

    s, q = snowball_input(sentences, question)
    snowball = tfidf_list(sentences, s,q,snowball_count)
    index, snowball = max_sentence(snowball)

    #this needs work before we use it
    context = get_context(index, sentences)
    resolve = False
    for pronoun in pronouns:
        if pronoun in nltk.word_tokenize(context[-1].lower()):
            resolve = True
    if resolve:
        answer = get_resolved_sentence(context)
    else:
        answer = snowball[0]
    return answer


def answer_all(article, questions):
    return [answer(article, question) for question in questions]

if __name__ == '__main__':
    #unit testing
    pass
