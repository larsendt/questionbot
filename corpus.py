import requests
import re
import cache
import basic_logger
import pygoogle
import wikipedia

class WikipediaCorpus(object):
    def __init__(self, query):
        self.l = basic_logger.Logger("WikipediaCorpus")
        self._query = self._clean_query(query)
        self._corpus = self._create_corpus(self._query)

    def _clean_query(self, query):
        return re.sub("[.,-\/#!$%\^&\*;:{}=\-_`~()]", "", query)

    def _clean_corpus(self, text):
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

    def _results_are_acceptable(self, search_results, query):
        """ Idea for this function: Wikipedia sometimes returns totally unrelated
            pages, so do some sort of Hamming distance on the results and the
            query to see if they're related enough to be acceptable."""
        return len(search_results) > 0

    def _create_corpus(self, query):
        @cache.disk_cache
        def _internal_fetch(query):
            pages = wikipedia.search(query)
            if self._results_are_acceptable(pages, query):
                try:
                    page = wikipedia.page(pages[0])
                    self.l.info("Using page for %s" % pages[0])
                except wikipedia.DisambiguationError as e:
                    page = wikipedia.page(e.options[0])
                    self.l.info("After disambiguation, using page for %s" % e.options[0])
            else:
                self.l.info("No acceptable page for query, using Groot")
                page = wikipedia.page("Groot")

            return self._clean_corpus(page.content)
        
        return _internal_fetch(query)

    def corpus(self):
        return self._corpus
