# webarchive

Webarchive is command line web pages extractor which producesa readable
contents of requested web pages. It works with URLs, local file paths and
standard input.

## Features

The following commands show how webarchive can be feeded with web page
content:

```
$ webarchive https://example.com

$ webarchive "$HOME/index.html"

$ webarchive - < "$HOME/index.html"
```

It then outputs text in various formats:

- Markdown
- HTML
- Plain text

If readability algorithms don't work for a particular web page, webarchive
can use an external command which provides textual dumps of pages. Examples
of such programs are command line web browsers like links or w3m.

```
$ webarchive https://example.com -t dump --dump-cmd "w3m -dump"
```

Webarchive automatically detects and provides contextualized informations
like page titles, which can be prepended in YAML Front Matter. It's useful if
webarchive output is later processed by other tools which understand YML
Front Matter, such as pandoc:

```
$ webarchive https://example.com -t md | \
    pandoc -f markdown --standalone > article.html
$ ebook-convert article.html article.epub  # ebook-convert is part of Calibre
```

Additionally, a GUI wrapper is provided, which is also script-friendly as it
prints all saved files to standard output.

```bash
#!/bin/sh

for f in `webarchive-qt`; do
  pandoc "$f" --standalone > article.html
  ebook-convert article.html article.epub
  mutt -a "article.epub" -s "Good article I found" -- alice@example.com
  rm -f "article.html" "article.epub" "$f"
done
```

## Installation

```
$ pip3 install webarchive
```

To install dependencies for GUI wrapper (webarchive-qt):

```
$ pip3 install webarchive[gui]
```

You can use tools such as pipx and pipsi to automatically install webarchive
and its dependencies to isolated environment:

```
$ pipx install 'webarchive[gui]'
```
