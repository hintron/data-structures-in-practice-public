#!/usr/bin/env python3
"""
replace_css.py — Replace inline <style>...</style> blocks in HTML files
with a <link> to styles.css.

Usage:
    python replace_css.py output/html/*.html
    python replace_css.py output/html/chapter01.html output/html/chapter02.html

The script rewrites each file in-place. It expects styles.css to live in the
same directory as the HTML files being processed; if they are in different
directories you can override the href with --href.

Options:
    --href PATH    CSS href to use (default: styles.css)
    --dry-run      Print what would change without writing files
"""

import argparse
import os
import re
import sys


STYLE_PATTERN = re.compile(
    r'[ \t]*<style>\n.*?</style>\n?',
    re.DOTALL,
)


def replace_style(html: str, href: str) -> tuple[str, bool]:
    """Return (new_html, was_changed)."""
    link_tag = f'  <link rel="stylesheet" href="{href}" />\n'
    new_html, count = STYLE_PATTERN.subn(link_tag, html, count=1)
    return new_html, count > 0


def process_file(path: str, href: str, dry_run: bool) -> None:
    with open(path, encoding='utf-8') as fh:
        original = fh.read()

    new_content, changed = replace_style(original, href)

    if not changed:
        print(f'  SKIP  {path}  (no inline <style> block found)')
        return

    if dry_run:
        print(f'  DRY   {path}  (would replace inline style with link tag)')
        return

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new_content)

    print(f'  OK    {path}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Replace inline <style> blocks with a <link> to styles.css'
    )
    parser.add_argument(
        'files',
        nargs='+',
        metavar='FILE',
        help='HTML files to process (supports glob patterns on Unix; '
             'on Windows use quotes or pass explicit paths)',
    )
    parser.add_argument(
        '--href',
        default='styles.css',
        metavar='PATH',
        help='href value for the <link> tag (default: styles.css)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without writing files',
    )
    args = parser.parse_args()

    # Expand any glob patterns that the shell didn't expand (Windows)
    import glob
    expanded: list[str] = []
    for pattern in args.files:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            expanded.extend(matches)
        else:
            expanded.append(pattern)  # keep as-is; will fail with a clear error

    missing = [p for p in expanded if not os.path.isfile(p)]
    if missing:
        for p in missing:
            print(f'  ERROR {p}  (file not found)', file=sys.stderr)
        sys.exit(1)

    for path in expanded:
        process_file(path, args.href, args.dry_run)


if __name__ == '__main__':
    main()
