from srtfix.data import *
from srtfix.text import *


def test_char_ngrams():
    assert char_ngrams('abc', 1) == ['a', 'b', 'c']
    assert char_ngrams('abc', 2) == ['ab', 'bc']
    assert char_ngrams('abc', 3) == ['abc']
    assert char_ngrams('abc', 4) == []


def test_jaccard_similarity():
    assert jaccard_similarity(set([1]), set([1])) == 1
    assert jaccard_similarity(set([1]), set([2])) == 0
    assert jaccard_similarity(set([1, 2, 3]), set([2, 3, 4])) == 1/2


def test_rank():
    _, words = list(zip(
        *rank('abcde', ['fedcba', 'abcdef', 'abcde'])
    ))

    assert words == ('abcde', 'abcdef', 'fedcba')


def test_matching():
    queries = ['abcdef', 'bcdefg']
    docs = ['bcdxefg', 'abcxdef', 'xyz']
    qd = [
        (q, d) for q, d, _ in matching(
            queries,
            docs,
        )
    ]

    assert qd == [(queries[0], docs[1]), (queries[1], docs[0])]


def test_season_episode():
    title = Episode(titles[0], s=1, e=2).get_title()
    print(title)
    assert season_episode(title) == (1, 2)
