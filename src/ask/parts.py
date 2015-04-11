#!/usr/bin/env python
import nltk
import common.stanford as stanford
from multiprocessing import Pool
import settings
from filter import contains_linking
import re

parser = stanford.Parser()

class TreeFinder:

    tree = None
    index = None

    def __init__(self, tree, output):
        results = output[0].split(':')
        tree_num = int(results[0])
        item_num = int(results[1])
        self.find_tree(tree, item_num, 1)

    def find_tree(self, tree, index, so_far):
        #print tree
        #print so_far
        if not isinstance(tree,nltk.Tree):
            return so_far
        #print tree.height()
        for i, item in enumerate(tree):
            so_far += 1
            if so_far == index:
                self.tree = tree
                self.index = i
                return so_far+1
            so_far = self.find_tree(item, index, so_far)
            if so_far > index: return so_far
        return stuff


def original_text(sentence, tokens):
    #build regex
    regex_string = ''
    for i,token in enumerate(tokens):
        if token.startswith('-') and token.endswith('-'):
            continue
        regex_string += re.escape(token)
        if i != len(tokens) -1:
            regex_string += '[^a-zA-Z0-9]*';
    #search for regex in original string
    match = re.search(regex_string, sentence)
    if match:
        return match.group(0)
    return None


def get_parts(np, vp, sentence, verb_length):
    subject = original_text(sentence, np)
    if len(vp) < verb_length:
        return None
    verb = original_text(sentence, vp[0:verb_length])
    verb_object = original_text(sentence, vp[verb_length:])
    if subject and verb and verb_object:
        return subject, verb, verb_object
    return None

def get_patterns(sentence):
    sentence_object = (nltk.word_tokenize(sentence), sentence)
    verb = contains_linking(sentence_object)
    print verb
    if len(verb) == 0:
        return []
    if len(verb) == 1:
        p1 = 'NP $. (VP <, (/VB.?/ <, %s))'
        p1 = p1 % verb[0]
        return [p1]
    else:
        p1 = 'NP $. (VP < (VP <,(/VB.?/ <, %s) <2 (VP <, (/VB.?/ <, %s))))'
        p2 = 'NP $. (VP <,(/VB.?/ <, %s) <2 (VP <, (/VB.?/ <, %s)))'
        p1 = p1 % (verb[0],verb[1])
        p2 = p2 % (verb[0],verb[1])
        return [p1, p2]


#should make sure things work
def question_part(sentence):
    parse = parser.raw_parse_sents([sentence]).next().next()
    f = None
    for pattern in get_patterns(sentence):
        #call tregex
        output = stanford.tregex(str(parse), pattern, ['-x'])
        try:
            #try to get the tree
            f = TreeFinder(parse, output)
            break
        except:
            pass
    #if we didn't find anything, abandon ship
    if not f: return None
    np = f.tree[f.index]
    vp = f.tree[f.index+1]
    #print "NP: ", np.leaves()
    #print "VP: ", vp.leaves()
    yolo = get_parts(np.leaves(), vp.leaves(), sentence, 1)
    #print yolo
    return yolo

def question_parts(ranked, debug=False):
    #for rank in ranked:
    #    temp = question_part(rank)
    #    if temp: yield temp
    pool = Pool(settings.NUM_CORES)
    for parts in pool.imap(question_part, ranked):
        if parts: yield parts


if __name__ == '__main__':
    question = "Jane, the daughter of a magistrate, is coming to town next Saturday."
    original_text(question,['the','daughter','of'])
    #print question_part(question)
    #unit testing
    pass
