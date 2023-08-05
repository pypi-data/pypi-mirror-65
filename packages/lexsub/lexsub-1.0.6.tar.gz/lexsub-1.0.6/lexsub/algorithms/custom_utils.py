import torch
from lexsub.process_data.definition import Candidate
from typing import List
from transformers import *
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LexSubUtils:
    def __init__(self):
        pass

    @staticmethod
    def custom_top_k(t: torch.tensor,
                     k: int, tokenizer,
                     valid_set: set = None,
                     target_word: str = None) -> List[Candidate]:
        """
        Extending torch top k method Here we want to do argsort and choose top k
        but with the option to leave out items in the ignore set
        :param target_word:
        :type tokenizer: tokenizer (to convert to token - Ex. BertTokenizer)
        :type valid_set: (Python:set) The set of items valid (feasible set)
        :type t: (Tensor) – the input tensor.
        :type k: (python:int) – the k in “top-k”

        :return: A list of Candidate object with token and score
        """
        candidates = []
        sorted_scores, sorted_indices = torch.sort(t, descending=True)
        for ix, score in zip(sorted_indices, sorted_scores):
            if len(candidates) == k:
                break
            token = tokenizer.convert_ids_to_tokens(ix.item())
            score = score.item()
            if token in valid_set:
                if token != target_word:
                    candidates.append(Candidate(token=token, lm_score=score))

        return candidates

    def fetch_pre_trained(self, model_class: str, pre_trained_wt: str):
        if model_class == 'BertModel':
            tokenizer = BertTokenizer.from_pretrained(pre_trained_wt)
            lm_model = BertForMaskedLM.from_pretrained(pre_trained_wt).to(DEVICE)
            # sentence_encoder = BertModel.from_pretrained(pre_trained_wt).to(DEVICE)
        elif model_class == 'RobertaModel':
            tokenizer = RobertaTokenizer.from_pretrained(pre_trained_wt)
            lm_model = RobertaForMaskedLM.from_pretrained(pre_trained_wt).to(DEVICE)
            # sentence_encoder = RobertaModel.from_pretrained(pre_trained_wt).to(DEVICE)
        else:
            raise NotImplementedError

        lm_model.eval()
        # sentence_encoder.eval()

        return tokenizer, lm_model  # , sentence_encoder
