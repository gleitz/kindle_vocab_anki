# merriam.py ---
#
# Filename: merriam.py
# Description:
# Author: Vidhyalakshmi Sundara Raman
# Created: Mon Nov  5 01:06:14 2018 (-0500)

# TODO:
# [ ] Lookup for queries with more than a word
# [X] Get usage examples for query
# [ ] Key in separate folder
#

# Test cases: hello, please, love

# Code:

import json
import argparse
import urllib.request
from urllib.parse import quote
import re

keyfile = open("keys.txt", 'r')
keys = keyfile.readline()


def define(query):
    print(f'Looking up {query}')
    definition = ''
    urlfrmt = "https://dictionaryapi.com/api/v3/references/collegiate/json/" + quote(query) + "?key=" + keys
    response = urllib.request.urlopen(urlfrmt)
    jsStruct = json.load(response)

    for meaning in jsStruct:
        if isinstance(meaning, str):
            definition += '\n' + meaning
            break
        definitions = meaning['shortdef']
        if meaning['meta']['id'] != query:
            definition += "\n"+meaning['meta']['id']
        try:
            definition += ' ('+meaning['fl']+')'
            for i, eachDef in enumerate(definitions, 1):
                definition += '\n' + str(i) + ". " + eachDef
        except KeyError:
            pass

    definition += "\nUsage"

    for usage in jsStruct:
        try:
            if isinstance(usage, str):
                definition += '\n' + usage
                break
            longdefs = usage['def']
            for i, eachDef in enumerate(longdefs, 1):
                if 'sseq' in eachDef:
                    # test[*][0][1]['dt'] - gives list of illustrations
                    for ill in eachDef['sseq']:
                        if 'dt' in ill[0][1]:
                            for illus in ill[0][1]['dt']:
                                if illus[0] == 'vis':
                                    # enumerate
                                    for ii in range(1, len(illus)):
                                        L = len(illus[ii])
                                        for jj in range(L):
                                            if 't' in illus[ii][jj]:
                                                # remove everything within braces before printing
                                                definition += '\n' + "* "+illus[ii][jj]['t']
        except KeyError:
            pass

    return definition.strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str)
    args = parser.parse_args()
    query = args.word
    print(define(query))
