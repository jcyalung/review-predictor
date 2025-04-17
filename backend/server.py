from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from args import get_args
import uvicorn
import time
import logging
import learners as learn
import dataset as db
from enums import Code
from sqlite_helpers import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

args = get_args()
FILE = args.db_name
KEYS = ["url", "user", "media_name", "episode_name", "score", "review"]


@app.get("/")
def root():
    return ({ "message" : "hello world!"})

@app.get("/store-review")
def store_review(url=None):
    if url is None:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"url is required"})
    values = db.get_review(url)
    review_dict = dict(zip(KEYS, values))
    review_dict['prediction'] = 'unknown'
    if insert_review(FILE, **review_dict):
        return {'status_code' : Code.OK, 'message': 'review stored to database!', 'result':review_dict}
    else:
        raise HTTPException(Code.BAD_REQUEST, detail={'message':'an error occurred.'})
    
@app.post("/predict-review")
async def predict_review(request : Request):
    print('predict review api called')
    req_json = await request.json()
    if "url" not in req_json:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"No url found!"})
    if "model" not in req_json:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"Model not specified"})
    review = None
    try:
        # review = retrieve_review(FILE, req_json["url"])
        # if review is None:
        #     review = db.get_review(req_json["url"])
        #     review_dict = dict(zip(KEYS, review))
        #     insert_review(FILE, **review_dict)
        # print(review)

        review = db.get_review(req_json["url"])
        review_dict = dict(zip(KEYS, review))
        insert_review(FILE, **review_dict)
        review = retrieve_review(FILE, req_json["url"])
    except Exception as e:
        print(e)
        raise HTTPException(Code.BAD_REQUEST, detail={"message":e.args})
    review = (review[6], review[4])
    result, label = learn.predict_review(review=review, model_type=req_json["model"])
    update_prediction(FILE, req_json["url"], result)
    if result is None:
        raise HTTPException(Code.INTERNAL_SERVER_ERROR, detail={"message": "error predicting label"})
    return {'status_code' : Code.OK, 'result': result, 'label' : label }

@app.post("/predict-input")
async def predict_input(request : Request):
    req_json = await request.json()
    if "review" not in req_json:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"Review is required"})
    if "model" not in req_json:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"Model not specified"})
    if "label" not in req_json:
        raise HTTPException(Code.BAD_REQUEST, detail={"message":"Score not specified"})
    review = (req_json["review"], req_json["label"])
    result, label = learn.predict_review(review=review, model_type=req_json["model"])
    return {'status_code':Code.OK, 'result':result, 'label':label}
    
@app.get("/all-reviews")
async def all_reviews():
    reviews = list_reviews(FILE)
    reviews = [
        {
            'link': link,
            'user': user,
            'media_name': media_name,
            'episode_name': episode_name,
            'score': score,
            'prediction': prediction,
            'review': text,
            'timestamp': timestamp,
            'id': review_id
        }
        for link, user, media_name, episode_name, score, prediction, text, timestamp, review_id in reviews
    ]
    return {'status_code' : Code.OK, 'reviews':reviews}

@app.get("/recent-reviews")
async def recent_reviews(count = 5):
    try:
        count = int(count)
    except Exception as e:
        return HTTPException(Code.BAD_REQUEST, detail={'message' : 'Invalid count'})
    reviews = list_reviews(FILE)
    reviews = [
        {
            'link': link,
            'user': user,
            'media_name': media_name,
            'episode_name': episode_name,
            'score': score,
            'prediction': prediction,
            'review': text,
            'timestamp': timestamp,
            'id': review_id
        }
        for link, user, media_name, episode_name, score, prediction, text, timestamp, review_id in reviews
    ]
    
    reviews = sorted(reviews, key=lambda x: x['timestamp'], reverse=True)
    return {'status_code' : Code.OK, 'count' : count, 'reviews' : reviews[:count]}
    
@app.get("/logging-levels")
def logging_levels():
    logging.error("error message")
    logging.warning("warning message")
    logging.info("info message")
    logging.debug("debug message")


logging.Formatter.converter = time.gmtime
logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level= logging.ERROR - (args.verbose*10),
)

if __name__ == "__main__":
    create_table(FILE)
    uvicorn.run("server:app", host=args.host, port=args.port, reload=args.reload)