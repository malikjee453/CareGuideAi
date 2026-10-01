from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbeddingModel:
    """
    Lightweight local text representation for the first RAG version.

    This keeps deployment simple and does not require a second API key.
    A semantic embedding model can replace this component in Advanced RAG.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
        )

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts)

    def transform(self, texts):
        return self.vectorizer.transform(texts)
