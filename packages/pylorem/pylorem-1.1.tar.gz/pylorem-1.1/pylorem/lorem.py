import json
from typing import Optional, List, Iterable
import random
import itertools
from functools import lru_cache
import pathlib
import os

pd = pathlib.Path(__file__).parent.absolute()
loremfile = os.path.join(pd, "lorem.json")


class LoremIpsum(object):

    @classmethod
    @lru_cache(maxsize=128)
    def _load_words(cls) -> List[str]:
        """ Returns a list of words """
        with open(loremfile, "r") as fp:
            return json.load(fp)

    @classmethod
    def _get_words(cls) -> List[str]:
        """ Returns a shuffled list of words """
        words = cls._load_words()
        random.shuffle(words)
        return words

    @classmethod
    def gen_words(cls) -> Iterable[str]:
        """ Word generator """
        for word in itertools.cycle(cls._get_words()):
            yield word

    @classmethod
    def word(cls) -> str:
        """ Returns a random word """
        return random.choice(cls._get_words()).capitalize()

    @classmethod
    def word_list(cls, n: int) -> List[str]:
        """ Returns a list of random words with n length"""
        count: int = 0
        words: List[str] = []
        for i in cls.gen_words():
            if count == n:
                break
            words.append(i)
            count += 1
        return words

    @classmethod
    def words(cls, n: int, sep: Optional[str] = None) -> str:
        """ Returns a string of n words """
        words = cls.word_list(n)
        return sep or " ".join(words).capitalize()

    @classmethod
    def sentence(cls,
                 min_words: Optional[int] = 15,
                 max_words: Optional[int] = 25,
                 sep: Optional[str] = ".") -> str:
        """ Returns a sentence """
        slen = random.randrange(min_words, max_words)
        return " ".join(cls.word_list(slen)).capitalize() + sep

    @classmethod
    def sentences(cls, n: int, sep: Optional[str] = ".") -> str:
        """ Returns a string of n sentences """
        sentences = [cls.sentence(sep=sep) for i in range(n)]
        return " ".join(sentences)

    @classmethod
    def paragraph(cls,
                  min_sentences: Optional[int] = 3,
                  max_sentences: Optional[int] = 8) -> str:
        """ Returns a paragraph """
        plen = random.randrange(min_sentences, max_sentences)
        sentences = cls.sentences(plen)
        return sentences

    @classmethod
    def paragraphs(cls, n: int) -> str:
        """ Returns a string of n paragraphs """
        paragraphs = [cls.paragraph() for i in range(n)]
        return "\n\n".join(paragraphs)
