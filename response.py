import corpus
import markov
import basic_logger
import re

L = basic_logger.Logger("response")

def is_question(message):
    return "?" in message

def make_response(message):
    L.info("Query '%s'" % message)

    if not is_question(message):
        L.info("Didn't ask a question")
        return "Ask me a question, you groot!"

    wiki = corpus.WikipediaCorpus(message)
    chain = markov.MarkovChain(wiki.corpus())

    sentence_list = []
    cur_word = chain.get_random_start()
    sentence_list.append(cur_word)
    while not cur_word.endswith("."):
        cur_word = chain.get_word(cur_word)
        sentence_list.append(cur_word)
    reply = " ".join(sentence_list)
    L.info("Reply: '%s'" % reply)
    return reply
