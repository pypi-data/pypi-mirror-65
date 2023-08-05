import re
from nltk.corpus import stopwords
from string import punctuation


class CustomTokenizer:
    def __init__(self, text: str, clean=True):
        self.tokens = self.get_clean_text(text=text, clean=clean)

    @staticmethod
    def get_clean_text(text, clean=False):
        """ Define your Text Cleaning Rules here
        If clean = False, it basically just
        returns tokenized lower cased sentence """
        text = text.lower()
        if clean:
            stops = set(stopwords.words("english"))
            stops.update(set(punctuation))
            text = re.sub(r"\. \. \.", "\.", text)
            text = re.sub(r"[^A-Za-z0-9(),!?\'\`\.]", " ", text)
            text = re.sub(r'[0-9]+', '', text)
            text = re.sub(r"\'s", " \'s", text)
            text = re.sub(r"\'ve", " \'ve", text)
            text = re.sub(r"n\'t", " n\'t", text)
            text = re.sub(r"\'re", " \'re", text)
            text = re.sub(r"\'d", " \'d", text)
            text = re.sub(r"\'ll", " \'ll", text)
            text = re.sub(r",", "", text)
            text = re.sub(r"!", "", text)
            text = re.sub(r"\(", "", text)
            text = re.sub(r"\)", "", text)
            text = re.sub(r"\?", "", text)
            text = re.sub(r"\s{2,}", " ", text)
            text = re.sub(r"<br />", " ", text)
            text = re.sub(r'[^\w\s]', '', text)

        text = text.split(" ")
        if clean:
            text = [w for w in text if w not in stops]

        return text
