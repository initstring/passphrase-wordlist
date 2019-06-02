# Overview
People think they are getting smarter by using passphrases. Let's prove them wrong!

This project includes a massive wordlist of phrases (over 20 million) and two hashcat rule files for GPU-based cracking. The rules will create over 1,000 permutations of each phase.

To use this project, you need:
- The wordlist hosted [here](https://initstring.keybase.pub/passphrase-wordlist/passphrases.txt?dl=1).
- Both hashcat rules [here](hashcat-rules/).

**WORDLIST LAST UPDATED**: June-02-2019

# Usage
Generally, you will use with hashcat's `-a 0` mode which takes a wordlist and allows rule files. It is important to use the rule files in the correct order, as rule #1 mostly handles capital letters and spaces, and rule #2 deals with permutations.

Here is an example for NTLMv2 hashes: If you use the `-O` option, watch out for what the maximum password length is set to - it may be too short.

```
hashcat -a 0 -m 5600 hashes.txt passphrases.txt -r passphrase-rule1.rule -r passphrase-rule2.rule -O -w 3
```

# Sources Used
So far, I've scraped the following: <br>
- IMDB dataset using the "primaryTitle" column from `title.basics.tsv.gz` file available [here](https://datasets.imdbws.com/) grabbed May 25.
- From the Wikipedia `pages-articles-multistream-index` dump generated May-20-2019 [here](https://dumps.wikimedia.org/enwiki), article titles and category names.
- From Wiktionary's similar index dump [here](https://dumps.wikimedia.org/enwiktionary), the entries generated May-20-2019.
- Urban Dictionary dataset pulled May 27 2019 using [this great script](https://github.com/mattbierner/urban-dictionary-word-list).
- [15,000 Useful Phrases](https://www.gutenberg.org/ebooks/18362)
- Song lyrics for Rolling Stone's "top 100" artists using my [lyric scraping tool](https://github.com/initstring/lyricpass).
- Movie titles and lines from this [Cornell project](http://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html).
- [Global POI dataset](http://download.geonames.org/export/dump/) using the 'allCountries' file.
- [Quotables](https://www.kaggle.com/alvations/quotables) dataset on Kaggle.
- [1,800 English Phrases](https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html)
- [2016 US Presidential Debates](https://www.kaggle.com/kinguistics/2016-us-presidential-primary-debates) dataset on Kaggle.
- [Goodreads Book Reviews](https://www.kaggle.com/gnanesh/goodreads-book-reviews) from Kaggle. I scraped the titles of over 300,000 books.
- US & UK top album names, artists, and track names from the 1950s - 2018 using [mwkling's tool here](https://github.com/mwkling/umdmusic-downloader).
    - *Note: I modified that python script to download multiple charts, as opposed to just US Billboard*

# Hashcat Rules
The rule files are designed to both "shape" the password and to mutate it. Shaping is based on the idea that human beings follow fairly predictable patterns when choosing a password, such as capitalising the first letter of each word and following the phrase with a number or special character. Mutations are also fairly predictable, such as replacing letters with visually-similar special characters.

Given the phrase `take the red pill` the first hashcat rule will output the following:
```
take the red pill
take-the-red-pill
take.the.red.pill
take_the_red_pill
taketheredpill
Take the red pill
TAKE THE RED PILL
tAKE THE RED PILL
Taketheredpill
tAKETHEREDPILL
TAKETHEREDPILL
Take The Red Pill
TakeTheRedPill
Take-The-Red-Pill
Take.The.Red.Pill
Take_The_Red_Pill
```

Adding in the second hashcat rule makes things get a bit more interesting. That will return a huge list per candidate. Here are a couple examples:

```
T@k3Th3R3dPill!
T@ke-The-Red-Pill
taketheredpill2020!
T0KE THE RED PILL
```

# Additional Info
Optionally, some researchers might be interested in:
- My best-effort to maintain raw sources [here](https://keybase.pub/initstring/passphrase-wordlist/raw-sources).
- The script I use to clean the raw sources into the wordlist [here](utilities/cleanup.py).


The cleanup script works like this:

```
$ python3.6 cleanup.py infile.txt outfile.txt
Reading from ./infile.txt: 505 MB
Wrote to ./outfile.txt: 250 MB
Elapsed time: 0:02:53.062531

```

Enjoy!
