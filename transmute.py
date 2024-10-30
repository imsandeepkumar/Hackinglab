#!/usr/bin/env python
"""
Usage: transmute [opts] [inputFile]

Generates transmutations of input words according to selected options.
"""

import sys
import getopt
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Global config variables
CONF_Debug = CONF_infile = CONF_AddSet = CONF_singleWord = None
CONF_leet = CONF_commonleet = CONF_capitalize = False
CONF_NumAppend = CONF_NumPrepend = CONF_NumInsert = CONF_NumEdgeInsert = 0

def add_set(characters):
    global CONF_AddSet
    CONF_AddSet += characters

def parse_args():
    global CONF_Debug, CONF_infile, CONF_singleWord, CONF_leet, CONF_commonleet, CONF_capitalize
    global CONF_NumAppend, CONF_NumPrepend, CONF_NumInsert, CONF_NumEdgeInsert

    opts, args = getopt.getopt(sys.argv[1:], "hdtlLcw:p:P:i:I:nsaA", ["help", "list="])
    CONF_infile = "-" if len(args) == 0 else args[0]
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif opt == "-d":
            CONF_Debug = True
        elif opt == "-t":
            CONF_leet = CONF_capitalize = True
            CONF_NumAppend, CONF_NumPrepend = 3, 2
            add_set("0123456789!@#$%^&*()-+=_`~[]{}\\|;:'\",./<>?")
        elif opt == "-l":
            CONF_leet = True
        elif opt == "-L":
            CONF_commonleet = True
        elif opt == "-p":
            CONF_NumAppend = int(arg)
        elif opt == "-P":
            CONF_NumPrepend = int(arg)
        elif opt == "-i":
            CONF_NumInsert = int(arg)
        elif opt == "-I":
            CONF_NumEdgeInsert = int(arg)
        elif opt == "-a":
            add_set("abcdefghijklmnopqrstuvwxyz")
        elif opt == "-A":
            add_set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        elif opt == "-n":
            add_set("0123456789")
        elif opt == "-s":
            add_set("!@#$%^&*()-+=_`~[]{}\\|;:'\",./<>?")
        elif opt == "--list":
            add_set(arg)
        elif opt == "-c":
            CONF_capitalize = True
        elif opt == "-w":
            CONF_singleWord = arg

def main():
    parse_args()
    
    if CONF_singleWord:
        process_transmute(CONF_singleWord)
        return

    FILE = sys.stdin if CONF_infile == '-' else open(CONF_infile, 'r')
    for line in FILE:
        process_transmute(line.strip())

def process_transmute(word):
    if CONF_Debug:
        print(f"Processing word: {word}")
    if CONF_AddSet:
        transmute_edge_insert(word)
    else:
        transmute_caps(word)

def transmute_edge_insert(word):
    if CONF_NumEdgeInsert > 0:
        transmute(word, transmute_insert)

def transmute_insert(word):
    if CONF_NumInsert > 0:
        transmute(word, transmute_prepend)

def transmute_prepend(word):
    if CONF_NumPrepend > 0:
        transmute(word, transmute_append)

def transmute_append(word):
    if CONF_NumAppend > 0:
        transmute(word, transmute_caps)

def transmute_caps(word):
    if CONF_capitalize:
        print(word.capitalize())
    else:
        print(word)

if __name__ == "__main__":
    main()
