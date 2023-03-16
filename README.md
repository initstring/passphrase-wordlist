# Overview

People think they are getting smarter by using passphrases. Let's prove them wrong!

This project includes a massive wordlist of phrases (over 20 million) and two hashcat rule files for GPU-based cracking. The rules will create over 1,000 permutations of each phase.

To use this project, you need:

- The wordlist hosted itself (`passphrases.txt`), which you can find in the [releases](https://github.com/initstring/passphrase-wordlist/releases).
- Both hashcat rules [here](/hashcat-rules/).

**WORDLIST LAST UPDATED**: November 2022

# Usage

Generally, you will use with hashcat's `-a 0` mode which takes a wordlist and allows rule files. It is important to use the rule files in the correct order, as rule #1 mostly handles capital letters and spaces, and rule #2 deals with permutations.

Here is an example for NTLMv2 hashes: If you use the `-O` option, watch out for what the maximum password length is set to - it may be too short.

```
hashcat -a 0 -m 5600 hashes.txt passphrases.txt -r passphrase-rule1.rule -r passphrase-rule2.rule -O -w 3
```

# Sources Used

Some sources are pulled from a static dataset, like a Kaggle upload. Others I generate myself using various scripts and APIs. I might one day automate that via CI, but for now you can see how I update the dynamic sources [here](/utilities/updating-sources.md).

| <ins>**source file name**</ins> | <ins>**source type**</ins> | <ins>**description**</ins> |
| --- | --- | --- |
| wiktionary-2022-11-19.txt | dynamic | Article titles scraped from Wiktionary's index dump [here.](https://dumps.wikimedia.org/enwiktionary) |
| wikipedia-2022-11-19.txt | dynamic | Article titles scraped from the Wikipedia `pages-articles-multistream-index` dump generated 29-Sept-2021 [here.](https://dumps.wikimedia.org/enwiki) |
| urban-dictionary-2022-11-19.txt | dynamic | Urban Dictionary dataset pulled using [this script](https://github.com/mattbierner/urban-dictionary-word-list). |
| know-your-meme-2022-11-19.txt | dynamic | Meme titles from KnownYourMeme scraped using my tool [here.](/utilities/kym_scrape.py) |
| imdb-titles-2022-11-19.txt | dynamic | IMDB dataset using the "primaryTitle" column from `title.basics.tsv.gz` file available [here](https://datasets.imdbws.com/) |
| global-poi-2022-11-19.txt | dynamic | [Global POI dataset](https://download.geonames.org/export/dump/) using the 'allCountries' file from 29-Sept-2021. |
| billboard-titles-2022-11-19.txt | dynamic | Album and track names using [Ultimate Music Database](https://www.umdmusic.com/), scraped with [a fork of mwkling's tool](https://github.com/initstring/umdmusic-downloader), modified to grab Billboard Singles (1940-2021) and Billboard Albums (1970-2021) charts. |
| billboard-artists-2022-11-19.txt | dynamic | Artist names using [Ultimate Music Database](https://www.umdmusic.com/), scraped with [a fork of mwkling's tool](https://github.com/initstring/umdmusic-downloader), modified to grab Billboard Singles (1940-2021) and Billboard Albums (1970-2021) charts. |
| book.txt | static | Kaggle dataset with titles from over 300,000 books. |
| rstone-top-100.txt | static<br>(could be dynamic in future) | Song lyrics for Rolling Stone's "top 100" artists using my [lyric scraping tool](https://github.com/initstring/lyricpass). |
| cornell-movie-titles-raw.txt | static | Movie titles from this [Cornell project](https://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html). |
| cornell-movie-lines.txt | static | Movie lines from this [Cornell project](https://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html). |
| author-quotes-raw.txt | static | [Quotables](https://www.kaggle.com/alvations/quotables) dataset on Kaggle. |
| 1800-phrases-raw.txt | static | [1,800 English Phrases.](https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html) |
| 15k-phrases-raw.txt | static | [15,000 Useful Phrases.](https://www.gutenberg.org/ebooks/18362) |

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

Optionally, some researchers might be interested in the script I use to clean the raw sources into the wordlist [here](/utilities/cleanup.py).

The cleanup script works like this:

```
$ python3.6 cleanup.py infile.txt outfile.txt
Reading from ./infile.txt: 505 MB
Wrote to ./outfile.txt: 250 MB
Elapsed time: 0:02:53.062531

```

Enjoy!
