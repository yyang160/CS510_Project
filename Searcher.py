import metapy
import json

class Searcher:

    def __init__(self):
        self.idx = metapy.index.make_inverted_index("config.toml")

    def search(self, query):

        with open('docs.json', 'r') as fp:
            data = json.load(fp)

        results = []

        ranker = metapy.index.OkapiBM25()
        q = metapy.index.Document()
        q.content(query)
        top_docs = ranker.score(self.idx, q, num_results = 50)

        for d_id, score in top_docs:
            print(d_id, score)
            if str(d_id) in data:
                results.append(data[str(d_id)])
        return results

