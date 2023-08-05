MASK_TOKEN = "[MASK]"


class LexSubExample:
    """
    Takes the context (i.e.) the sentence and the position of the word to be replaced
    similar to the way SEMEVAL data is provided
    creates another field with the actual word
    ex. the wine was 'strong' for me.

    context :the wine was strong for me
    ix: 3
    target: strong
    """

    def __init__(self, context: str,
                 word_pos: int,
                 key: str = None,
                 idx: str = None):

        self.key = key
        self.id = idx
        self.context = context
        self.word_pos = word_pos

        # self.masked_tokens = CustomTokenizer(text=context, clean=False).tokens[:-1]
        text = context.lower()
        text = text.split(" ")
        self.masked_tokens = text[:-1]

        self.target_word = self.masked_tokens[word_pos]
        self.masked_tokens[word_pos] = MASK_TOKEN


class Candidate:
    def __init__(self, token: str,
                 lm_score: float = 0.0,
                 word_sim: float = 0.0,
                 wt_lm_score: float = 1.4,
                 wt_word_sim: float = 1.0):
        self.token = token
        self.wt_lm_score = wt_lm_score
        self.wt_word_sim_score = wt_word_sim

        self.lm_score = lm_score
        self.static_word_sim = word_sim

    # Define your scoring function below
    @property
    def ranking_score(self):
        return self.wt_lm_score * self.lm_score \
               + self.wt_word_sim_score * self.static_word_sim

