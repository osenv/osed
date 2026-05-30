# scripts/

Standalone utility scripts that support OSED research but are **not** part of the
skills, templates, or the regulatory connector. Nothing here changes a design
invariant (see `CLAUDE.md`).

## `scrape_climate_news.py`

Discovers and downloads articles relevant to the "AI & Climate" project from
[State of the Planet](https://news.climate.columbia.edu), the Columbia Climate
School news site.

It talks to the site's WordPress REST API (`/wp-json/wp/v2/...`) rather than
scraping HTML — more stable — and falls back to the RSS feed if the API is
unavailable.

**Discovery is taxonomy-first.** It resolves the site's own editorial tags
(`artificial intelligence`, `machine learning`) to their term IDs, then pulls
the posts carrying those tags. This is far more precise than free-text search:
on a climate-news site the words *energy*, *water*, *climate* appear nearly
everywhere, so a keyword search matches almost the entire archive.

Free-text scoring is kept only to **rank** the tagged corpus, never to decide
membership — and it ranks on AI/ML vocabulary (incl. the `AI`/`ML`
abbreviations, matched on word boundaries), not generic climate words, since
every article here is already climate-focused and AI-tagged. A lower-precision
free-text *search* pass is available behind `--search`.

By default it writes into the committed corpus at `docs/references/climate-news/`:

- `index.json` / `index.csv` — catalog of matches (title, url, date, tags, score)
- `articles/<slug>-<id>.md` — full article text (only with `--download`). The
  `<id>` suffix guarantees distinct posts can't overwrite each other.

### Install

```bash
pip install requests        # required
pip install defusedxml      # recommended: hardens the untrusted-RSS fallback
```

`defusedxml` is optional but recommended: the RSS fallback parses XML served by
a remote site (untrusted data), and `defusedxml` guards against entity-expansion
attacks. Without it the script still runs, using the stdlib parser, and warns.

### Quick start

```bash
# Set a contact address so the bot can identify itself politely.
# This is read from the environment, never hardcoded in the repo.
export CLIMATE_NEWS_CONTACT="you@example.edu"

# Pull posts tagged with the project's AI themes; download full text
python scripts/scrape_climate_news.py --download
```

### Useful options

```bash
python scripts/scrape_climate_news.py \
    --tags "artificial intelligence" "machine learning" "data centers" \
    --categories "climate" \
    --since 2024-01-01 \
    --search \
    --output-dir ./data/climate_news \
    --contact you@example.edu \
    --download
```

- `--tags` / `--categories` choose which editorial terms define the corpus.
  Unknown names are reported and skipped (never silently guessed); when several
  candidates match, the script prefers an exact name/slug match and otherwise
  the most-used term, flagging it as a nearest match to verify.
- `--queries` are the phrases used to **rank** the corpus (and to drive
  `--search`); they do not filter it.
- `--search` adds an opt-in, lower-precision free-text pass, merged in and
  labelled `search:<term>` so its provenance is visible.
- `--contact` overrides the `CLIMATE_NEWS_CONTACT` environment variable.
- `--delay` (default `1.0`s) throttles requests to stay polite; raise it if needed.
- `--min-score` (default `0`, i.e. keep everything tagged) / `--max-results`.

### Polite-use notes

- The bot identifies itself in the `User-Agent` with the contact address above
  and throttles + backs off on errors. Keep `--delay` reasonable.
- This reads only publicly available content.
- It hasn't been smoke-tested against the live site from this environment (the
  domain isn't reachable here) — run it locally and report any endpoint that
  behaves differently than expected.
