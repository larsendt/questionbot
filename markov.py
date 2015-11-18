import random
from collections import defaultdict
import basic_logger

L = basic_logger.Logger("MarkovChain")

class MarkovChain(object):
    def __init__(self, corpus):
        self._model = self._build_model(corpus)

    def _build_model(self, corpus):
        words = corpus.split()
        model = defaultdict(list)
        for i in xrange(len(words)):
            if i == 0:
                continue

            cur_word = words[i]
            context = words[i-1]
            model[context].append(cur_word)

        return model

    def get_random_start(self):
        choice = random.choice(self._model.keys())
        for i in range(100):
            if choice.endswith(".") or not (ord("A") <= ord(choice[0]) <= ord("Z")):
                choice = random.choice(self._model.keys())
            else:
                break
        return choice

    def get_word(self, context):
        if context in self._model:
            return random.choice(self._model[context])
        else:
            return self.get_random_start()
    


