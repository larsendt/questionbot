import pygoogle
import wikipedia
import random
import re
from collections import defaultdict
import cache
import basic_logger

L = basic_logger.Logger("markov")

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
    
def clean_corpus(text):
    header_re = "=?==[\w\s]+===?"
    sections = re.split(header_re, text)
    headers = re.findall(header_re, text)
    corpus = ""
    for header, section in zip(headers, sections):
        if header not in ["== References ==", "== Further reading ==", "== External links =="]:
            corpus += " " + section
    corpus = corpus.replace("\n", " ")
    corpus = re.sub("= =", " ", corpus)
    corpus = re.sub("\s+", " ", corpus)
    return corpus

def clean_query(query):
    return re.sub("[.,-\/#!$%\^&\*;:{}=\-_`~()]", "", query)

def results_are_acceptable(search_results, query):
    """ Idea for this function: Wikipedia sometimes returns totally unrelated
        pages, so do some sort of Hamming distance on the results and the
        query to see if they're related enough to be acceptable."""
    return len(search_results) > 0

@cache.disk_cache
def create_corpus(message):
    pages = wikipedia.search(message)
    if results_are_acceptable(pages, message):
        try:
            page = wikipedia.page(pages[0])
            L.info("Using page for %s" % pages[0])
        except wikipedia.DisambiguationError as e:
            page = wikipedia.page(e.options[0])
            L.info("After disambiguation, using page for %s" % e.options[0])
    else:
        L.info("No acceptable page for query, using Groot")
        page = wikipedia.page("Groot")

    return clean_corpus(page.content)

def make_response(message):
    if "?" not in message:
        L.info("Didn't ask a question")
        return "Ask me a question, you groot!"
    query = clean_query(message)
    L.info("Query '%s'" % query)
    corpus = create_corpus(query)
    chain = MarkovChain(corpus)
    sentence_list = []
    cur_word = chain.get_random_start()
    sentence_list.append(cur_word)
    while not cur_word.endswith("."):
        cur_word = chain.get_word(cur_word)
        sentence_list.append(cur_word)
    reply = " ".join(sentence_list)
    L.info("Reply: '%s'" % reply)
    return reply
