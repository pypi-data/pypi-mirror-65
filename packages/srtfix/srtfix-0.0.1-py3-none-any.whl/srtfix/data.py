from typing import List
import random

format = [
    'WEB-DL',
    'DVDRip',
    'CAMRIP',
    'DVDRIP',
    'HDTS',
    'HDTV',
    'XviD',
    'AC3',
]


years = [str(y) for y in range(2000, 2020)]

titles = [
    ['Sudden', 'Prejudice'],
    ['Triple', 'Assassination'],
    ['Fist', 'of', 'Honor'],
]


class TitleGenerator:
    def __init__(self, title: List[str]):
        self.title = title

    def _get_noise(self):
        return []

    def get_title(self, ext: str = 'mkv'):
        noise = self._get_noise()
        random.shuffle(noise)
        return '.'.join(self.title + noise + [ext])


class Movie(TitleGenerator):
    def _get_noise(self):
        return [
            random.choice(format),
            random.choice(years)
        ]


class Episode(TitleGenerator):
    def __init__(self, title: List[str], s: int = 1, e: int = 1) -> None:
        self.s = s
        self.e = e
        super().__init__(title)

    def _get_noise(self):
        return [
            random.choice(format),
            random.choice(years),
            f's{self.s:02}e{self.e:02}'
        ]


movies = [Movie(title) for title in titles]
episodes = [Episode(title) for title in titles]

print(*[m.get_title() for m in movies], sep='\n')
print(*[e.get_title() for e in episodes], sep='\n')
