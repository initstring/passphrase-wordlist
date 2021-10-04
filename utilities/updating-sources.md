# Notes on updating sources

Sure, this should be a CI job. But hey, it's a start.

Some of the source files get regular updates. Below is a guide to obtaining those, preparing them for cleaning, actually cleaning, and then merging into the existing list.

## IMDB titles

```
wget https://datasets.imdbws.com/title.basics.tsv.gz
gunzip ./title.basics.tsv.gz
cat title.basics.tsv | awk -F '\t' '{print $3}' > ./imdb-titles-$(date +%Y-%m-%d).txt
rm title.basics.tsv
```

## Wikipedia article titles & category names

```
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream-index.txt.bz2
bunzip2 ./enwiki-latest-pages-articles-multistream-index.txt.bz2
cat ./enwiki-latest-pages-articles-multistream-index.txt | cut -d: -f 3 > ./wikipedia-$(date +%Y-%m-%d).txt
rm enwiki-latest-pages-articles-multistream-index.txt

```

## Wiktionary titles

```
wget https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles.gz
gunzip enwiktionary-latest-all-titles.gz
cat enwiktionary-latest-all-titles | awk -F '\t' '{print $2}' > ./wiktionary-$(date +%Y-%m-%d).txt
rm enwiktionary-latest-all-titles

```

## Urban Dictionary

```
git clone https://github.com/initstring/urban-dictionary-word-list
cd urban-dictionary-word-list
python3 ./main.py --out urban-dictionary-$(date +%Y-%m-%d).txt
```

## Know Your Meme

```
python3 /utilities/kym_scrape.py
mv memes.txt ./know-your-meme-$(date +%Y-%m-%d).txt
```

## Global POI dataset

```
wget http://download.geonames.org/export/dump/allCountries.zip
unzip ./allCountries.zip
cat allCountries.txt | awk -F '\t' '{print $3}' > ./global-poi-$(date +%Y-%m-%d).txt
rm allCountries.zip
rm allCountries.txt
```

## Billboard charts

```
git clone https://github.com/initstring/umdmusic-downloader
cd umdmusic-downloader
pip install -r ./requirements.txt
python2 ./downloader.py
cat ./us_billboard.psv | cut -d "|" -f 5 > ./billboard-titles-$(date +%Y-%m-%d).txt
cat ./us_billboard.psv | cut -d "|" -f 6 | sed "s/ featuring /\n/g" > ./billboard-artists-$(date +%Y-%m-%d).txt
```

## Combining

With all raw files in the same folder:

```
cat ./*.txt | sort -u > raw.txt
python3 ./cleanup.py raw.txt passphrases.txt
```
