#!/user/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import sys
import MeCab
import random
import re

consumer_key=os.environ["CONSUMER_KEY"],
consumer_secret=os.environ["CONSUMER_SECRET"],
access_token_key=os.environ["ACCESS_TOKEN_KEY"],
access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]

def Mecab_file():
    file = open("words.txt", "rb")
    data = file.read()
    file.close()

    mecab_tagger = MeCab.Tagger("-Owakati")

    wordlist = mecab_tagger.parse(data)
    wordlist = wordlist.rstrip(" \n").split(" ")

    markov = {}
    w = ""

    for word in wordlist:
        if w:
            if markov.has_key(w):
                new_list = markov[w]
            else:
                new_list = []

            new_list.append(word)
            markov[w] = new_list
        w = word

    choice_words = wordlist[0]
    sentence = ""
    count = 0

    while count < 90:
        sentence += choice_words
        choice_words = random.choice(markov[choice_words])
        count += 1

        sentence = sentence.split(" ", 1)[0]
        p = re.compile("[!-/:-@[-`{-~]")
        sus = p.sub("", sentence)

    words = re.sub(re.compile("[!-~]"), "", sus)


url = "https://api.twitter.com/1.1/statuses/update.json"
params = {"status": words, "lang": "ja"}
tw = OAuth1Session(consumer_key, consumer_secret, access_token_key, access_token_secret)
req = tw.post(url, params = params)

if req.status_code == 200:
    print('tweet success')
else:
    print(req.status_code)
