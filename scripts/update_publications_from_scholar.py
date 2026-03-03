#!/usr/bin/env python3
"""
Update publications from Google Scholar to BibTeX.

Fetches your Google Scholar publications and writes them to a BibTeX file.
Uses your scholar_userid from _data/socials.yml (or pass as argument).

Usage:
    python scripts/update_publications_from_scholar.py              # Uses socials.yml
    python scripts/update_publications_from_scholar.py M5XHvEYAAAAJ  # Explicit ID
    python scripts/update_publications_from_scholar.py --merge   # Merge with existing papers.bib

Requirements:
    pip install scholarly
"""

import argparse
import re
import sys
from pathlib import Path

# Project root (parent of scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOCIALS_FILE = PROJECT_ROOT / "_data" / "socials.yml"
BIB_FILE = PROJECT_ROOT / "_bibliography" / "papers.bib"


def get_scholar_id_from_socials():
    """Extract scholar_userid from _data/socials.yml."""
    if not SOCIALS_FILE.exists():
        return None
    content = SOCIALS_FILE.read_text(encoding="utf-8")
    match = re.search(r"scholar_userid:\s*(\S+)", content)
    if match:
        return match.group(1).strip()
    return None


def fetch_publications(scholar_id: str):
    """Fetch publications from Google Scholar using the scholarly library."""
    try:
        from scholarly import scholarly
    except ImportError:
        print("Error: Install the scholarly package:")
        print("  pip install scholarly")
        sys.exit(1)

    print(f"Fetching publications for author ID: {scholar_id}")
    print("This may take a minute...")

    author = scholarly.search_author_id(scholar_id, filled=False)
    author = scholarly.fill(author, sections=["publications"], sortby="year", publication_limit=0)

    bib_entries = []
    seen_titles = set()

    for i, pub in enumerate(author.get("publications", [])):
        try:
            pub_filled = scholarly.fill(pub)
            bib_str = scholarly.bibtex(pub_filled)
            if bib_str:
                # Deduplicate by normalizing title (rough check)
                title_match = re.search(r"title\s*=\s*\{([^}]+)\}", bib_str)
                title = title_match.group(1).strip().lower() if title_match else ""
                if title and title in seen_titles:
                    continue
                if title:
                    seen_titles.add(title)
                bib_entries.append(bib_str.strip())
                print(f"  [{i+1}] {pub_filled.get('bib', {}).get('title', '?')[:60]}...")
        except Exception as e:
            print(f"  Warning: Could not fetch publication: {e}")
            continue

    return "\n\n".join(bib_entries)


def _extract_bib_entries(bib_text: str):
    """Split BibTeX text into (key, full_entry) pairs."""
    entries = []
    current = []
    in_entry = False
    for line in bib_text.splitlines():
        if line.strip().startswith("@"):
            if current:
                full = "\n".join(current)
                key_match = re.search(r"@\w+\{([^,]+),", full)
                if key_match:
                    entries.append((key_match.group(1), full))
            current = [line]
            in_entry = True
        elif in_entry:
            current.append(line)
    if current:
        full = "\n".join(current)
        key_match = re.search(r"@\w+\{([^,]+),", full)
        if key_match:
            entries.append((key_match.group(1), full))
    return entries


def merge_with_existing(new_bib: str, existing_path: Path) -> str:
    """Merge new Scholar entries with existing papers.bib, preferring existing for duplicates."""
    if not existing_path.exists():
        return new_bib

    existing = existing_path.read_text(encoding="utf-8")
    existing_entries = _extract_bib_entries(existing)
    existing_keys = {k for k, _ in existing_entries}

    new_entries = _extract_bib_entries(new_bib)
    to_add = [entry for key, entry in new_entries if key not in existing_keys]

    if not to_add:
        return existing

    merged = existing.rstrip()
    if not merged.endswith("\n"):
        merged += "\n"
    merged += "\n\n" + "\n\n".join(to_add) + "\n"
    return merged


def main():
    parser = argparse.ArgumentParser(description="Update publications from Google Scholar")
    parser.add_argument(
        "scholar_id",
        nargs="?",
        default=None,
        help="Google Scholar author ID (e.g. M5XHvEYAAAAJ). Default: from _data/socials.yml",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge with existing papers.bib instead of overwriting",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: _bibliography/papers_scholar.bib if not --merge)",
    )
    args = parser.parse_args()

    scholar_id = args.scholar_id or get_scholar_id_from_socials()
    if not scholar_id:
        print("Error: No Google Scholar ID found.")
        print("  Add scholar_userid: YOUR_ID to _data/socials.yml")
        print("  Or pass it as argument: python update_publications_from_scholar.py M5XHvEYAAAAJ")
        sys.exit(1)

    bib_content = fetch_publications(scholar_id)

    if args.merge:
        bib_content = merge_with_existing(bib_content, BIB_FILE)
        out_path = Path(args.output or str(BIB_FILE))
    else:
        out_path = Path(args.output or str(BIB_FILE.parent / "papers_scholar.bib"))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(bib_content, encoding="utf-8")

    num_entries = len(_extract_bib_entries(bib_content))
    print(f"\nDone! Wrote {num_entries} entries to {out_path}")
    if not args.merge and out_path != BIB_FILE:
        print("\nTo use: review papers_scholar.bib and merge desired entries into papers.bib")
        print("Or run with --merge to append new entries to papers.bib automatically.")


if __name__ == "__main__":
    main()
