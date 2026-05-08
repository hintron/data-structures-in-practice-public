#!/bin/bash

if [ -d "output/html" ]; then
    rm -rf output/html
fi
if [ -d "output/pdf" ]; then
    rm -rf output/pdf
fi

mkdir -p output/html
mkdir -p output/pdf

INPUT_DIR="manuscript_mgh"
OUTPUT_DIR="output"
CHROME_PATH="/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"

# Create .html files from .md files
for file in $INPUT_DIR/*.md; do
    pandoc "$file" -o "$OUTPUT_DIR/html/$(basename "$file" .md).html" -s
done

# Copy shared stylesheet and replace inline <style> blocks with a <link> tag
cp styles.css "$OUTPUT_DIR/html/styles.css"
python replace_css.py "$OUTPUT_DIR/html/"*.html


# Then, use Chrome to convert .html files to .pdf
for file in $OUTPUT_DIR/html/*.html; do
    stem=$(basename "$file" .html)
    pdf_path=$(cygpath -w "$PWD/$OUTPUT_DIR/pdf/$stem.pdf")
    html_path=$(cygpath -w "$PWD/$file")
    "$CHROME_PATH" --headless --print-to-pdf="$pdf_path" "$html_path"
done
