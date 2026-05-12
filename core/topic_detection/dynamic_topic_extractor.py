import re

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from nltk.corpus import stopwords

from core.preprocessing.semantic_cleaner import (
    clean_semantic_text
)


STOP_WORDS = set(stopwords.words("english"))



def extract_dynamic_topics(question_texts,
                           top_k=15):

    cleaned_docs = []

    for text in question_texts:

        cleaned_text = clean_semantic_text(text)

        if len(cleaned_text.strip()) > 10:

            cleaned_docs.append(cleaned_text)
            
    if len(cleaned_docs) == 0:

        return []
        
    vectorizer = TfidfVectorizer(
        stop_words="english",

        ngram_range=(1, 3),

        max_features=100
    )

    tfidf_matrix = vectorizer.fit_transform(
        cleaned_docs
    )

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.sum(axis=0).A1

    topic_scores = list(
        zip(feature_names, scores)
    )

    topic_scores = sorted(
        topic_scores,
        key=lambda x: x[1],
        reverse=True
    )

    extracted_topics = []

    for topic, score in topic_scores:

        if len(topic.split()) > 4:
            continue

        extracted_topics.append(
            {
                "topic": topic,
                "score": round(score, 3)
            }
        )

    return extracted_topics[:top_k]