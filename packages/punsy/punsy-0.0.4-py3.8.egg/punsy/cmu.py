#!/usr/bin/env python3

import os, sys
from argparse import ArgumentParser
from pkg_resources import resource_string
import json
import logging

from punsy.structs.suffix_trie import SuffixTrie

DICTIONARY_FPATH = 'data/cmudict-0.7b.utf8'

class CMU:
    def __init__(self, cmu_fpath):
        self.fpath = cmu_fpath
        self.phonemes = SuffixTrie()
        self.mapping = {}
        self.n_lines = CMU.count_lines(self.fpath)

    def run(self):
        logging.debug(f'Parsing & loading {self.n_lines} entries from CMU dictionary file')
        for word, phonemes in CMU.parse(self.fpath):
            phonemes = phonemes.split(' ')
            self.phonemes.insert(phonemes, word)
            self.mapping[word] = phonemes

    def rhymes_for(self, suffix, offset=3, max_depth=10):
        pron = self.mapping[suffix]
        logging.debug(f'Pronunciation of "{suffix}" is "{"-".join(pron)}"')
        logging.debug(f'Fetching rhymes, applying offset={offset}: "{"-".join(pron[offset:])}"')
        rhymes = self.phonemes.rhymes_for_suffix(
            pron,
            offset=offset,
            max_depth=10
        )
        logging.debug(f'Rhymes for {suffix}: {rhymes}')
        return rhymes

    @staticmethod
    def parse(fpath='', delimiter='|'):
        for line in CMU.__iter_file(fpath):
            yield line.strip().split(delimiter)

    @staticmethod
    def count_lines(fpath=''):
        for i, _ in enumerate(CMU.__iter_file(fpath)):
            pass
        else:
            return i

    @staticmethod
    def __iter_file(fpath=''):
        if fpath:
            with open(fpath, 'r') as istream:
                yield from istream
        else:
            for line in resource_string('punsy', DICTIONARY_FPATH).decode().split('\n'):
                if line:
                    yield line


class POC:
    def __init__(self, cmu_fpath):
        self.cmu = CMU(cmu_fpath)
        self.cmu.run()

    def run(self, sentence, offset=1, max_depth=10):
        import random
        parts = sentence.split(' ')
        word = parts[-1].upper()
        rhyme = random.choice(self.cmu.rhymes_for(
            word, offset=offset, max_depth=max_depth
        ))
        parts[-1] = rhyme
        return ' '.join(parts)


def poc():
    parser = ArgumentParser(prog='punsy')

    parser.add_argument('--sentence', type=str, required=True, help='The sentence to punnify')
    parser.add_argument('--cmu-file', type=str, help='(optional) the path of the cmu rhyming dictionary')
    parser.add_argument('--offset', type=int, default=2, help='The number of syllables to match')
    parser.add_argument('--max-depth', type=int, default=10, help='The maximum length of a matched rhyming word')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format='- %(message)s')

    result = POC(args.cmu_file).run(
        sentence=args.sentence,
        offset=args.offset
    )

    logging.info(f'Generated pun: "{args.sentence}" => "{result}"')

if __name__ == '__main__':
    poc()
