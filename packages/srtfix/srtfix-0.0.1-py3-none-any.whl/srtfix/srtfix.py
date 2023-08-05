import argparse
import os

from pathlib import Path
from typing import List
from typing import Iterable, List

from termcolor import colored

from srtfix.text import matching


def p2s(*pathss: Iterable[Path]) -> List[str]:
    return sum([[
        str(path)
        for paths in pathss
        for path in paths
    ]], [])


def vid_2_srt(vid: str) -> str:
    return str(Path(vid).with_suffix('.srt'))


def get_srts(path: str):
    return p2s(Path(path).glob('*.srt'))


def get_vids(path: str):
    p = Path(path)
    return p2s(
        p.glob('*.mkv'),
        p.glob('*.mp4'),
        p.glob('*.avi'),
    )


def rename(srts: List[str], vids: List[str]):
    ms = matching(srts, vids, threshold=0.2)

    dont_have = set(vids) - set(d for q, d, _ in ms)

    print(colored('Couldn\'t find subtitles for the following`', 'yellow'))
    for v in dont_have:
        print(v)

    m = [
        (q, vid_2_srt(d))
        for q, d, _ in ms
    ]

    m = [(q, d) for q, d in m if q != d]

    if not m:
        print(colored('No srts were found', 'green'))
        return

    print(colored('Found the following matches:', 'green'))
    print()
    for q, d in m:
        print(
            colored(q, 'yellow'),
            colored(d, 'blue'),
            '',
            sep='\n'
        )

    print()
    choice = input(colored('Rename?[Y/n]', 'red'))
    if choice == 'n':
        return

    for q, d in m:
        os.rename(q, d)


def main():
    argparse.ArgumentParser(
        description='managing media files the right way'
    )

    srts = get_srts('.')
    vids = get_vids('.')
    rename(list(srts), list(vids))
