import os                               # reading files
import re                               # regex
import requests
from bs4 import BeautifulSoup

IMDB = r'^https:\/\/www\.imdb\.com\/.*$'

MOVIE_LINK = 'https://www.imdb.com/review/rw10325949/?ref_=tt_ururv_perm'
EPISODE_LINK = 'https://www.imdb.com/review/rw7363919/?ref_=tt_ururv_perm'
TV_LINK = 'https://www.imdb.com/review/rw8266882/?ref_=tt_ururv_perm'
NEUTRAL_LINK = 'https://www.imdb.com/review/rw10324876/?ref_=tt_ururv_perm'
RATINGLESS_LINK = 'https://www.imdb.com/review/rw0299483/?ref_=tturv_perm_4'

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
            raise Exception("Missing rating!")
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

    # remove the word 'br' explicitly
    words = [word for word in words if word != 'br']
    
    return words
