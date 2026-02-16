#!/usr/bin/env python3
"""Fetch recent CS papers from arXiv RSS feed and save as JSON."""

import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime, timezone

RSS_URL = "http://rss.arxiv.org/rss/cs"


def fetch_papers():
    print(f"Fetching {RSS_URL}...")
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "arxivcards/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()

    root = ET.fromstring(data)
    channel = root.find("channel")
    pub_date = channel.findtext("pubDate", "")
    print(f"Feed date: {pub_date}")

    papers = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        title = " ".join(title.split())
        link = item.findtext("link", "")
        desc = item.findtext("description", "")
        creator = item.findtext("{http://purl.org/dc/elements/1.1/}creator", "")
        pub = item.findtext("pubDate", "")

        categories = [el.text for el in item.findall("category") if el.text]

        # Only keep papers with a cs.* category
        cs_cats = [c for c in categories if c.startswith("cs.")]
        if not cs_cats:
            continue

        # Extract abstract from description
        # Format: "arXiv:XXXX Announce Type: ... \nAbstract: ..."
        abstract = ""
        m = re.search(r"Abstract:\s*(.+)", desc, re.DOTALL)
        if m:
            abstract = " ".join(m.group(1).split())

        # Extract arXiv ID from link
        arxiv_id = link.split("/abs/")[-1] if "/abs/" in link else link

        # Parse authors
        authors = [a.strip() for a in creator.split(",") if a.strip()]

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors,
            "summary": abstract,
            "published": pub,
            "categories": categories,
            "primary_category": cs_cats[0],
            "abs_url": link,
        })

    return papers, pub_date


def main():
    papers, pub_date = fetch_papers()
    print(f"Found {len(papers)} CS papers.")

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "feed_date": pub_date,
        "count": len(papers),
        "papers": papers,
    }

    with open("papers.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Saved to papers.json")


if __name__ == "__main__":
    main()
