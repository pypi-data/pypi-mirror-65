#!/usr/bin/env python3
'''
A python implementation of the Trie data structure, specialising in searching by _suffix_.

    https://en.wikipedia.org/wiki/Trie

This trie has the ability to store and search words in reverse

e.g. to find words rhyming with '-at', the search is reversed to 'ta' and then
the child nodes 'b' (bat) and 'c' (cat) are returned.

t - a - b
      \ c

Usage:

t = SuffixTrie()                    # create a suffix trie

t.insert(['K1', 'AH1', 'T'], 'cat') # insert a pronunciation sequence and associated word metadata into the trie
t[['K1', 'AH1', 'T']]               # retrieve a node from the trie
t,              print(t)            # print the contents of the trie
print(t.json())                     # pretty-print the trie as a JSON object
t.rhymes_for_suffix(['AH1', 'T'])   # return all data for words ending in 'at'
t.rhymes_for_suffix(
    ['K1', 'AH1', 'T'],
    offset=1
)                                   # return all data for words rhyming with 'kat' (i.e. ending in 'at')
'''

import json, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from punsy.structs.trie import Trie

class SuffixTrie:

    def __init__(self):
        self.trie = Trie()

    def insert(self, word, data):
        self.trie.insert(
            list(reversed(word)),
            data
        )

    def __getitem__(self, word):
        return self.trie.__getitem__(
            list(reversed(word))
        )

    def json(self):
        return json.dumps(self.trie.asdict(), indent=2)

    def rhymes_for_suffix(self, word, offset=0, max_depth=10):
        '''Return all rhymes for the word/suffix, skipping <offset> number of
        syllables, and returning matches of
        length=(<max_depth> + <length of word>)'''
        return SuffixTrie._collect_child_data(
            self.__getitem__(word[offset:]),
            max_depth=max_depth,
            results=list()
        )

    @staticmethod
    def _collect_child_data(node, max_depth=10, results=list()):
        if node.final:
            results.extend(node.data)
        for key, child in node.children.items():
            if max_depth > 0:
                SuffixTrie._collect_child_data(child, max_depth-1, results)
        return results


if __name__ == '__main__':
    from IPython import embed
    print(__doc__)
    embed()

