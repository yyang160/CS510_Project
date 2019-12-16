import csv
import json


def csv2dat(fp):
    with open('songsdata/song_sentiment.json') as json_file:
        sentiment = json.load(json_file)

    with open('songsdata/songsdata.txt', 'w') as txt_dest:
        with open('songsdata/songsdata.dat', 'w') as dest:
            with open(fp) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        continue
                    text = row[3].replace('\n', '')
                    lyrics = row[1] + '. ' + text + '\n'

                    dest.write(lyrics)
                    text = row[3].replace('\n', '@')
                    txt_dest.write(row[0] + '\t' + row[1] + '\t' + sentiment[str(i-1)] + '\t' + row[2] + '\t' + text + '\n')
        dest.close()
        txt_dest.close()



fp = 'songsdata/songdata.csv'
csv2dat(fp)
dat = open('songsdata/songsdata.dat', 'r')
