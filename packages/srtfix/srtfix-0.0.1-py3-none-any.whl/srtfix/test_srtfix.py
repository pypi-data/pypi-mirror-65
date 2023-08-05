from srtfix.srtfix import *
from pathlib import Path


def test_p2s():
    assert p2s([Path('.'), Path('..')], [Path('...')]) == ['.', '..', '...']


def test_vid_2_srt():
    srt = vid_2_srt('Sudden Prejudice.1980.720p.BluRay.x264-[YTS.LT].mp4')
    assert str(srt) == 'Sudden Prejudice.1980.720p.BluRay.x264-[YTS.LT].srt'
