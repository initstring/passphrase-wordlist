#!/bin/bash
INFILE=$1
OUTFILE=$2

# It might be worth running this script twice. :)

cat $INFILE \
    | grep -E '[a-z]{2}.* | [a-z]{2}'                            `# must have at least one space and two seq letters` \
    | sed -r "s/([a-zA-Z]* [a-zA-Z]* [a-zA-Z]*)([,.] )/\1\\n/g"  `# Split up longer lines containing , or .` \
    | sed -e "s/\(.*\)/\L\1/"                                    `# switch to lowercase` \
          -e "s/[-_]/ /g"                                        `# change hyphens & underscores to spaces` \
          -e "s/ \+/ /g"                                         `# combine multiple spaces into one` \
          -e "s/[^[:punct:]a-z0-9 ]//g"                          `# keep only letters numbers and spaces` \
          -e "s/^[ \t]*//;s/[ \t]*$//"                           `# strip whitespace from beginning and end` \
    | awk 'length($0)<41 && length($0)>4'                        `# enforce length` \
    | sort | uniq                                                `# sort and remove duplicates` \
>> ./$OUTFILE


# Here are some commands that might be useful for certain datasets:
#   | awk -niord '{printf RT?$0chr("0x"substr(RT,2)):$0}' RS=%..       # removes URL encoding

