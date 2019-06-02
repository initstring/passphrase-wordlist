#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prepares passphrase cracking lists for use with the hashcat rules at
github.com/initstring/passphrase-wordlist
"""

import sys
import re
import urllib.parse
import html
import os
import time
import argparse
from datetime import timedelta

# Set a min/max passphrase character length. Change this if you want.
MIN_LENGTH = 8
MAX_LENGTH = 40

def parse_arguments():
    """
    Handles user-passed parameters
    """
    desc = 'Transforms text files in passphrase lists.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('infile', type=str, action='store',
                        help='Input file.')
    parser.add_argument('outfile', type=str, action='store',
                        help='Output file.')

    args = parser.parse_args()

    if not os.access(args.infile, os.R_OK):
        print("[!] Cannot access input file, exiting")
        sys.exit()

    return args

def build_buffer(infile):
    """
    Reads infile and builds a list of candidates for additional processing
    """
    buffer = []

    infile_size = str((int(os.path.getsize(infile)/1000000))) + " MB"
    print("Reading from {}: {}".format(infile, infile_size))

    with open(infile, encoding='utf-8', errors='ignore') as file_handler:
        for line in file_handler:
            candidates = []
            # Remove HTML and URL encoding first
            line = escape_encoding(line)

            # Split lines with common delimiters like . , or ;
            for split_line in re.split(r';|,|\.', line):
                candidates.append(split_line.strip())

            # There is a new short list, append each to the buffer
            for string in candidates:
                buffer.append(string)

    return buffer

def handle_punctuation(line):
    """
    Deals with common punctionation
    """
    clean_lines = []

    # Allow only letters, numbers, spaces, and some punctuation
    allowed_chars = re.compile("[^a-zA-Z0-9 '&]")

    # Gets rid of any remaining special characters in the name
    line = allowed_chars.sub('', line)

    # Shrinks down multiple spaces
    line = re.sub(r'\s\s+', ' ', line)

     # If line has an apostrophe make a duplicate without
    if "'" in line:
        clean_lines.append(re.sub("'", "", line))

    # Making duplicating phrases including and / &
    if ' and ' in line:
        clean_lines.append(re.sub(' and ', ' & ', line))
    if '&' in line:
        newline = re.sub('&', ' and ', line)
        newline = re.sub(r'\s+', ' ', newline).strip()
        clean_lines.append(newline)

    # Add what is left to the list and return it
    clean_lines.append(line)
    return clean_lines

def escape_encoding(line):
    """
    Deals with common encoding and accented characters
    """
    line = urllib.parse.unquote(line)       # convert URL encoding like %27
    line = html.unescape(line)              # convert HTML encoding like &apos;
    line = re.sub(r'\s+', ' ', line).strip() # Remove extra whitespace
    line = line.lower()                     # convert to lowercase
    line = re.sub(r'[-_]', ' ', line)       # Change - and _ to spaces

    # The following lines attempt to remove accented characters, as the
    # tool is focused on Engligh-language passwords.
    line = re.sub('[àáâãäå]', 'a', line)
    line = re.sub('[èéêë]', 'e', line)
    line = re.sub('[ìíîï]', 'i', line)
    line = re.sub('[òóôõö]', 'o', line)
    line = re.sub('[ùúûü]', 'u', line)
    line = re.sub('[ñ]', 'n', line)

    return line

def choose_candidates(line):
    """
    Final check to determine with cleaned phrases to keep
    """
    match = re.compile('[a-z0-9\'&] [a-z0-9\'&]')
    # Throw out single-word candidates
    if not match.search(line):
        return False

    # Thow out too short / too long lines
    if len(line) < MIN_LENGTH or len(line) > MAX_LENGTH:
        return False

    return True

def write_file(buffer, outfile):
    """
    Writes choses candidates to an output file
    """
    file_handler = open(outfile, 'w')
    for line in buffer:
        file_handler.write(line.strip()+ '\n')
    file_handler.close()

    outfile_size = str((int(os.path.getsize(outfile)/1000000)))
    print("Wrote to {}: {} MB".format(outfile, outfile_size))


def main():
    """
    Main program function
    """
    start = time.time()
    args = parse_arguments()
    buffer = build_buffer(args.infile)
    final = set([])
    # Processes phrases and adds to a set (deduped)
    for phrase in buffer:
        new_phrases = handle_punctuation(phrase)
        for newphrase in new_phrases:
            if choose_candidates(newphrase):
                final.add(newphrase)
    # Writes final set out to file
    write_file(final, args.outfile)
    elapsed = (time.time() - start)
    print("Elapsed time: " + str(timedelta(seconds=elapsed)))


if __name__ == "__main__":
    main()
