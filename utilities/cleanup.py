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

# Compiled regex patterns for performance
MULTIWORD_PATTERN = re.compile('[a-z0-9\'&] [a-z0-9\'&]')
ALLOWED_CHARS_PATTERN = re.compile("[^a-zA-Z0-9 '&]")
MULTIPLE_SPACES_PATTERN = re.compile(r'\s\s+')
QUOTE_REMOVAL_PATTERN = re.compile(r" '([^']*)' ")
WHITESPACE_PATTERN = re.compile(r'\s+')
HYPHEN_UNDERSCORE_PATTERN = re.compile(r'[-_]')
APOSTROPHE_REMOVAL_PATTERN = re.compile("'")
AND_TO_AMPERSAND_PATTERN = re.compile(' and ')
AMPERSAND_TO_AND_PATTERN = re.compile('&')

# Accented character patterns
ACCENTED_A_PATTERN = re.compile('[àáâãäå]')
ACCENTED_E_PATTERN = re.compile('[èéêë]')
ACCENTED_I_PATTERN = re.compile('[ìíîï]')
ACCENTED_O_PATTERN = re.compile('[òóôõö]')
ACCENTED_U_PATTERN = re.compile('[ùúûü]')
ACCENTED_N_PATTERN = re.compile('[ñ]')
ACCENTED_C_PATTERN = re.compile('[ç]')
ACCENTED_Y_PATTERN = re.compile('[ÿ]')

# Split pattern
SPLIT_PATTERN = re.compile(r';|,|\.')

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
            for split_line in SPLIT_PATTERN.split(line):
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

    # Gets rid of any remaining special characters in the name
    line = ALLOWED_CHARS_PATTERN.sub('', line)

    # Shrinks down multiple spaces
    line = MULTIPLE_SPACES_PATTERN.sub(' ', line)

    # Strip quotes around line
    line = line.strip('\'"')

    # Remove quotes around internal segments
    line = QUOTE_REMOVAL_PATTERN.sub(r' \1 ', line)

    # If line has an apostrophe make a duplicate without deleting it
    if "'" in line:
        clean_lines.append(APOSTROPHE_REMOVAL_PATTERN.sub("", line))

    # Making duplicating phrases including and / &
    if ' and ' in line:
        clean_lines.append(AND_TO_AMPERSAND_PATTERN.sub(' & ', line))
    if '&' in line:
        newline = AMPERSAND_TO_AND_PATTERN.sub(' and ', line)
        newline = WHITESPACE_PATTERN.sub(' ', newline).strip()
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
    line = WHITESPACE_PATTERN.sub(' ', line).strip() # Remove extra whitespace
    line = line.lower()                     # convert to lowercase
    line = HYPHEN_UNDERSCORE_PATTERN.sub(' ', line)       # Change - and _ to spaces

    # The following lines attempt to remove accented characters, as the
    # tool is focused on Engligh-language passwords.
    line = ACCENTED_A_PATTERN.sub('a', line)
    line = ACCENTED_E_PATTERN.sub('e', line)
    line = ACCENTED_I_PATTERN.sub('i', line)
    line = ACCENTED_O_PATTERN.sub('o', line)
    line = ACCENTED_U_PATTERN.sub('u', line)
    line = ACCENTED_N_PATTERN.sub('n', line)
    line = ACCENTED_C_PATTERN.sub('c', line)
    line = ACCENTED_Y_PATTERN.sub('y', line)

    return line

def choose_candidates(line):
    """
    Final check to determine with cleaned phrases to keep
    """
    # Throw out single-word candidates
    if not MULTIWORD_PATTERN.search(line):
        return False

    # Thow out too short / too long lines
    if len(line) < MIN_LENGTH or len(line) > MAX_LENGTH:
        return False

    return True

def write_file(buffer, outfile):
    """
    Writes choses candidates to an output file
    """
    with open(outfile, 'w') as file_handler:
        for line in sorted(buffer):
            file_handler.write(line.strip() + '\n')

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
    elapsed = time.time() - start
    print("Elapsed time: " + str(timedelta(seconds=elapsed)))


if __name__ == "__main__":
    main()
