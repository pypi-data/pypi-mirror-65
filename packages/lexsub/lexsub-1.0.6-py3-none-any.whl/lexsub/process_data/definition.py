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

