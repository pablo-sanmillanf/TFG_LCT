import nltk.tokenize.punkt as pkt


class CustomLanguageVars(pkt.PunktLanguageVars):

    _period_context_fmt = r"""
        \S*                          # some word material
        %(SentEndChars)s             # a potential sentence ending
        \s*                       #  <-- THIS is what I changed
        (?=(?P<after_tok>
            %(NonWord)s              # either other punctuation
            |
            (?P<next_tok>\S+)     #  <-- Normally you would have \s+ here
        ))"""


class SentenceSplitter:
    custom_tknzr = pkt.PunktSentenceTokenizer(lang_vars=CustomLanguageVars())

    # tokenizer = nltk.data.load('file:punkt/english.pickle')
    def split_text(self, text: str) -> list[str]:
        return self.custom_tknzr.tokenize(text)