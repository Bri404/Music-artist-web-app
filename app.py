import flask  # micro web framework
import os  # operating system interface
import requests  # pulling information from websites
import json  # exposes an API familiar to users of the standard library
import random  # generates random numbers
import tweepy  # gets tweets from twitter

url = "https://api.genius.com/search?q=Masego"

auth = {"Authorization": os.getenv('BEARER')}

auth2 = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))

auth2.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
api = tweepy.API(auth2)


# gets the page needed for the artist
def web_page():
    response = requests.get(url, headers=auth)
    json_body = response.json()
    random_song = random.randint(0, len(json_body['response']['hits']) - 1)

    return json_body['response']['hits'][random_song]


# creates a variable for function web_page()
json_obj = web_page()
# prints info in a formatted way
print(json.dumps(json_obj, indent=2))


# gets tweets from twitter about my artist
def twitter():
    list = []
    # loops through tweets by my artist
    for tweet in api.search("Masego"):
        list.append(tweet.text)
    return list


# calling the function
twitter()

app = flask.Flask(__name__)


@app.route('/')  # add new functionality to an existing object without modifying its structure
def hello():  # function
    page = web_page()
    tweets = twitter()
    # returns the content from my html file
    return flask.render_template(
        "index.html",
        # gets the image of the song from genius
        image=json_obj['result']['header_image_thumbnail_url'],
        # gets the song title from genius
        sng=json_obj['result']['title'],
        tw=tweets

    )


app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)  # run on this web server