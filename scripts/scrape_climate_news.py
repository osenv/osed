#!/usr/bin/env python3
"""
scrape_climate_news.py
======================

Discover and download articles relevant to the "AI & Climate" project from
State of the Planet, the Columbia Climate School news site
(https://news.climate.columbia.edu).

The site runs on WordPress, so this script talks to the WordPress REST API
(/wp-json/wp/v2/...) rather than scraping fragile HTML.

Discovery is **taxonomy-first**: it resolves the site's own editorial tags
(e.g. "artificial intelligence", "machine learning") to their term IDs, then
pulls the posts carrying those tags. This is far more precise than free-text
search, which on a climate-news site matches almost everything (the words
"energy", "water", "climate" appear nearly everywhere). Free-text scoring is
kept only to *rank* the tagged corpus, never to decide membership.

If the REST API is unreachable it falls back to the site's RSS feed (recent
posts, unfiltered — clearly a degraded mode).

For each matching article it writes:
  - index.json / index.csv  : a catalog of matches (title, url, date, tags, score)
  - articles/<slug>-<id>.md  : the full article text (only with --download)

The <id> suffix guarantees distinct posts can't overwrite each other on a slug
collision.

Only the standard library plus `requests` is required:
    pip install requests
`defusedxml` is recommended (hardens the untrusted-RSS fallback): pip install defusedxml

Politeness: the bot identifies itself in the User-Agent with a contact address.
Set it via the CLIMATE_NEWS_CONTACT environment variable (or --contact); the
address is never hardcoded in this file. Example:
    export CLIMATE_NEWS_CONTACT="you@example.edu"

Examples
--------
    # Default: pull posts tagged with the project's AI themes, save a catalog
    python scrape_climate_news.py

    # Also download the full text of each match
    python scrape_climate_news.py --download

    # Custom tags + categories, only posts since 2024, plus an opt-in free-text pass
    python scrape_climate_news.py \
        --tags "artificial intelligence" "machine learning" "data centers" \
        --categories "climate" \
        --since 2024-01-01 \
        --search \
        --download

This script only reads publicly available content. It identifies itself in the
User-Agent, throttles requests, and backs off on errors to stay polite.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

BASE_URL = "https://news.climate.columbia.edu"
API_POSTS = f"{BASE_URL}/wp-json/wp/v2/posts"
API_TAGS = f"{BASE_URL}/wp-json/wp/v2/tags"
API_CATEGORIES = f"{BASE_URL}/wp-json/wp/v2/categories"
RSS_FEED = f"{BASE_URL}/feed/"

# The contact address embedded in the User-Agent is read from the environment
# (or --contact), never hardcoded, so personal details stay out of the repo.
CONTACT_ENV_VAR = "CLIMATE_NEWS_CONTACT"
PLACEHOLDER_CONTACT = f"unset — set {CONTACT_ENV_VAR} or pass --contact"


def resolve_contact(cli_contact: str | None = None) -> str:
    """Resolve the contact address: --contact > env var > placeholder."""
    contact = cli_contact or os.environ.get(CONTACT_ENV_VAR) or ""
    contact = contact.strip()
    if not contact:
        print(
            f"  ! no contact configured; set the {CONTACT_ENV_VAR} environment "
            f"variable (or pass --contact) so the site operator can reach you.",
            file=sys.stderr,
        )
        return PLACEHOLDER_CONTACT
    return contact


def build_user_agent(contact: str) -> str:
    return (
        "ClimateNewsResearchBot/1.0 "
        f"(+research aggregation for AI-and-climate project; contact: {contact})"
    )


# Default editorial tags to pull. These are the project's AI hooks; the corpus
# is the union of posts carrying any of them. Tags are resolved by name against
# the site's taxonomy, so near-matches are reported and unknown ones are skipped.
# (A "data centers" tag was tried but does not exist on the site; add the real
# name via --tags if you find it.)
DEFAULT_TAGS = [
    "artificial intelligence",
    "machine learning",
]

# Categories are broader than tags; empty by default to keep precision high.
DEFAULT_CATEGORIES: list[str] = []

# Terms used ONLY to rank the tagged corpus (and for the opt-in --search pass);
# they do not decide membership. These are AI/ML vocabulary, NOT generic climate
# words: every article here is already on a climate site and already AI-tagged,
# so terms like "carbon"/"energy" don't measure how *central* AI is — they just
# reward length. The abbreviations "AI"/"ML" matter because the articles use them
# far more than the spelled-out phrases. Scoring is word-boundary aware, so "AI"
# does not match "rain"/"available".
DEFAULT_QUERIES = [
    "artificial intelligence",
    "AI",
    "machine learning",
    "ML",
    "neural network",
    "deep learning",
    "algorithm",
    "generative",
    "large language model",
    "data center",
]

# Per-field weights used when scoring how relevant an article is.
SCORE_WEIGHTS = {"title": 5, "excerpt": 2, "content": 1}

# A page worth of results per API call (WordPress caps this at 100).
PER_PAGE = 100

# Fields requested for each post. tags/categories give per-article provenance.
POST_FIELDS = "id,slug,link,date,title,excerpt,content,tags,categories"


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Article:
    id: int
    title: str
    url: str
    date: str
    slug: str
    excerpt: str = ""
    content: str = ""
    # Why this article is in the corpus: the tag/category names (or, in --search
    # mode, the query strings) that surfaced it.
    matched: set[str] = field(default_factory=set)
    score: int = 0

    def to_row(self) -> dict:
        """Flat dict for CSV / JSON index output (omits full content body)."""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "date": self.date,
            "score": self.score,
            "matched": "; ".join(sorted(self.matched)),
        }


# --------------------------------------------------------------------------- #
# HTML helpers
# --------------------------------------------------------------------------- #

class _TextExtractor(HTMLParser):
    """Minimal HTML -> plain text, so we avoid a BeautifulSoup dependency."""

    _SKIP = {"script", "style"}
    _BLOCK = {"p", "br", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skipping = False

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skipping = True
        elif tag in self._BLOCK:
            self._chunks.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP:
            self._skipping = False
        elif tag in self._BLOCK:
            self._chunks.append("\n")

    def handle_data(self, data):
        if not self._skipping:
            self._chunks.append(data)

    def text(self) -> str:
        raw = "".join(self._chunks)
        raw = html.unescape(raw)
        # Collapse runs of whitespace/newlines into something readable.
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
        return raw.strip()


def html_to_text(raw_html: str) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(raw_html or "")
    except Exception:
        # If parsing chokes, fall back to a crude tag strip.
        return html.unescape(re.sub(r"<[^>]+>", " ", raw_html or "")).strip()
    return parser.text()


# --------------------------------------------------------------------------- #
# HTTP session with polite retry/backoff
# --------------------------------------------------------------------------- #

def build_session(user_agent: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent, "Accept": "application/json"})
    return session


def get_with_retry(
    session: requests.Session,
    url: str,
    params: dict | None = None,
    *,
    max_retries: int = 4,
    base_delay: float = 1.0,
    timeout: float = 30.0,
) -> requests.Response | None:
    """GET with exponential backoff. Returns None on persistent failure."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(url, params=params, timeout=timeout)
        except requests.RequestException as exc:
            wait = base_delay * (2 ** (attempt - 1))
            print(f"  ! request error ({exc}); retrying in {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)
            continue

        if resp.status_code == 200:
            return resp
        if resp.status_code == 404:
            return resp  # caller decides what an empty page means
        if resp.status_code in (429, 500, 502, 503, 504):
            wait = base_delay * (2 ** (attempt - 1))
            print(
                f"  ! HTTP {resp.status_code} from server; backing off {wait:.0f}s",
                file=sys.stderr,
            )
            time.sleep(wait)
            continue

        print(f"  ! unexpected HTTP {resp.status_code} for {url}", file=sys.stderr)
        return resp

    print(f"  ! giving up on {url} after {max_retries} retries", file=sys.stderr)
    return None


# --------------------------------------------------------------------------- #
# Post -> Article construction
# --------------------------------------------------------------------------- #

def post_to_article(
    post: dict,
    *,
    term_names: dict[int, str] | None = None,
) -> Article:
    """Build an Article from a WordPress post payload.

    `term_names` maps resolved tag/category IDs to their display names; the
    article's `matched` set records which of those terms it actually carries,
    giving honest provenance ("this is here because it's tagged X").
    """
    term_names = term_names or {}
    carried_ids = (post.get("tags") or []) + (post.get("categories") or [])
    matched = {term_names[i] for i in carried_ids if i in term_names}
    return Article(
        id=post.get("id", 0),
        title=html.unescape((post.get("title") or {}).get("rendered", "")).strip(),
        url=post.get("link", ""),
        date=post.get("date", ""),
        slug=post.get("slug", ""),
        excerpt=html_to_text((post.get("excerpt") or {}).get("rendered", "")),
        content=html_to_text((post.get("content") or {}).get("rendered", "")),
        matched=matched,
    )


# --------------------------------------------------------------------------- #
# Taxonomy resolution + taxonomy-filtered fetch (the primary path)
# --------------------------------------------------------------------------- #

def resolve_terms(
    session: requests.Session,
    endpoint: str,
    names: Iterable[str],
    *,
    label: str,
) -> dict[int, dict]:
    """Resolve tag/category names to term records. Returns {id: term}.

    Unknown names are reported and skipped (never silently guessed). When a
    search returns several candidates, prefer an exact name/slug match, else
    the most-used term (highest post count).
    """
    resolved: dict[int, dict] = {}
    for name in names:
        resp = get_with_retry(
            session,
            endpoint,
            {"search": name, "per_page": PER_PAGE, "_fields": "id,name,slug,count"},
        )
        if resp is None or resp.status_code != 200:
            print(f"  ! could not query {label} for {name!r}", file=sys.stderr)
            continue
        try:
            matches = resp.json()
        except ValueError:
            matches = []
        if not isinstance(matches, list) or not matches:
            print(f"  ! no {label} found matching {name!r} — skipped", file=sys.stderr)
            continue

        wanted_slug = slugify(name)
        exact = [
            m for m in matches
            if m.get("name", "").lower() == name.lower()
            or m.get("slug", "").lower() == wanted_slug
        ]
        chosen = exact[0] if exact else max(matches, key=lambda m: m.get("count", 0))
        resolved[chosen["id"]] = chosen
        note = "" if exact else "  (nearest match — verify)"
        print(
            f"    {label}: {name!r} -> #{chosen['id']} "
            f"{chosen.get('name', '')!r} ({chosen.get('count', 0)} posts){note}"
        )
    return resolved


def fetch_posts_by_terms(
    session: requests.Session,
    param: str,
    term_ids: Iterable[int],
    term_names: dict[int, str],
    *,
    since: str | None,
    delay: float,
) -> list[Article]:
    """Page through posts filtered by a taxonomy (param='tags' or 'categories').

    Multiple IDs are OR-ed by the WordPress API, so this returns the union of
    posts carrying any of the given terms.
    """
    ids = list(term_ids)
    if not ids:
        return []

    articles: list[Article] = []
    page = 1
    while True:
        params = {
            param: ",".join(str(i) for i in ids),
            "per_page": PER_PAGE,
            "page": page,
            "_fields": POST_FIELDS,
            "orderby": "date",
        }
        if since:
            params["after"] = f"{since}T00:00:00"

        resp = get_with_retry(session, API_POSTS, params)
        if resp is None or resp.status_code != 200:
            break
        try:
            batch = resp.json()
        except ValueError:
            print(f"  ! non-JSON response paging {param}", file=sys.stderr)
            break
        if not isinstance(batch, list) or not batch:
            break

        for post in batch:
            articles.append(post_to_article(post, term_names=term_names))

        total_pages = int(resp.headers.get("X-WP-TotalPages", page))
        if page >= total_pages:
            break
        page += 1
        time.sleep(delay)

    return articles


# --------------------------------------------------------------------------- #
# Free-text search (opt-in only, via --search; never decides membership alone)
# --------------------------------------------------------------------------- #

def search_via_api(
    session: requests.Session,
    query: str,
    *,
    since: str | None,
    delay: float,
    max_pages: int = 5,
) -> list[Article]:
    """Search posts for one query term (relevance-ordered).

    Capped at `max_pages` because the WordPress search is loose (substring /
    OR-of-words), so a broad term like "AI" can match nearly the whole archive.
    Results are relevance-ordered, so the cap keeps the strongest matches; the
    local score gate (search_min_score) then decides membership.
    """
    articles: list[Article] = []
    page = 1
    while True:
        params = {
            "search": query,
            "per_page": PER_PAGE,
            "page": page,
            "_fields": POST_FIELDS,
            "orderby": "relevance",
        }
        if since:
            params["after"] = f"{since}T00:00:00"

        resp = get_with_retry(session, API_POSTS, params)
        if resp is None or resp.status_code != 200:
            break
        try:
            batch = resp.json()
        except ValueError:
            print(f"  ! non-JSON response for query {query!r}", file=sys.stderr)
            break
        if not isinstance(batch, list) or not batch:
            break

        for post in batch:
            art = post_to_article(post)
            art.matched = {f"search:{query}"}
            articles.append(art)

        total_pages = int(resp.headers.get("X-WP-TotalPages", page))
        if page >= total_pages:
            break
        if page >= max_pages:
            print(
                f"  ! '{query}' search truncated at {max_pages}/{total_pages} "
                f"pages (relevance-ordered; the rest are weaker matches).",
                file=sys.stderr,
            )
            break
        page += 1
        time.sleep(delay)

    return articles


# --------------------------------------------------------------------------- #
# RSS fallback (used only if the REST API is unreachable)
# --------------------------------------------------------------------------- #

def fetch_via_rss(session: requests.Session) -> list[Article]:
    """Parse the site RSS feed as a fallback. Returns recent posts (unfiltered).

    RSS is untrusted web content, so the XML is parsed with defusedxml when
    available (hardened against XXE / billion-laughs entity-expansion attacks).
    If defusedxml is not installed we degrade to the stdlib parser but warn,
    since the stdlib parser is vulnerable to those attacks.
    """
    try:
        from defusedxml.ElementTree import fromstring as xml_fromstring
        from defusedxml.ElementTree import ParseError as XMLParseError
    except ModuleNotFoundError:
        import xml.etree.ElementTree as _ET

        xml_fromstring = _ET.fromstring
        XMLParseError = _ET.ParseError
        print(
            "  ! defusedxml not installed; parsing untrusted RSS with the stdlib "
            "XML parser, which is vulnerable to entity-expansion attacks. "
            "Harden this path with: pip install defusedxml",
            file=sys.stderr,
        )

    print("  > falling back to RSS feed (recent posts, unfiltered)", file=sys.stderr)
    resp = get_with_retry(session, RSS_FEED)
    if resp is None or resp.status_code != 200:
        return []

    try:
        root = xml_fromstring(resp.content)
    except XMLParseError as exc:
        print(f"  ! could not parse RSS ({exc})", file=sys.stderr)
        return []

    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    articles: list[Article] = []
    for item in root.iterfind(".//item"):
        link = (item.findtext("link") or "").strip()
        title = html.unescape((item.findtext("title") or "").strip())
        pub = item.findtext("pubDate") or ""
        desc = html_to_text(item.findtext("description") or "")
        body = html_to_text(item.findtext("content:encoded", default="", namespaces=ns))
        slug = urlparse(link).path.strip("/").split("/")[-1] or title[:40]
        articles.append(
            Article(
                id=abs(hash(link)) % (10**9),
                title=title,
                url=link,
                date=pub,
                slug=slug,
                excerpt=desc,
                content=body,
                matched={"rss-fallback"},
            )
        )
    return articles


# --------------------------------------------------------------------------- #
# Relevance scoring & merging
# --------------------------------------------------------------------------- #

def score_article(article: Article, queries: Iterable[str]) -> int:
    """Weighted, word-boundary count of query terms across title/excerpt/content.

    Used only to RANK the corpus, not to filter it. Matching is whole-phrase and
    word-boundary aware (regex \\b...\\b), so "data center" does not score on a
    bare "water", and the short token "AI" matches standalone occurrences (incl.
    "AI's") without firing on "rain" or "available".
    """
    fields = (
        (article.title.lower(), SCORE_WEIGHTS["title"]),
        (article.excerpt.lower(), SCORE_WEIGHTS["excerpt"]),
        (article.content.lower(), SCORE_WEIGHTS["content"]),
    )
    score = 0
    for query in queries:
        term = query.lower().strip()
        if not term:
            continue
        pattern = r"\b" + re.escape(term) + r"\b"
        for text, weight in fields:
            score += len(re.findall(pattern, text)) * weight
    return score


def merge(found: list[Article]) -> dict[int, Article]:
    """De-duplicate by post id, unioning the terms that surfaced each one."""
    merged: dict[int, Article] = {}
    for art in found:
        if art.id in merged:
            merged[art.id].matched |= art.matched
        else:
            merged[art.id] = art
    return merged


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", text)[:80] or "untitled"


def write_index(
    articles: list[Article],
    output_dir: Path,
    *,
    tags_used: list[str],
    categories_used: list[str],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [a.to_row() for a in articles]

    json_path = output_dir / "index.json"
    json_path.write_text(
        json.dumps(
            {
                "source": BASE_URL,
                "generated": datetime.now().isoformat(timespec="seconds"),
                "tags_used": tags_used,
                "categories_used": categories_used,
                "count": len(rows),
                "articles": rows,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    csv_path = output_dir / "index.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["id", "title", "url", "date", "score", "matched"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote index of {len(rows)} articles:")
    print(f"  {json_path}")
    print(f"  {csv_path}")


def write_articles(articles: list[Article], output_dir: Path) -> None:
    art_dir = output_dir / "articles"
    art_dir.mkdir(parents=True, exist_ok=True)
    for art in articles:
        # The <id> suffix makes the filename unique, so distinct posts that
        # slugify to the same string cannot overwrite each other.
        stem = slugify(art.title) or art.slug or "untitled"
        name = f"{stem}-{art.id}.md"
        body = (
            f"# {art.title}\n\n"
            f"- URL: {art.url}\n"
            f"- Date: {art.date}\n"
            f"- Relevance score: {art.score}\n"
            f"- Matched: {', '.join(sorted(art.matched))}\n\n"
            f"---\n\n"
            f"{art.content}\n"
        )
        (art_dir / name).write_text(body, encoding="utf-8")
    print(f"  Saved {len(articles)} article bodies to {art_dir}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Pull AI-&-climate articles from news.climate.columbia.edu by tag."
    )
    p.add_argument(
        "--tags",
        nargs="+",
        default=DEFAULT_TAGS,
        help="Editorial tags to pull (default: the project's AI themes).",
    )
    p.add_argument(
        "--categories",
        nargs="+",
        default=DEFAULT_CATEGORIES,
        help="Categories to pull (default: none — tags are more precise).",
    )
    p.add_argument(
        "--queries",
        nargs="+",
        default=DEFAULT_QUERIES,
        help="Phrases used to RANK the corpus (and for --search). Not a filter.",
    )
    p.add_argument(
        "--search",
        action="store_true",
        help="Opt-in: also run a free-text search for --queries and merge the "
        "results (lower precision; tagged via 'search:<term>'). Untagged hits "
        "must clear --search-min-score to be kept.",
    )
    p.add_argument(
        "--search-min-score",
        type=int,
        default=5,
        help="Minimum score for an UNTAGGED --search result to be kept; tagged "
        "articles are always kept regardless. Default: 5.",
    )
    p.add_argument(
        "--search-max-pages",
        type=int,
        default=5,
        help="Max result pages to fetch per --search query (relevance-ordered). "
        "Bounds load from broad terms like 'AI'. Default: 5.",
    )
    p.add_argument(
        "--since",
        default=None,
        help="Only include posts published on/after this date (YYYY-MM-DD).",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/references/climate-news"),
        help="Directory to write the index (and articles, with --download).",
    )
    p.add_argument(
        "--contact",
        default=None,
        help=(
            "Contact address for the polite User-Agent. Overrides the "
            f"{CONTACT_ENV_VAR} environment variable if set."
        ),
    )
    p.add_argument(
        "--max-results",
        type=int,
        default=0,
        help="Cap the number of articles kept (0 = no cap).",
    )
    p.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="Drop articles scoring below this (default: 0 — keep all tagged).",
    )
    p.add_argument(
        "--download",
        action="store_true",
        help="Also save each matching article's full text as a .md file.",
    )
    p.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to pause between requests, to stay polite (default: 1.0).",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    contact = resolve_contact(args.contact)
    session = build_session(build_user_agent(contact))

    # 1) Resolve the requested tags/categories to term IDs (skip unknowns).
    print(f"Resolving taxonomy on {BASE_URL} ...")
    tag_terms = resolve_terms(session, API_TAGS, args.tags, label="tag")
    cat_terms = resolve_terms(session, API_CATEGORIES, args.categories, label="category")
    term_names = {tid: t.get("name", "") for tid, t in {**tag_terms, **cat_terms}.items()}

    if not tag_terms and not cat_terms and not args.search:
        print(
            "\nNo tags or categories resolved, and --search not given. Nothing to "
            "fetch. Check the names with --tags, or add --search.",
            file=sys.stderr,
        )
        return 1

    # 2) Pull the posts carrying those terms (the corpus).
    found: list[Article] = []
    if tag_terms:
        print(f"\nFetching posts for {len(tag_terms)} tag(s)...")
        found += fetch_posts_by_terms(
            session, "tags", tag_terms, term_names, since=args.since, delay=args.delay
        )
    if cat_terms:
        print(f"Fetching posts for {len(cat_terms)} category(ies)...")
        found += fetch_posts_by_terms(
            session, "categories", cat_terms, term_names,
            since=args.since, delay=args.delay,
        )

    # 3) Optional, lower-precision free-text pass (explicitly opt-in).
    if args.search:
        print(f"\n--search: free-text pass over {len(args.queries)} phrase(s)...")
        for query in args.queries:
            print(f"  - {query!r}")
            found += search_via_api(
                session, query, since=args.since, delay=args.delay,
                max_pages=args.search_max_pages,
            )
            time.sleep(args.delay)

    # 4) If the API gave us nothing at all, try the RSS feed (degraded mode).
    if not found:
        found = fetch_via_rss(session)

    merged = merge(found)
    for art in merged.values():
        art.score = score_article(art, args.queries)

    def is_editorial(a: Article) -> bool:
        # True if a tag/category surfaced this article (trusted membership), as
        # opposed to only the free-text search ("search:...") or RSS fallback.
        return any(
            not (m.startswith("search:") or m == "rss-fallback")
            for m in a.matched
        )

    def keep(a: Article) -> bool:
        if a.score < args.min_score:
            return False
        if is_editorial(a):
            return True  # editorial tag is trusted; never gated by the search floor
        return a.score >= args.search_min_score  # search-only must prove relevance

    kept = [a for a in merged.values() if keep(a)]
    if args.search:
        n_search = sum(1 for a in merged.values() if not is_editorial(a))
        n_search_kept = sum(1 for a in kept if not is_editorial(a))
        print(
            f"\n--search: kept {n_search_kept} of {n_search} untagged candidates "
            f"(score >= {args.search_min_score}); the rest were below the floor.",
            file=sys.stderr,
        )

    articles = kept
    # Rank by score, then most-recent first for ties.
    articles.sort(key=lambda a: (a.score, a.date), reverse=True)
    if args.max_results > 0:
        articles = articles[: args.max_results]

    if not articles:
        print("\nNo matching articles found.", file=sys.stderr)
        return 1

    write_index(
        articles,
        args.output_dir,
        tags_used=[t.get("name", "") for t in tag_terms.values()],
        categories_used=[c.get("name", "") for c in cat_terms.values()],
    )
    if args.download:
        write_articles(articles, args.output_dir)

    print("\nTop matches:")
    for art in articles[:10]:
        print(f"  [{art.score:>4}] {art.title}")
        print(f"         {art.url}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
