import unittest

from pylorem import LoremIpsum


class TestLoremIpsum(unittest.TestCase):

    def test_word(self):

        word = LoremIpsum.word()
        self.assertTrue(len(word) > 1)

    def test_word_list(self):

        words = LoremIpsum.word_list(10)
        self.assertTrue(len(words) == 10)

    def test_words_5(self):

        c = 5
        words = LoremIpsum.words(c)
        self.assertTrue(len(words.split(" ")) == c)

    def test_words_100(self):

        c = 100
        words = LoremIpsum.words(c)
        self.assertTrue(len(words.split(" ")) == c)

    def test_words_1000(self):

        c = 1000
        words = LoremIpsum.words(c)
        self.assertTrue(len(words.split(" ")) == c)

    def test_words_5000(self):

        c = 5000
        words = LoremIpsum.words(c)
        self.assertTrue(len(words.split(" ")) == c)

    def test_sentence(self):

        s = LoremIpsum.sentence()
        self.assertTrue(15 <= len(s.split(" ")) <= 25)

    def test_sentences(self):

        s = LoremIpsum.sentences(5)
        self.assertEqual(len(s.split(". ")), 5)

    def test_paragraph(self):

        # TODO: Add test
        p = LoremIpsum.paragraph()

    def test_paragraphs(self):

        # TODO: Add test
        p = LoremIpsum.paragraphs(5)
