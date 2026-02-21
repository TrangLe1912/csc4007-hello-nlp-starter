from sklearn.feature_extraction.text import TfidfVectorizer


def test_empty_string_ok():
    vec = TfidfVectorizer()
    X = vec.fit_transform(["xin chao", ""])
    assert X.shape[0] == 2


def test_weird_chars_ok():
    vec = TfidfVectorizer()
    X = vec.fit_transform(["😄!!!", "###@@@ ???"])
    assert X.shape[0] == 2