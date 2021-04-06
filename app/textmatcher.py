"""
TextMatcher Class: Trains a model based on keywords from training_data.py.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import spacy


class TextMatcher:
    """ Generic NLP Text Matching Model 
    Example:
    Model is instantiated using...
    `model = TextMatcher(training_data)`

    Then the model can make predictions using...
    `prediction = model(text)`

    This will return a police brutality rank 1-5.

    *** TRAINING DATA NEEDS BE FORMATTED IN THE SAME FORMAT AS training_data.py
    """
    class Tokenizer:
        """ Standard SpaCy Tokenizer """

        nlp = spacy.load('en_core_web_sm')

        def __call__(self, text: str) -> list:
            return [
                token.lemma_ for token in self.nlp(text)
                if not token.is_stop and not token.is_punct
            ]

    def __init__(self, train_data: dict, ngram_range=(1, 3), max_features=8000):
        """ Model training on live data at init """
        self.lookup = {k: ' '.join(v) for k, v in train_data.items()}
        self.name_index = list(self.lookup.keys())
        self.tfidf = TfidfVectorizer(
            ngram_range=ngram_range,
            tokenizer=self.Tokenizer(),
            max_features=max_features,
        )
        self.knn = NearestNeighbors(
            n_neighbors=1,
            n_jobs=-1,
        ).fit(self.tfidf.fit_transform(self.lookup.values()).todense())
        self.baseline, _ = self._worker('')

    def _worker(self, user_input: str):
        """ Prediction worker method - internal only """
        vec = self.tfidf.transform([user_input]).todense()
        return (itm[0][0] for itm in self.knn.kneighbors(vec))

    def __call__(self, user_input: str) -> str:
        """ Callable object for making predictions """
        dist, idx = self._worker(user_input)
        if dist != self.baseline:
            return self.name_index[int(idx)]
        else:
            return 'Rank 0 - No Police Presence'
