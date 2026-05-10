#!/bin/bash

if [ -d "output/html_book" ]; then
    rm -rf output/html_book
fi

mkdir -p output/html_book

INPUT_DIR="manuscript_mgh"
OUTPUT_DIR="output"
CHROME_PATH="/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"

# Build a single HTML file from all .md files
pandoc.exe manuscript_mgh/*.md -o $OUTPUT_DIR/html_book/book.html -s -f commonmark+pipe_tables

# Copy shared stylesheet and replace inline <style> blocks with a <link> tag
cp styles.css "$OUTPUT_DIR/html_book/styles.css"
python replace_css.py "$OUTPUT_DIR/html_book/"*.html

# TODO: Make Table of Contents have links
# TODO: Make all URLs have clickable links

# Then, use Chrome to convert .html file to .pdf
pdf_path=$(cygpath -w "$PWD/$OUTPUT_DIR/html_book/book.pdf")
html_path=$(cygpath -w "$PWD/$OUTPUT_DIR/html_book/book.html")
"$CHROME_PATH" --headless --print-to-pdf="$pdf_path" "$html_path"
