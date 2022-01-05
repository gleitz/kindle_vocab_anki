# Export Kindle Vocabulary Builder Directly to Anki

Kindle Vocabulary Builder is useful, as it collects new words automatically when you read books. However, it has only two decks: "Learning" and "Mastered". It lacks a lot of functionalities found in professional flashcard software like Anki. Kindle Vocabulary Builder stores all the data in `/system/vocabulary/vocab.db` SQLite3 database. This repo directly extracts words from a connected Kindle's Vocabulary Builder, looks up definitions for the words from Merriam-Webster, and creates a file you an export to Anki.

## Usage

1. Sign up for an [API key](https://dictionaryapi.com/register/index) with Merriam-Webster (you want the `Collegiate Dictionary`). Place the key inside a file called `keys.txt`.
1. Run `./fetch_and_convert_vocab.py notes.tsv` to fetch all words from your Vocabulary Builder and export an Anki TSV.
1. You can now import the `notes.tsv` file into Anki.

## File Formats

*TSV* stands for [Tab-seperated vlues](https://en.wikipedia.org/wiki/Tab-separated_values). The fact that there are unlikely any `\t`s in dictionary definitions or book citations, makes TSV a better choice than CSV for both plain-text dictionaries and Anki notes.

The TSV Anki notes file has three columns: Stem, Usage, Definition. You can map them to whatever fields you like. The "Usage" and "Definition" columns are HTML, so remember to check "Allow HTML in fields" when importing into Anki. The "Usage" column contains all the citations in Kindle Vocabulary Builder, i.e. if you look up a word in different books, the usage sentences will be merged into one single Anki note.

## Templates and Styling

The templates and styling below make the rendered Anki cards very similar to their counterparts in Kindle Vocabulary Builder.

![](./Screenshot_AnkiDroid.png)

Front Template:

```HTML
<h1>{{Word}}</h1>
<hr>
{{Usage}}
```

Back Template:

```HTML
{{FrontSide}}
<hr>
{{Definition}}
```

Styling:

```CSS
h1 {
 text-align: center;
}
blockquote small:before {
 content: " -- ";
}
```

## External Links

- [Anki Web](https://ankiweb.net/)
- [AnkiDroid](https://play.google.com/store/apps/details?id=com.ichi2.anki&hl=en_US&gl=US)
- [AnkiApp iOS](https://apps.apple.com/us/app/ankiapp-flashcards/id689185915)
