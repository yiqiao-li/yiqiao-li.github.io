# Scripts

## Update Publications from Google Scholar

Sync your publications from Google Scholar to BibTeX format.

### Setup

```bash
pip install scholarly
```

### Usage

**Option 1: Fetch to a new file (review before replacing)**

```bash
python scripts/update_publications_from_scholar.py
```

This writes to `_bibliography/papers_scholar.bib`. Review the file, then merge desired entries into `papers.bib` manually. Use this when you have custom fields (PDF links, abstracts, etc.) in your existing `papers.bib` that you want to keep.

**Option 2: Merge new entries into papers.bib**

```bash
python scripts/update_publications_from_scholar.py --merge
```

Fetches from Scholar and appends only entries whose citation keys don't already exist in `papers.bib`. Existing entries are unchanged.

**Option 3: Use a specific Scholar ID**

```bash
python scripts/update_publications_from_scholar.py M5XHvEYAAAAJ
```

By default, the script uses `scholar_userid` from `_data/socials.yml` (already set for this site).

### Notes

- **Rate limiting**: Google Scholar may block requests if you run the script too often. Wait a few minutes between runs. If blocked, try again later or use a proxy (see [scholarly docs](https://scholarly.readthedocs.io/)).
- **BibTeX quality**: Scholar's BibTeX can have typos or missing DOIs. You may need to refine entries manually.
- **Custom fields**: The script does not preserve custom fields like `pdf`, `abstract`, `selected` from existing entries. Use `--merge` to add only new publications while keeping your curated `papers.bib` intact.
