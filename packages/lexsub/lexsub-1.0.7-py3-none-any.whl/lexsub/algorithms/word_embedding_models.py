from typing import Dict
import time
import numpy as np

from lexsub.process_data.indexer import Indexer

# define special symbols to handle padding etc
UNK_TOKEN = "[UNK]"    # unknown token
PAD_TOKEN = "[PAD]"    # padding
BOS_TOKEN = "[CLS]"    # Beginning of sentence token
EOS_TOKEN = "[SEP]"    # End of sentence token
MASK_TOKEN = "[MASK]"  # Mask Token

class EmbeddingLookup:
    def __init__(self,
                 embed_file: str,
                 emb_dim = 300,
                 word_ix: Indexer = Indexer()):
        self.embedding_filename = embed_file
        self.emb_dim = emb_dim
        self.word_ix = word_ix
        self.ix2embed, self.word_ix = \
            self._load_and_index_word_embedding(embedding_file=self.embedding_filename, word_ix=self.word_ix)

    def _load_and_index_word_embedding(self, embedding_file, word_ix: Indexer) -> [Dict, Indexer]:
        """
        Read a GloVe txt file.
        Returns:
        1. a dictionary mapping index to embedding vector(index_to_embedding),
        2. an indexer of all the words in the lookup (word_to_index + index_to_word)
        Also, appropriately initializes UNK, BOS, EOS, PAD embeddings
        word <-> index -> embedding
        """
        print("Processing Embedding File:  ", embedding_file)
        t = time.time()
        index_to_embedding = {}

        # Read embedding File and update the word_ix:[ word2ix, ix2word ] and ix2embed for all words
        embeds = open(embedding_file, encoding='iso8859')
        for line in embeds:
            split = line.split(' ')
            word = split[0]
            representation = split[1:]
            representation = np.array([float(val) for val in representation])
            ix = word_ix.add_and_get_index(word)
            index_to_embedding[ix] = representation
        embeds.close()

        # create empty representation for unknown words.
        _UNK_ix = word_ix.add_and_get_index(UNK_TOKEN)
        _PAD_ix = word_ix.add_and_get_index(PAD_TOKEN)
        _BOS_ix = word_ix.add_and_get_index(BOS_TOKEN)
        _EOS_ix = word_ix.add_and_get_index(EOS_TOKEN)
        _MASK_ix = word_ix.add_and_get_index(MASK_TOKEN)

        index_to_embedding[_UNK_ix] = [0.0] * self.emb_dim
        index_to_embedding[_PAD_ix] = [0.0] * self.emb_dim
        index_to_embedding[_BOS_ix] = [999] * self.emb_dim
        index_to_embedding[_EOS_ix] = [-999] * self.emb_dim
        index_to_embedding[_MASK_ix] = [0.0] * self.emb_dim

        print("Done Processing Embedding File")
        print("Time Taken for embedding dict creation: {}".format(time.time()-t))
        return index_to_embedding, word_ix

    def get_word_embedding(self, word) -> np.array:
        """
        Given a word returns the corresponding embedding vector of dim = embed_dim (ex. 300)
        if word in glove else return UNK representation which is vector of zeros by design
        Returns: The embedding vector of the query word
        """
        word = word.lower()
        ix = self.word_ix.add_and_get_index(word) if self.word_ix.contains(word) \
            else self.word_ix.add_and_get_index(UNK_TOKEN)

        return self.ix2embed[ix]

    def get_similarity_score(self, vec_1: np.array, vec_2: np.array, measure: str = 'cosine') -> float:
        if measure == 'l2':
            return self.euclidean_dist(vec_1=vec_1, vec_2=vec_2)
        elif measure == 'cosine':
            return self.cosine_sim(vec_1=vec_1, vec_2=vec_2)
        elif measure == 'wmd':
            return self.wmd(vec1=vec_1, vec2=vec_2)
        else:
            raise NotImplementedError

    @staticmethod
    def euclidean_dist(vec_1: np.array, vec_2: np.array) -> float:
        return np.square(np.linalg.norm(vec_1 - vec_2))

    @staticmethod
    def cosine_sim(vec_1: np.array, vec_2: np.array) -> float:
        dot = np.dot(vec_1, vec_2)
        norm_u = np.sqrt(np.sum(vec_1 ** 2))
        norm_v = np.sqrt(np.sum(vec_2 ** 2))
        cosine_similarity = dot / np.dot(norm_u, norm_v)

        return cosine_similarity

    @staticmethod
    def wmd(vec1: np.array, vec2: np.array) -> float:
        raise NotImplementedError
