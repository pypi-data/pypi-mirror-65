#!/usr/bin/env python3
'''
A python implementation of the Trie data structure.

    https://en.wikipedia.org/wiki/Trie

The Trie is a memory-optimised data store for strings. It stores strings using a
k-ary tree structure (a tree in which each node has up to `k` children)

e.g. to store the words `car`, `cat`, 'bar' and 'bat'

       /- t
  b - a - r
/
- c - a -|- r
       \- t

Usage:

t = Trie()  # create a trie

t.insert('cat')                   # insert a word into the trie
t.insert('cat', 'feline')         # insert a word and associated metadata into the trie
'cat' in t,     t.contains('cat') # check if the trie contains a word
t['cat'],       t.get('cat')      # retrieve a node from the trie
t,              print(t)          # print the contents of the trie
'''

import os, sys

class Trie(object):
    '''
    A Trie class which implements insert, contains and get methods.
    '''

    def __init__(self, value=None, data=None):
        self.value = value
        self.children = dict()
        self.final = False
        self.data = list()
        if data:
            self.data.extend((data,))

    def insert(self, word, data=None):
        'Insert a word into the trie, with optional data attached'
        current = self
        for i, letter in enumerate(word):
            try:
                current = current.children[letter]
            except KeyError:
                current.children[letter] = Trie()
                current = current.children[letter]
            current.value = letter
        current.final = True
        if data:
            current.data.extend((data,))

    def __getitem__(self, word):
        'Retrieve a node (or branch) from the trie by key, otherwise raise KeyError'
        current = self
        for i, letter in enumerate(word):
            try:
                current = current.children[letter]
            except KeyError:
                raise KeyError(f'word "{word}" not found')
        return current

    def asdict(self):
        'Return a representation of the node as a dict, for use with visualising using JSON'
        d = {}
        for k in ['data', 'value', 'final']:
            if k in self.__dict__:
                d[k] = self.__dict__[k]
        if self.children:
            d['children'] = {k: v.asdict() for k, v in self.children.items()}
        return d

    def __repr__(self):
        'Flat string representation of the node'
        if self.value is None:
            return f'(root) -> {self.children}'
        else:
            return f'{self.value} ({self.data}) -> {self.children}'

    def __contains__(self, value):
        'Returns True if the trie contains the key as an entire word, otherwise returns False'
        try:
            return self[value].final
        except (KeyError, IndexError):
            return False


if __name__ == '__main__':
    from IPython import embed
    print(__doc__)
    embed()

