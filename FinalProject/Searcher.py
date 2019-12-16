import metapy
import math
import json
import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_score(query):
    # nltk.download('vader_lexicon')

    sid = SentimentIntensityAnalyzer()
    comp = sid.polarity_scores(query)
    return comp['compound']


class BM25Plus(metapy.index.RankingFunction): # Refer to paper for formula and explanation

    def __init__(self, k1, b):
        self.k1 = k1
        self.b = b
        super(BM25Plus, self).__init__()

    def score_one(self, sd):        # score of a single term
        return math.log2((sd.num_docs+1)/sd.doc_count)*((self.k1 + 1)
                                                        * sd.doc_term_count/(self.k1 * ((1-self.b)+self.b * sd.doc_size/sd.avg_dl)
                                                        + sd.doc_term_count)+1)

class Searcher:

    def __init__(self):
        self.idx = metapy.index.make_inverted_index("config.toml")

    def search(self, query):

        songsdata = open('songsdata/songsdata.txt', 'r')

        results = []
        # ranker = metapy.index.OkapiBM25()
        ranker = BM25Plus(k1 = 1.2, b = 0.75)
        q = metapy.index.Document()
        q.content(query)

        top_docs = ranker.score(self.idx, q, num_results=30)

        songsdata = songsdata.readlines()
        recommend = []
        percentage = {'Sentiment':'Level', 'positive': 0, 'neutral': 0, 'negative': 0}

        query_sent = get_score(query)
        new_top_docs = []

        for sid, score in top_docs:
            song = songsdata[sid].split('\t')
            if query_sent < 0:
                if song[2] == 'negative':
                    print(score)
                    score *= 1.1
            elif query_sent > 0:
                if song[2] == 'positive':
                    score *= 1.1
            new_top_docs.append([sid, score])
        new_top_docs.sort(key = lambda x : x[1], reverse = True)

        for sid, score in new_top_docs[:30]:
            d = {}
            song = songsdata[sid].split('\t')

            d['artist'] = song[0]
            d['song'] = song[1]
            d['sentiment'] = song[2]
            d['link'] = 'http://www.lyricsfreak.com' + song[3]
            d['text'] = song[4].replace('@', '\n')

            # Compute recommended songs
            if len(recommend) < 8:
                artist = song[0]
                song = song[1]
                sentiment = song[2]
                recommend.append(self.getRecommend(artist, song, sentiment))

            results.append(d)
            if song[2] == 'positive' or song[2] == 'negative' or song[2] == 'neutral':
                percentage[song[2]] += 1

        return [results, recommend, percentage]

    def getRecommend(self, artist, song_name, sentiment):
        songsdata = open('songsdata/songsdata.txt', 'r')
        songsdata = songsdata.readlines()

        with open('songsdata/singer_scores.json') as json_file:
            scores = json.load(json_file)
        with open('songsdata/singer_scores_sid.json') as json_file:
            sids = json.load(json_file)
        songs = scores[artist]
        singer_sids = sids[artist]
        idx = 0
        for i, song in enumerate(songs):
            score, name = song
            if name == song_name:
                idx = i
                break
        song_data = {}
        if sentiment == 'positive' or sentiment == 'neutral':
            if idx + 1 < len(songs):
                # return songs[idx+1][1]
                sid = singer_sids[idx+1][1]
            elif len(songs) >= 2:
                sid = singer_sids[idx-1][1]
            else:
                sid = None
        else:
            if idx - 1 >= 0:
                sid = singer_sids[idx-1][1]
            elif len(songs) >= 2:
                sid = singer_sids[idx+1][1]
            else:
                sid = None

        if sid:
            song = songsdata[sid].split('\t')
            return {'artist': song[0], 'song': song[1], 'sentiment': song[2],
                    'link': 'http://www.lyricsfreak.com' + song[3],
                    'text': song[4].replace('@', '\n')}
        return None

#
# s = Searcher()
# results, recommend = s.search("rain")
# print(results[0])
# print(results[0]['sentiment'])
# print(recommend)
#




