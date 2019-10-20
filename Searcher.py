import metapy
import json
import os
import sys

import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    letters += ' '
    return ''.join(random.choice(letters) for i in range(stringLength))

class Searcher:

    def __init__(self):
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.toml')

        # print(config_file_path)
        self.idx = metapy.index.make_inverted_index(config_file_path)
        self.ranker = metapy.index.OkapiBM25()


    def search(self, query):

        with open('docs.json', 'r') as fp:
            data = json.load(fp)

        results = []
        print("start indexing")
        q = metapy.index.Document()
        q.content(query)
        print("find top docs")
        ret = []
        for i in range(50):
            title = randomString(10)
            abstract = randomString(100)
            url = 'www.google.com'
            ret.append({'title':title, 'url':url, 'abstract':abstract})
        return ret
        # top_docs = self.ranker.score(self.idx, q)
        # print("output")
        # for d_id, score in top_docs:
        #     print(d_id, score)
        #     if str(d_id) in data:
        #         results.append(data[str(d_id)])
        # return results

if __name__ == "__main__":
    s = Searcher()
  #  print(sys.modules.keys())
    print(s.search('text'))