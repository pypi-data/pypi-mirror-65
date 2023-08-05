import os
import subprocess
import sys

import toml
import tweepy

import settings
from logger import logging

auth = {}
tokens_fn = ''


def open_url(url):
    if sys.platform == "win32":
        os.startfile(url)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", url])
    else:
        try:
            subprocess.Popen(["xdg-open", url])
        except OSError:
            print("Please open a browser on: " + url)


def publish(info):
    global auth, tokens_fn
    api = tweepy.API(auth)

    try:
        api.update_status(
            " is #NowPlaying ♫: " + info["now"] + " #streamcables"
        )
    except tweepy.TweepError:
        os.remove(tokens_fn)
        session_setup()
        api = tweepy.API(auth)

    public_tweets = api.home_timeline()

    for tweet in public_tweets[0:1]:
        print(tweet.text)


def register():
    global tokens_fn
    tokens_fn = settings.config['dirs'].user_data_dir + "/twitter.toml"

    session_setup()

    logging.info("[twitter] writer registered.")
    return publish


def session_setup():
    global auth, tokens_fn

    mysettings = settings.config['twitter']

    app_key = ''
    app_secret = ''

    try:
        app_key = mysettings["consumer-key"]
        app_secret = mysettings["consumer-secret"]
    except KeyError:
        print('Please add the consumer-key and consumer-secret '
              'to the [twitter] section of the settings file located at ' + settings.config['settings_fn'])
        exit(1)

    auth = tweepy.OAuthHandler(app_key, app_secret)

    try:
        tokens = toml.load(tokens_fn)
    except (FileNotFoundError, KeyError):
        # new authorization request
        logging.info("[twitter] new access token required")
        tokens = authorize()

    auth.set_access_token(tokens["access_token"], tokens["access_token_secret"])
    logging.info("[twitter] reused access token.")


def authorize():
    global auth, tokens_fn
    try:
        redirect_url = auth.get_authorization_url()
        open_url(redirect_url)
    except tweepy.TweepError:
        print("Error! Failed to get request token.")

    verifier_code = input("Verifier code: ")
    auth.get_access_token(verifier_code)

    tokens = {
        "access_token": auth.access_token,
        "access_token_secret": auth.access_token_secret,
    }

    with open(tokens_fn, "w") as f:
        toml_string = toml.dumps(tokens)
        f.write(toml_string)

    return tokens
