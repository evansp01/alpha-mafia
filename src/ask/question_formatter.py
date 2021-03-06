#!/usr/bin/env python
import nltk
import named_entities as ne
import os
import random
import settings

def sanitize(obj,subj=None):
    obj = obj.replace("also ","")
    if not subj:
        return obj
    subj = subj.replace("also ","")
    return obj, subj


def cap_subj(subj, tags):
    subj = subj.encode('utf-8')
    if not subj[0].isupper():
        return False
    entities = ne.named_entities(tags)
    if len(entities) == 0:
        return False
    if 'Moscow' in subj:
        print nltk.word_tokenize(subj)[0]
        print entities[0][0]
    if nltk.word_tokenize(subj)[0] != entities[0][0]:
        return False
    return True

def decapitalize(subj):
    return subj[:1].lower() + subj[1:] if subj else ''

def space(obj):
    return obj[0].isalnum()

def format_is(subj, verb, obj, tags):
    obj, subj = sanitize(obj, subj=subj)
    if not cap_subj(subj, tags):
        subj = decapitalize(subj)
    if space(obj):
        obj = ' '+obj
    verb = verb.capitalize()
    if random.random() < settings.PERCENT_NEGATED:
        subj = subj + ' not'
    return ("%s %s%s?" % (verb, subj, obj),'is')

def format_wh(wh, verb, obj):
    obj = sanitize(obj)
    if space(obj):
        obj = ' '+obj
    wh = wh.capitalize()
    return ("%s %s%s?" % (wh, verb, obj), 'wh')

def format_wh_class(wh, clss, verb, obj):
    obj = sanitize(obj)
    if space(obj):
        obj = ' '+obj
    wh = wh.capitalize()
    return ("%s %s %s%s?" % (wh, clss, verb, obj),'wh-class')

if __name__ == '__main__':
    pass
