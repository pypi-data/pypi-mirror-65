import re
from typing import List, Tuple, Union


def char_ngrams(s: str, n=4) -> List[str]:
    return [s[i:i+n] for i in range(len(s) + 1 - n)]


def jaccard_similarity(s1: set, s2: set) -> float:
    return len(s1 & s2) / len(s1 | s2)


def season_episode(s: str) -> Union[Tuple[int, int], None]:
    m = re.search(r's(\d\d)e(\d\d)', s.lower())
    return (int(m.group(1)), int(m.group(2))) if m else None


def rank(query: str, docs: List[str]) -> List[Tuple[float, str]]:
    boost = 5

    def score(n):
        return lambda doc: jaccard_similarity(
            set(char_ngrams(query.lower(), n)),
            set(char_ngrams(doc.lower(), n))
        )

    s4 = score(4)
    s3 = score(3)
    return sorted([
        ((boost * s4(doc) + s3(doc)) / (boost + 1), doc)
        for doc in docs
    ],
        reverse=True
    )


def matching(queries: List[str], docs: List[str], sort=False, threshold=0):
    match = [
        (query,) + rank(query, docs)[0]
        for query in queries
    ]

    match = [
        (q, d, s) for q, s, d in match
        if s >= threshold
    ]

    return match if not sort else sorted(match, reverse=True)
