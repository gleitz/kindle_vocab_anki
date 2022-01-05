#!/usr/bin/env python

import sys
import sqlite3
import argparse
import itertools
from datetime import datetime
from operator import itemgetter
from operator import attrgetter
from collections import namedtuple

from merriam import define

AnkiNote = namedtuple('AnkiNote', 'word usage definition timestamp')
DEFAULT_VOCAB_DB = '/Volumes/Kindle/system/vocabulary/vocab.db'


def get_vocab(vocab_db, _since=0):

    if isinstance(_since, datetime):
        since = int(_since.timestamp()) * 1000
    else:
        since = _since * 1000

    db = sqlite3.connect(vocab_db)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    sql = '''
        select WORDS.stem, WORDS.word, LOOKUPS.usage, BOOK_INFO.title, LOOKUPS.timestamp
        from LOOKUPS left join WORDS
        on WORDS.id = LOOKUPS.word_key
        left join BOOK_INFO
        on BOOK_INFO.id = LOOKUPS.book_key
        where LOOKUPS.timestamp > ?
        order by WORDS.stem, LOOKUPS.timestamp
    '''
    rows = cur.execute(sql, (since,)).fetchall()
    return rows


def make_notes(vocab, include_nodef=False):

    stems_no_def = set()
    notes = []
    # vocab is a list of db rows order by (stem, timestamp)
    for stem, entries in itertools.groupby(vocab, itemgetter('stem')):
        # Merge multiple usages into one.
        usage_all = ''
        usage_timestamp = None
        for entry in entries:
            word = entry['word']
            _usage = entry['usage'].replace(word, f'<strong>{word}</strong>').strip()
            usage = f'<blockquote>{_usage}<br><small>({entry["title"]})</small></blockquote>'
            usage_all += usage
            usage_timestamp = entry['timestamp']

        # Look up definition in dictionary
        try:
            definition = define(stem).replace('\n', '<br>').replace('{wi}', '<strong>').replace('{/wi}', '</strong>')
        except KeyError:
            stems_no_def.add(stem)
            if include_nodef:
                definition = None
            else:
                continue

        note = AnkiNote(stem, usage_all, definition, usage_timestamp)
        notes.append(note)

    if stems_no_def:
        print(f'WARNING: Some words cannot be found in dictionary:\n{stems_no_def}', file=sys.stderr)

    return notes


def output_anki_tsv(notes, output, sort=True):

    if sort:
        notes.sort(key=attrgetter('timestamp'), reverse=True)

    with output as f:
        for note in notes:
            line = f'{note.word}<br><p class="context">{note.usage}</p>\t<p class="context">{note.definition}</p>\n'
            f.write(line)


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--since', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), default=datetime.utcfromtimestamp(86400 * 2))  # Windows workaround
    argp.add_argument('--include-nodef', action='store_true', help='include words that have no definitions in dictionary')
    argp.add_argument('anki_tsv', type=argparse.FileType('w', encoding='utf-8'))
    args = argp.parse_args()
    vocab = get_vocab(DEFAULT_VOCAB_DB, _since=args.since)
    notes = make_notes(vocab, include_nodef=args.include_nodef)
    output_anki_tsv(notes, args.anki_tsv)
