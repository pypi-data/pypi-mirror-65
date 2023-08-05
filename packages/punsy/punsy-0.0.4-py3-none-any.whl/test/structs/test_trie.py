import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from punsy.structs.trie import Trie
from punsy.structs.suffix_trie import SuffixTrie

class TestTrie(unittest.TestCase):

    def test_insert_suffixes(self):
        words = [
            'cat',
            'bat',
            'catinthehat',
            'rat',
        ]
        trie = Trie()
        for word in words:
            trie.insert(word)

        for word in words:
            self.assertTrue(trie[word].final)

    def test_insert(self):
        trie = Trie()
        words = {
            'NONE': ['N', 'AH1', 'N'],
            'NAAN': ['N', 'AH1', 'N'],
            'ONCE': ['W', 'AH1', 'N', 'S'],
            'PUN':  ['P', 'AH1', 'N'],
        }
        for word, pronunciation in words.items():
            trie.insert(pronunciation, word)
        self.assertEqual(['NONE', 'NAAN'], trie[['N', 'AH1', 'N']].data)
        self.assertEqual(['ONCE'], trie['W', 'AH1', 'N', 'S'].data)
        self.assertEqual(['PUN'], trie['P', 'AH1', 'N'].data)


    def test_search_suffix(self):
        trie = SuffixTrie()
        words = {
            'NONE': ['N', 'AH1', 'N'],
            'NAAN': ['N', 'AH1', 'N'],
            'ONCE': ['W', 'AH1', 'N', 'S'],
            'PUN':  ['P', 'AH1', 'N'],
            'ANSWER': ['AH1', 'N', 'S', 'ER'],
        }
        for word, pronunciation in words.items():
            trie.insert(pronunciation, word)
        self.assertEqual(
            ['NONE', 'NAAN', 'PUN'],
            trie.rhymes_for_suffix(['AH1', 'N'])
        )

    def test_get_item(self):
        trie = SuffixTrie()
        trie.insert('A', 123)
        # Assert A is stored correctly
        self.assertEqual([123], trie['A'].data)
        self.assertEqual('A', trie['A'].value)

        # Insert a child
        trie.insert('AB', 321)
        # Assert A is preserved
        self.assertEqual([123], trie['A'].data)
        self.assertEqual('A', trie['A'].value)
        self.assertTrue(trie['A'].final)
        # Assert AB is stored correctly
        self.assertTrue('A' in trie['B'].children)
        self.assertEqual([321], trie['AB'].data)
        self.assertTrue(trie['AB'].final)

        # Insert a child of -AB: CAB
        trie.insert('CAB', 101)
        # Assert that reverse order is correct
        self.assertEqual(['A', 'B'], list(trie.trie.children.keys()))
        self.assertEqual([101], trie['CAB'].data)
        self.assertEqual('C', trie['CAB'].value)
        self.assertTrue(trie['CAB'].final)

