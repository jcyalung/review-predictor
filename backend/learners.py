import numpy as np
import matplotlib.pyplot as plt
import dataset as db
from sqlite_helpers import imdb_reviews
import time
import io
import base64
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


reviews, labels, _ = zip(*imdb_reviews('imdbReviews.db'))
train_reviews, test_reviews, train_labels, test_labels = train_test_split(
        reviews, labels, train_size=SPLIT, random_state=42, stratify=labels
    )
vectorizer = TfidfVectorizer(stop_words='english',max_df=MAX_DF,min_df=MIN_DF, ngram_range=NGRAM_RANGE)

# models
nb = MultinomialNB()
svm = LinearSVC()
log_reg = LogisticRegression()

models = {'nb': nb, 'svm': svm, 'log_reg': log_reg}

def recorder(func):
    def wrapper():
        start_time = time.perf_counter()
        output = func()
        end_time = time.perf_counter()
        execution = end_time - start_time
        print(f'Time taken to run {func.__name__}: {execution:.4f} seconds')
        return output
    return wrapper
    


def train_models():
    start = time.perf_counter()
    global train_reviews, train_labels, test_reviews, test_labels
    global models, vectorizer
    scores = []
    features_train = vectorizer.fit_transform(train_reviews)
    features_test = vectorizer.transform(test_reviews)
    for type, model in models.items():
        model.fit(features_train, train_labels)
        preds = model.predict(features_test)
        scores.append((type, accuracy_score(preds, test_labels)))
    end = time.perf_counter()
    exec = end - start
    print(f'Time taken to train models: {exec:.4f} seconds')
    return scores


def predict_review(review, model_type):
    try: 
        if not hasattr(vectorizer, 'vocabulary_'):
            train_models()
        start = time.perf_counter()
        model = models[model_type]
        review, label = review
        review_vectorized = vectorizer.transform([review])
        
        result = model.predict(review_vectorized)[0]
        end = time.perf_counter()
        exec = end - start
        print(f'Time taken to predict: {exec:.4f} seconds')
        return result, label
    except Exception as e:
        print(e)
        return None, None

def matrix(true, pred):
    conf = confusion_matrix(true, pred)
    plt.figure(figsize=(5,4))
    plt.title('Confusion Matrix for Predictions')
    plt.xlabel('Predicted Labels')
    plt.ylabel('Actual Labels')
    plt.imshow(conf, interpolation='nearest', cmap='Blues') 
    for i in range(conf.shape[0]):
        for j in range(conf.shape[1]):
            plt.text(j, i, str(conf[i, j]), ha='center', va='center', color='black')
    plt.colorbar()        
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    return img
    
if '__main__' == __name__:
    start = time.perf_counter()
    train_models()
    end = time.perf_counter()
    print(f'Time taken: {end-start} seconds')