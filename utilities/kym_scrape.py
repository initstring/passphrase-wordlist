#!/usr/bin/env python3

"""
Know Your Meme Scraper
Grabs all titles from https://knowyourmeme.com

Puts output into memes.txt

Used to feed into password cracking wordlists like
https://github.com/initstring/passphrase-wordlist

Code by initstring
"""

import html
import time
import re
import sys
import requests

# The "all" URL allows autoscrolling
KYM_URL = 'https://knowyourmeme.com/memes/all/page'

# Regex to grab all formatted titles
RE_TITLE = re.compile(r'<h2> <a href="/memes/.*?">(.*?)</a> </h2>')

# Text to know when we reached end of line
NO_MORE = 'There are no entries for this category'

# Need real headers to get past WAF
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Out file
OUTFILE = 'memes.txt'

# File for in-process scraping
LOGFILE = 'memes-incomplete.txt'

# Sleep to avoid IP ban
SLEEP = 3

def write_log(phrases):
    """
    Logs phrases as the program runs

    Used for troubleshooting or to at least have _something_ in the case of
    IP ban, failure, etc
    """
    with open(LOGFILE, 'a') as logfile:
        for phrase in phrases:
            phrase = html.unescape(phrase)
            logfile.write(phrase + '\n')

def write_final(phrases):
    """
    Writes all phrases to a log file
    """
    # Unescape the HTML and write the phrases out
    with open(OUTFILE, 'w') as outfile:
        for phrase in phrases:
            phrase = html.unescape(phrase)
            outfile.write(phrase + '\n')

def scrape_pages():
    """
    Loops through all pages of kym
    """
    page = 0
    phrases = set([])

    while True:
        # Build the URL based on auto-scroll behaviour
        url = "{}/{}".format(KYM_URL, page)
        response = requests.get(url, headers=HEADERS)

        # Check for IP ban
        if response.status_code == 403:
            print("\n[!] You have been IP banned. Oops.")
            sys.exit()

        # Return if no more results
        if NO_MORE in response.text:
            print("\n[*] Reached end of line at page {}. Exiting"
                  .format(page))
            return phrases

        # Clear stdout for ongoing notifications
        sys.stdout.flush()
        sys.stdout.write(" " * 20)
        sys.stdout.write("\r")

        # Grab phrases from the raw text and add to set
        new_phrases = re.findall(RE_TITLE, response.text)
        phrases.update(new_phrases)

        # Write the new phrases to an ongoing logile
        write_log(new_phrases)

        # Update the patiently waiting user
        sys.stdout.write("[*] Page: {}, Phrases: {}, Unique Phrases: {}"
                         .format(page, len(new_phrases), len(phrases)))

        # Increment the page for the next loop
        page += 1

        # Sleep to avoid IP ban
        time.sleep(SLEEP)


def main():
    """
    Main program function
    """
    print("[*] Scraping all pages of KYM...")
    phrases = scrape_pages()

    print("[+] Found {} phrases, writing to {}..."
          .format(len(phrases), OUTFILE))
    write_final(phrases)


if __name__ == "__main__":
    main()
