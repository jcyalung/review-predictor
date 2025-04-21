# review predictor

predict imdb movie reviews given IMDB links or user input.
models are trained from this [dataset](https://ai.stanford.edu/~amaas/data/sentiment/) by Andrew Maas. 

## running the code

the backend requires these libraries, some already installed, most of which you can install using `pip`: <br>
``` fastapi uvicorn logging bs4 re requests numpy matplotlib sklearn ```
to run the backend,
run these two commands: <br>
```
cd backend
python server.py --reload=[RELOAD] --db=[NAME]

usage: server.py [-h] [--host HOST] [--port PORT] --reload RELOAD [--verbose] --db_name DB_NAME
```

to run the front end, run these commands: <br>
```
cd frontend
npm run dev
```
