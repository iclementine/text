import unittest
import pytest
import sys

from pytext import data
from pytext.datasets import TREC


class TestSubword(unittest.TestCase):
    @pytest.mark.skipif(sys.version_info < (3, 0),
                        reason="revtok currently breaks for python 2.7")
    def test_subword_trec(self):
        TEXT = data.SubwordField()
        LABEL = data.Field(sequential=False)
        RAW = data.Field(sequential=False, use_vocab=False)
        raw, _ = TREC.splits(RAW, LABEL)
        cooked, _ = TREC.splits(TEXT, LABEL)
        LABEL.build_vocab(cooked)
        TEXT.build_vocab(cooked, max_size=100)
        TEXT.segment(cooked)
        print(cooked[0].text)
        batch = next(iter(data.Iterator(cooked, 1, shuffle=False)))
        self.assertEqual(TEXT.reverse(batch.text.data)[0], raw[0].text)


if __name__ == '__main__':
    unittest.main()
