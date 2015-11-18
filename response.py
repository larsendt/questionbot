import corpus
import markov
import basic_logger
import re

L = basic_logger.Logger("response")

def is_question(message):
    return "?" in message

def is_christmas(message):
    msg = message.lower()
    return " santa " in msg or " christmas " in msg or " holiday " in msg

def add_christmas(message):
    return ":sexysanta:" + message + ":sexysanta:"

def make_response(message):
    L.info("Query '%s'" % message)

    if not is_question(message):
        L.info("Didn't ask a question")
        return "Ask me a question, you groot!"

    #c = corpus.WikipediaCorpus(message)
    c = corpus.BlogspotCorpus(message)
    chain = markov.MarkovChain(c.corpus())

    sentence_list = []
    cur_word = chain.get_random_start()
    sentence_list.append(cur_word)
    for i in range(100):
        cur_word = chain.get_word(cur_word)
        sentence_list.append(cur_word)
        if cur_word.endswith("."):
            break
    reply = " ".join(sentence_list)
    L.info("Reply: '%s'" % reply)
    
    if is_christmas(message):
        return add_christmas(reply)
    else:
        return reply
