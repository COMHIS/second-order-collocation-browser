import re, sys, json, os
import pandas
from sklearn.manifold import MDS
import wget, random
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import html_res


def API_query(query_item, period, limit):

    # builds the API query for wget

    url = "https://vm0175.kaj.pouta.csc.fi/ecco-search2/collocations?"
    url += "term="+query_item
    url += "&level=paragraph"
    url += "&limitQuery=pubDate:["+period[0]+"%20TO%20"+period[1]+"]"
    url += "&limit="+str(limit)
    url += "&minSumFreq=5"
    url += "&sumScaling=absolute"
    print(url)
    return url

def open_saved_wordlist(query, P):

    # tries to open pre-saved wordlist and first order collocation data, if fails queries and saves them using the API

    try:
        with open(query+"_".join(P)+".json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        IOError
        return build_new_wordlist(query, P)

def build_new_wordlist(query, P, stopwords):

    # builds first order collocation data and random sample of 400 items of it as a separate wordlist

    filename = wget.download(API_query(query, P, 5000))
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    sample = random.sample(data["collocations"].keys(), 400)
    sample = [x for x in sample if x not in stopwords]
    os.remove(filename)
    with open(query+"_".join(P)+".json", "w", encoding="utf-8") as f:
        json.dump((data, sample), f)
    return data, sample

def download_vector(query, P):

    # downloads a single word collocation vector and saves it

    fn = wget.download(API_query(query, P, 1000))
    
    with open(fn, "r", encoding="utf-8") as f:
        d = json.load(f)
    os.remove(fn)

    with open(col_path+row+".json", "w", encoding="utf-8") as f:
        json.dump(d, f)

    return d

# parameters from the command line:
    # Q = queried word
    # P = start year, end year)
    # DL whether to download new list for queried word

Q = sys.argv[1]
P = (sys.argv[2]+"0000", sys.argv[3]+"0000")
DL = len(sys.argv) > 4 and sys.argv[4] == "download"
try:
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = [x.replace("\n", "")  for x in f]
except:
    IOError
    stopwords = []


col_path = "collocations_"+"_".join(P)+"/"

if not os.path.isdir(col_path):
    os.mkdir(col_path)

if not os.path.isdir("html/"):
    os.mkdir("html")

if not os.path.isdir("html/images/"):
    os.mkdir("html/images/")



df = {}
run = 0

if DL:
    data, wordlist = build_new_wordlist(Q, P, stopwords)
else:
    data, wordlist = open_saved_wordlist(Q, P)
    
# building the second order collocation matrix

wordlist = [x for x in wordlist if x not in stopwords]

for row in wordlist:
    if len(row) > 2:
        try:
            with open(col_path+row+".json", "r", encoding="utf-8") as f:
                df.update({row : json.load(f)["collocations"]})
        except:
            IOError
            if DL:
                df.update({row : download_vector(row, P)["collocations"]})

# matrix to pandas DataFrame
df = { w : df[w] for w in df if sum(df[w].values()) > 0}



df = pandas.DataFrame(df)
df = df.transpose()
df = df.fillna(0)
df = df.div(df.sum(axis=0), axis=1)
tot = sum([data["collocations"][x] for x in wordlist])
sizes = [data["collocations"][w]/tot*10000 for w in df.index]

# MDS and plotting

mds = MDS()
pos = mds.fit(df).embedding_
scale = [-2.0, 2.0, -2.0, 2.0]
plt.axis(scale)
plt.scatter(pos[:, 0], pos[:, 1], s=sizes[:], c="white")
imagepath = "images/"+"_".join([Q, str(P[0]), str(P[1])])
plt.savefig("html/"+imagepath)

# build interactive HTML browsing file

with open("html/"+col_path.replace("/", ".html"), "w", encoding="utf-8") as f:
    f.write(html_res.get_HTML(imagepath, int(P[0].replace("0000", "")), pos, list(df.index), list(df.index), scale, sizes))
