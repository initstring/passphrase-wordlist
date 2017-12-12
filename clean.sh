#!/bin/bash
INFILE=$1
OUTFILE=$2

# It might be worth running this script twice. :)

cat $INFILE \
    | sed -r "s/([a-zA-Z]* [a-zA-Z]* [a-zA-Z]*)([,.] )/\1\\n/g"  `# Split up longer lines containing , or .` \
    | sed -e "s/^[ \t]*//;s/[ \t]*$//"                           `# strip whitespace from beginning and end` \
          -e "s/\(.*\)/\L\1/"                                    `# switch to lowercase` \
          -e "s/[-_]/ /g"                                        `# change hyphens & underscores to spaces` \
          -e "s/ \+/ /g"                                         `# combine multiple spaces into one` \
          -e "s~[^[:alnum:] ]\+~~g"                              `# keep only alphanumeric characters and spaces` \
    | grep ' '                                                   `# look for at least one space` \
    | awk 'length($0)<41 && length($0)>4'                        `# enforce length` \
    | sort | uniq                                                `# sort and remove duplicates` \
>> ./$OUTFILE


# Here are some commands that might be useful for certain datasets:
#   | awk -niord '{printf RT?$0chr("0x"substr(RT,2)):$0}' RS=%..       # removes URL encoding

