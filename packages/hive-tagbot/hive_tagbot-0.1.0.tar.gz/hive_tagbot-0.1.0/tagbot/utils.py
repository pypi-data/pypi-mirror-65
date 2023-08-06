import math
import os
from datetime import datetime

from dateutil.parser import parse
from nltk import wordpunct_tokenize, PorterStemmer
from hive import Hive
from hive.account import Account

_steem_conn = None


def get_hive_conn(nodes):
    global _steem_conn
    if _steem_conn is None:
        _steem_conn = Hive(
            nodes=nodes,
            keys=[os.getenv("POSTING_KEY"), ]
        )

    return _steem_conn


def get_current_vp(username, steemd):
    account = Account(username, hived_instance=steemd)
    last_vote_time = parse(account["last_vote_time"])
    diff_in_seconds = (datetime.utcnow() - last_vote_time).total_seconds()
    regenerated_vp = diff_in_seconds * 10000 / 86400 / 5
    total_vp = (account["voting_power"] + regenerated_vp) / 100
    if total_vp > 100:
        total_vp = 100

    return total_vp


def url(p):
    return "https://hive.blog/@%s/%s" % (p.get("author"), p.get("permlink"))


def reputation(reputation, precision=2):
    rep = int(reputation)
    if rep == 0:
        return 25
    score = max([math.log10(abs(rep)) - 9, 0]) * 9 + 25
    if rep < 0:
        score = 50 - score
    return round(score, precision)


def tokenize(text):
    porter = PorterStemmer()
    words = wordpunct_tokenize(text)
    stemmed = [porter.stem(word) for word in words]
    return [
        word.lower()
        for word in stemmed
        if word.isalpha()
        and len(word) > 2
    ]
