from sklearn.feature_extraction.text import TfidfVectorizer


def test_vectorizer_fit_only_on_train_vocab():
    train = ["a a a", "b b"]
    test = ["c c c"]  # token appears only in test
    vec = TfidfVectorizer()
    vec.fit(train)
    assert "c" not in vec.vocabulary_