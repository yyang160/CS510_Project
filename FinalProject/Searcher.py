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
        top_docs = ranker.score(self.idx, q, num_results=100)

        songsdata = songsdata.readlines()
        recommend = []

        for sid, score in top_docs:
            d = {}
            song = songsdata[sid].split('\t')

            d['artist'] = song[0]
            d['song'] = song[1]
            d['sentiment'] = song[2]
            d['link'] = song[3]
            d['text'] = song[4].replace('@', '\n')
            results.append(d)

            # Compute recommended songs
            if len(recommend) < 8:
                artist = song[0]
                song = song[1]
                sentiment = song[2]
                recommend.append(self.getRecommend(artist, song, sentiment))

        return results, recommend

    def getRecommend(self, artist, song_name, sentiment):
        with open('songsdata/singer_scores.json') as json_file:
            scores = json.load(json_file)
        songs = scores[artist]
        idx = 0
        for i, song in enumerate(songs):
            score, name = song
            if name == song_name:
                idx = i
                break
        if sentiment == 'positive' or sentiment == 'neutral':
            if idx + 1 < len(songs):
                return songs[idx+1][1]
            elif len(songs) >= 2:
                return songs[idx-1][1]
            else:
                return None
        else:
            if idx - 1 >= 0:
                return songs[idx-1][1]
            elif len(songs) >= 2:
                return songs[idx+1][1]
            else:
                return None


s = Searcher()
results, recommend = s.search("rain")
print(results[0])
print(results[0]['sentiment'])
print(recommend)





