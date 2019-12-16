import metapy
import math
import json
import csv


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

        for sid, score in top_docs:
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
        return [results, recommend]

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




