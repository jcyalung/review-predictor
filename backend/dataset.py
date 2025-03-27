import os                               # reading files
import re                               # regex
import requests
from bs4 import BeautifulSoup


TRAINING_PATH = '/Users/jcyalung/Documents/review-predictor/backend/aclImdb/train'
TESTING_PATH = '/Users/jcyalung/Documents/review-predictor/backend/aclImdb/test'
IMDB = r'^https:\/\/www\.imdb\.com\/.*$'

MOVIE_LINK = 'https://www.imdb.com/review/rw10325949/?ref_=tt_ururv_perm'
EPISODE_LINK = 'https://www.imdb.com/review/rw7363919/?ref_=tt_ururv_perm'
TV_LINK = 'https://www.imdb.com/review/rw8266882/?ref_=tt_ururv_perm'
NEUTRAL_LINK = 'https://www.imdb.com/review/rw10324876/?ref_=tt_ururv_perm'

def clean_html(review) -> str:
    review = review.replace('\n', ' ')
    review = re.sub(r'<br\s*/?>', '\n', review)  # removes <br> and <br />
    review = re.sub(r'<.*?>', '', review)      # removes any HTML tags
    return review

def get_review(url) -> tuple | None:
    try:
        user, media_name, rating, score, episode_name = None, None, None, None, None
        if not re.match(IMDB, url):
            raise Exception('Not an IMDB link!')
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.text)
        # parse 
        soup = BeautifulSoup(response.text, 'html.parser')
        # title and user html
        title_html = soup.find_all('div', class_='subpage_title_block')[0].find_all('a')
        user, media_name = title_html[0].text, title_html[1].text
        
        # cross check title html
        subtitle_html = soup.find_all('div', class_='lister-item-header')[0].find_all('a')[0]
        subtitle = subtitle_html.text
        
        # check if rating an episode, not the tv series/movie
        if not media_name == subtitle:
            episode_name = media_name
            media_name = subtitle[1:-1]
        # rating html
        rating_html = soup.find_all('span', class_='rating-other-user-rating')
        if len(rating_html) == 0:
            raise Exception("Invalid link.")
        score = int(rating_html[0].find_all('span')[0].text)
        review = soup.find_all('div', class_='text show-more__control')[0].text
        review = clean_html(review)
        score = 'negative' if score <= 4 else 'positive' if score >= 7 else score
        if type(score) == int:
            raise Exception('Rating is a neutral rating.')
        return (url, user, media_name, episode_name, score, review)
    except Exception as e:
        print(e)
        return None

# gets words of a specific review
def get_words(review : str):
    review = re.sub(r'<br\s*/?>', ' ', review)

    review = re.sub(r"[^a-zA-Z0-9']+", ' ', review)

    words = review.strip().lower().split()

    # Remove the word 'br' explicitly
    words = [word for word in words if word != 'br']
    
    return words

# just needs to be run once
# migrated to sqlite database
def get_data():
    data = []
    
    train_folder_neg = TRAINING_PATH + '/neg'
    train_folder_pos = TRAINING_PATH + '/pos'
    
    test_folder_neg = TESTING_PATH + '/neg'
    test_folder_pos = TESTING_PATH + '/pos'
    # add all training reviews to our train_data array
    for positive_path, negative_path in zip(os.listdir(train_folder_pos), os.listdir(train_folder_neg)):
        with \
        open(os.path.join(train_folder_pos, positive_path), 'r') as positive_file, \
        open(os.path.join(train_folder_neg, negative_path), 'r') as negative_file:
            pos_review = positive_file.read().strip()
            pos_review = clean_html(pos_review)
            neg_review = negative_file.read().strip()
            neg_review = clean_html(neg_review)
            data.append((pos_review, 'positive'))
            data.append((neg_review, 'negative'))
        
    # add all negative training reviews to our train_data array
    for positive_path, negative_path in zip(os.listdir(test_folder_pos), os.listdir(test_folder_neg)):
        with \
        open(os.path.join(test_folder_pos, positive_path), 'r') as positive_file, \
        open(os.path.join(test_folder_neg, negative_path), 'r') as negative_file:
            pos_review = positive_file.read().strip()
            pos_review = clean_html(pos_review)
            neg_review = negative_file.read().strip()
            neg_review = clean_html(neg_review)
            
            data.append((pos_review, 'positive'))
            data.append((neg_review, 'negative'))
    
    # split into labels and reviews
    reviews, labels = zip(*data)
    
    return reviews, labels

get_review('https://www.imdb.com/review/rw10056060/?ref_=tt_ururv_perm')