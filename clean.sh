#!/bin/bash
INFILE=$1
OUTFILE=$2

# It might be worth running this script twice. :)

cat $INFILE | sed 's/^[ \t]*//;s/[ \t]*$//'                               `# strip whitespace from beginning and end` \
            | awk '{print tolower($0)}'                                   `# switch to all lowercase` \
	    | awk -niord '{printf RT?$0chr("0x"substr(RT,2)):$0}' RS=%..  `# remove url encoding` \
	    | tr -cd '\000-\177'                                          `# remove funky chars like smartquotes, TM` \
            | sed -r "s/([a-z']* [a-z']* [a-z']*)(, )/\1"\\n"/g"          `# split long lines that have a comma*` \
	    | sed -r "s/([a-z]*)([_-])/\1 /g"                             `# change hyphens & underscores to spaces` \
            | tr -d '[:punct:]'                                           `# remove punctuation` \
	    | sed "s/ \+/ /g"                                             `# combine multiple spaces into one` \
	    | grep ' '                                                    `# look for phrases, not words` \
	    | awk 'length($0)<36 && length($0)>4'                         `# keep lines between 5 and 35 characters` \
	    | sort | uniq                                                 `# sort and remove duplicates` \
  >> ./$OUTFILE


# * what this is doing is looking for an instance of three words (separated by spaces) followed by a comma,
#   and then replacing that comma with a newline. I'm allowing apostrophes in those words, that will be stripped later. 
#   There's probably a better way to do this. If you know one, please let me know.
