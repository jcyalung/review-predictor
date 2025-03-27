import numpy as np
import matplotlib.pyplot as plt
import dataset as db
import imdb
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import VotingClassifier, StackingClassifier

MAX_DF = 0.95
MIN_DF = 2
NGRAM_RANGE = (1,3)
SPLIT = 0.8


reviews, labels = imdb.reviews_and_labels()
train_reviews, test_reviews, train_labels, test_labels = train_test_split(
        reviews, labels, train_size=SPLIT, random_state=42, stratify=labels
    )
vectorizer = TfidfVectorizer(stop_words='english',max_df=MAX_DF,min_df=MIN_DF, ngram_range=NGRAM_RANGE)

# models
nb = MultinomialNB()
svm = LinearSVC()
log_reg = LogisticRegression()

models = {'nb': nb, 'svm': svm, 'log_reg': log_reg}


# im dumb
def process_data():
    print('Processing data')
    
def train_models():
    global train_reviews, train_labels, test_reviews, test_labels
    global models, vectorizer
    scores = []
    features_train = vectorizer.fit_transform(train_reviews)
    features_test = vectorizer.transform(test_reviews)
    for type, model in models.items():
        model.fit(features_train, train_labels)
        preds = model.predict(features_test)
        scores.append((type, accuracy_score(preds, test_labels)))
    print('Models Trained!')

    return scores


def predict_review(review, model_type):
    if train_reviews is None or train_labels is None \
        or test_reviews is None or test_labels is None:
        process_data()
    try: 
        if not hasattr(vectorizer, 'vocabulary_'):
            train_models()
        model = models[model_type]
        review, label = review
        review_vectorized = vectorizer.transform([review])
        
        result = model.predict(review_vectorized)[0]
        return result, label
    except Exception as e:
        print(e)
        return None, None


if '__main__' == __name__:
    start = time.perf_counter()
    train_models()
    end = time.perf_counter()
    print(f'Time taken: {end-start} seconds')