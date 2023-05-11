import nltk.tokenize.punkt as pkt


class CustomLanguageVars(pkt.PunktLanguageVars):
    """
    This custom class splits the sentences and don't remove the "\n" characters.
    """

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
    """
    This class is used to split the text in sentences.
    """
    _custom_tknzr = pkt.PunktSentenceTokenizer(lang_vars=CustomLanguageVars())

    # tokenizer = nltk.data.load('file:punkt/english.pickle')
    def split_text(self, text: str) -> list[str]:
        """
        Split the text in sentences.
        :param text: The text.
        :return: A list with the split sentences.
        """
        return self._custom_tknzr.tokenize(text)
