import sqlite3
from datetime import datetime

# this function creates a table in the database
def create_table(filename):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function creates a table that has:
    # link, user who made review, name of media user reviewed, score (positive/negative), timestamp, and id.
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS reviews("
                        "url varchar(255)," 
                        "user varchar(33)," 
                        "media_name varchar(255),"
                        "episode_name TEXT,"
                        "score TEXT CHECK(score IN ('positive', 'negative')) NOT NULL,"
                        "prediction TEXT CHECK(prediction IN ('positive', 'negative', 'unknown')) NOT NULL,"
                        "review TEXT NOT NULL,"
                        "timestamp DATETIME NOT NULL," 
                        "id INTEGER PRIMARY KEY AUTOINCREMENT)")
    except Exception as e:
        print(e)

def insert_review(filename=None, url=None, user=None, media_name=None, episode_name=None, score=None, prediction='unknown', review=None):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # if url with alias already exists
    if retrieve_review(filename, url):
        return False
    # the function inserts a row into the table
    input = 'INSERT INTO reviews(url, user, media_name, episode_name, score, prediction, review, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
    val = (url, user, media_name, episode_name, score, prediction, review, datetime.now())
    cursor.execute(input, val)
    connection.commit()
    return True
    

def delete_review(filename, url):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function deletes a row from the table
    try:
        input = f'DELETE FROM reviews WHERE url=?'
        cursor.execute(input, (url,))
        connection.commit()
        # check if entries have changed
        if(cursor.rowcount() > 0):
            return True
        else:
            return False
    except Exception as e:
        return False

def list_reviews(filename):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function lists all the rows in the table
    result = cursor.execute("SELECT * FROM reviews")
    return result.fetchall()

def retrieve_review(filename, url):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function retrieves a row from the table
    result = cursor.execute(f'SELECT url, user, media_name, episode_name, score, prediction, review, timestamp, id FROM reviews WHERE url=?',
                            (url,))
    return result.fetchone()

# update prediction after
def update_prediction(filename, url, prediction):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE reviews SET prediction = ? WHERE url = ?",
            (prediction, url)
        )
        connection.commit()
        if cursor.rowcount == 0:
            raise Exception(f"No matching row found for URL: {url}")
        else:
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
        
        
def imdb_reviews(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM reviews')
    return result.fetchall()