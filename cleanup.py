#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
if not sys.version_info[:2] >= (3, 4):
    print("Please get with the times and use Python 3.4+")
    sys.exit()

import re
import sys
import urllib.parse
import html
import os
import time
from datetime import timedelta

inFile = sys.argv[1]
outFile = sys.argv[2]

def escape_encoding(line):
    line = urllib.parse.unquote(line)               # convert URL encoding like %27
    line = html.unescape(line)                      # convert HTML encoding like &apos;
    line = re.sub('\s+', ' ', line).strip()         # Remove extra whitespace
    line = line.lower()                             # convert to lowercase
    line = re.sub(r'[-_]', ' ', line)               # Change - and _ to spaces
    line = re.sub("[àáâãäå]", 'a', line)            # These lines remove common accents
    line = re.sub("[èéêë]", 'e', line)
    line = re.sub("[ìíîï]", 'i', line)
    line = re.sub("[òóôõö]", 'o', line)
    line = re.sub("[ùúûü]", 'u', line)
    line = re.sub("[ñ]", 'n', line)
    return line

def split_lines(line):
    newLines = re.split(';|,|\. ',line)             # Split at periods and semi-colons. Only split at periods followed
                                                    # by a space. This helps preserve SOME abbreviations but needs 
                                                    # further refining to catch those at the beginning of a phrase.
    return newLines

def handle_punctuation(line):
    cleanLines = []
    allowedChars = re.compile("[^a-zA-Z0-9 '&]")    # Allow only letters, numbers, spaces, and some punctuation
    line = allowedChars.sub('',line)                # Gets rid of any remaining special characters in the name
    line = re.sub("\s\s+" , " ", line)              # Shrinks down multiple spaces
    if "'" in line:                                 # If line has an apostrophe make a duplicate without
        cleanLines.append(re.sub("'", "", line))
    if "and" in line:                               # Making duplicating phrases including and / &
        cleanLines.append(re.sub("and", "&", line))
    if "&" in line:
        cleanLines.append(re.sub("&", "and", line))
    cleanLines.append(line)
    return cleanLines                               # Returns a new list based on the single input line

def choose_candidates(line):
    match = re.compile('[a-z0-9\'&] [a-z0-9\'&]')
    if not match.search(line):                      # Throw out single-word candidates
        return False
    elif len(line) < 8 or len(line) > 50:           # Thow out too short / too long lines 
        return False
    else:
        return True

def write_file(buffer, outfile):
    oF = open(outFile, 'w')
    for line in buffer:
        oF.write(line.strip()+ '\n')
    oF.close()

def build_buffer(inFile):
    buffer = []
    with open(inFile, encoding='utf-8', errors='ignore') as iF:
        for line in iF:
            candidates = []
            line = escape_encoding(line)                # Remove HTML and URL encoding first
            for l in split_lines(line):                 # Split lines with common delimiters like . , or ; 
                candidates.append(l.strip())
            for string in candidates:
                buffer.append(string)                   # These are the items we want to work with, they go in memory
    return buffer


def main():
    start = time.time()
    print("Reading from " + inFile + ": " + str((int(os.path.getsize(inFile)/1000000))) + " MB")
    buffer = build_buffer(inFile)                   # Builds a working list of phrases
    final = set([])
    for phrase in buffer:                           # Processes phrases and adds to a set (deduped)
        newPhrases = handle_punctuation(phrase)
        for phrase in newPhrases:
            if choose_candidates(phrase):
                final.add(phrase)
    write_file(final, outFile)                      # Writes final set out to file
    print("Wrote to " + outFile + ": " + str((int(os.path.getsize(outFile)/1000000))) + " MB")
    elapsed = (time.time() - start)
    print("Elapsed time: " + str(timedelta(seconds=elapsed)))


if __name__ == "__main__":
    main()
