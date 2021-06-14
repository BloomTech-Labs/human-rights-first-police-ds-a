from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

# nltk.download('punkt')


class TagMaker:
    """
    This class takes a string text and a list of tags and can return
    a dictionary of word stems for each tag in the tag list as well
    as a list of words found in the text that match the tag list.
    Any text can be searched for any version of words in the tag
    list.

    This class takes a text string and a list of possible tags.
    With this, a dictionary of tags with their words stems for keys
    and the original tag for values is created. The text input gets
    converted into stems and checked  for matches in the tag
    dictionary. A list of matching tags can be returned.

    KNOWN LIMITATIONS:
    Multi-word tags are created regardless of word order. This
    can lead to non-correlated words in text becoming a single tag.

    Abstract ideas can be described by many tags and are hard to define
    so they can easily be missed by this simple word stem matcher.

    There is a 1 for 1 relationship between tags and their stems.
    This class does not account for multiple word stems that
    share similar meaning.

    This class was created using a pre-made nltk library. Any
    slang, misspelled words, or colloquialism will likely be missed.
    """

    def __init__(self, text, tag_list):
        self.text = " ".join(text.split("-"))
        self.tag_list = tag_list

    def tag_dict(self):
        """
        This function will take the tag list and create a
        dictionary with word stems for keys. This is to increase
        efficiency of word lookups while text matching.

        :return: Dictionary with word stems for keys and
        original tags as values
        """
        ps = PorterStemmer()
        tag_dict = {}

        for category in self.tag_list:
            # multi-word tags have to be tokenized by word
            if len(category.split()) > 1:
                phrase = []
                for word in category.split():
                    phrase.append(ps.stem(word))
                if str(" ".join(phrase)) not in tag_dict.keys():
                    tag_dict[str(" ".join(phrase))] = category

            else:
                tag_dict[ps.stem(category)] = category

        return tag_dict

    def tags(self):
        """
        This function takes a string text, tokenizes the
        words, and checks the stems of these words for matches
        in the tag dictionary created within the same class.
        Any matches are appended to a list of tags.
        :return: List of tags that are found in both the
        text and the tag dictionary
        """
        ps = PorterStemmer()
        tag_dict = self.tag_dict()
        tags = []
        words = word_tokenize(self.text)

        # used later to check for multi-word tags
        multi_words = []

        for w in words:
            if ps.stem(w) in tag_dict:
                if tag_dict[ps.stem(w)] not in tags:
                    tags.append(tag_dict[ps.stem(w)])

            multi_words.append(ps.stem(w))

        # check for multi-word tags
        multi_tags = []

        for tag in self.tag_list:
            if len(tag.split()) > 1:
                multi_tok = word_tokenize(tag)
                phrase = []
                for word in multi_tok:
                    phrase.append(ps.stem(word))
                    if phrase not in multi_tags:
                        multi_tags.append(phrase)

        for multi in multi_tags:
            if all(elem in multi_words for elem in multi):
                if tag_dict[str(" ".join(multi))] not in tags:
                    tags.append(tag_dict[str(" ".join(multi))])

        return sorted(tags)
