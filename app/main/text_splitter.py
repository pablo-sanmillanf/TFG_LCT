import nltk


class CustomLanguageVars(nltk.tokenize.punkt.PunktLanguageVars):
    """
    This custom class splits the sentences and don't remove the "\n" characters.
    """

    _period_context_fmt = r"""
        \S*                          # some word material
        %(SentEndChars)s             # a potential sentence ending
        \s+                       #  <-- This is what has to be changed to preserve \n chars and white spaces
        (?=(?P<after_tok>
            %(NonWord)s              # either other punctuation
            |
            (?P<next_tok>\S+)     #  <-- Normally you would have \s+ here
        ))"""


class SentenceSplitter:
    """
    This class is used to split the text in sentences.
    """
    _custom_tknzr = nltk.tokenize.punkt.PunktSentenceTokenizer(lang_vars=CustomLanguageVars())

    # tokenizer = nltk.data.load('file:punkt/english.pickle')
    def split_text(self, text: str) -> list[str]:
        """
        Split the text in sentences.
        :param text: The text.
        :return: A list with the split sentences.
        """
        return self._custom_tknzr.tokenize(text)
