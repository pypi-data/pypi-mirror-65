from lexsub.process_data.definition import Candidate
from lexsub.algorithms.custom_utils import LexSubUtils
import torch
from typing import List

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class BERTLexSub:
    def __init__(self, example,
                 model_class=None,
                 masked_lm=None,
                 tokenizer=None,
                 k: int = 20,
                 feasible_set=None):
        if feasible_set is None:
            feasible_set = []

        self.example = example
        self.model_class = model_class
        self.masked_lm = masked_lm
        self.tokenizer = tokenizer
        self.no_of_candidates = k
        self.feasible_set = feasible_set

    def masked_lm_prediction(self) -> List[Candidate]:
        indexed_text = self.tokenizer.convert_tokens_to_ids(self.example.masked_tokens)
        indexed_text = self.tokenizer.build_inputs_with_special_tokens(token_ids_0=indexed_text)
        tokens_tensor = torch.tensor([indexed_text]).to(DEVICE)
        self.example.word_pos = self.example.word_pos + 1

        with torch.no_grad():
            if self.model_class == 'BertModel':
                segment_ix = len(indexed_text) * [0]
                segments_tensor = torch.tensor([segment_ix]).to(DEVICE)
                model_op = self.masked_lm(tokens_tensor, segments_tensor)
            else:
                model_op = self.masked_lm(tokens_tensor)

            predictions = model_op[0]
            preds = predictions[0, self.example.word_pos]
            candidates = LexSubUtils().custom_top_k(t=preds,
                                                    k=self.no_of_candidates,
                                                    valid_set=self.feasible_set,
                                                    tokenizer=self.tokenizer,
                                                    target_word=self.example.target_word)
        return candidates

    def _get_bert_sentence_emebedding(self):
        raise NotImplementedError



