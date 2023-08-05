import pkg_resources
import numpy as np


class TextBasedStopwords:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = np.loadtxt(
            data_file, dtype=np.unicode, comments=None, encoding=None
        ).tolist()

    def __call__(self, token):
        return token not in self.data


_stopwords_baidu_file = pkg_resources.resource_filename(
    __name__, "data/stopwords_baidu.txt"
)
stopwords_baidu = TextBasedStopwords(_stopwords_baidu_file)
