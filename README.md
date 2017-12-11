# Overview
This is a project to build a massive wordlist using passphrases for cracking password hashes. Most of the wordlists I know of (rockyou, exploitin, crackstation, etc) contain single-word passwords. People are getting smarter and using phrases instead.

**For Cracking: You need only the "passphrases" file**

My list will have the following rules:
- 5 characters or more
- 40 characters or less
- at least one space (making it a phrase, not a single word)
- transform hyphens into spaces
- remove other punctuation

I'd recommend combining with Hashcat rules like [Hob064](https://github.com/praetorian-inc/Hob0Rules).

# Sources Used
So far, I've scraped the following: <br>
- [15,000 Useful Phrases](https://www.gutenberg.org/ebooks/18362)
- Urban Dictionary dataset pulled Dec 09 2017 using [this great script](https://github.com/mattbierner/urban-dictionary-word-list).
- Song lyrics for Rolling Stone's "top 100" artists using my [lyric scraping tool](https://github.com/initstring/lyricpass).
- Movie titles and lines from this [Cornell project](http://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html).
- "Titles" from the [IMDB dataset](https://www.kaggle.com/orgesleka/imdbmovies) on Kaggle.
- [Quotables](https://www.kaggle.com/alvations/quotables) dataset on Kaggle.
- [MemeTracker](https://www.kaggle.com/snap/snap-memetracker) dataset from Kaggle.
- [Wikipedia Article Titles](https://www.kaggle.com/residentmario/wikipedia-article-titles) dataset from Kaggle.
- A few random "top phrases / top quotes" sites

# Cleaning sources
Check out the script [clean.sh](https://github.com/initstring/passphrase-cracker/blob/master/clean.sh) to see how I've cleaned the raw sources. You can find the pre-cleaned data [here](https://github.com/initstring/passphrase-cracker/tree/master/raw-sources).
