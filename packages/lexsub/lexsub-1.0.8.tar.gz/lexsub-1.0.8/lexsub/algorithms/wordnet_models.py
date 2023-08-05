from nltk.corpus import wordnet
from typing import List
import re


class WordNetRaw:
    def __init__(self, word):
        self.word = word
        self.syns = self._get_syn_wordnet()

    def _get_syn_wordnet(self) -> List:
        """ Returns a List of synonyms to the given word from Wordnet """
        candidates = []
        syn_sets = wordnet.synsets(self.word)
        for syn_set in syn_sets:
            # new_candidates = syn_set._lemma_names
            candidates.extend(syn_set._lemma_names)
        candidates = list(set(candidates))
        for ix in range(0, len(candidates)):
            item = candidates[ix]
            item = re.sub(r"_", " ", item)
            if item != self.word:
                candidates[ix] = item
        return candidates

    def suggest_candidates(self):
        raise NotImplementedError


def run_wordnet(test):
    """We use wordnet to look up dictionary synonyms and return the top k as the best candidate """
    predicted_candidates = WordNetRaw(word=test.target).syns
    wordnet_replacement = predicted_candidates[0]
    # print("wordnet replacement for {} in the sentence {} is : {}".format(test.target, test, wordnet_replacement))

