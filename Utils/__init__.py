import os
from .KeywordGenerator import KeywordGenerator

BASEDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
SAVEDIR = os.path.join(BASEDIR, 'Files/')
TRIPLE_AD_URL = 'https://triplead-panel.pagez.kr'
SUPPORTED_CRAWLER = ["Huawei", "Baidu", "TFpp"]

__all__ = ['BASEDIR', 'SAVEDIR', 'KeywordGenerator']
