# arxivcards

A slideshow display of recent arXiv CS papers, designed for large public screens. Cycles through paper abstracts with QR codes linking to the full paper.

## Usage

Fetch the latest papers from the arXiv RSS feed:

```bash
python3 fetch_papers.py
```

Serve the display page:

```bash
python3 serve.py
```

Then open http://localhost:8080 in a browser.

## Keyboard controls

- **Space** — pause/resume auto-cycling
- **Left/Right arrows** — navigate between papers

## How it works

`fetch_papers.py` pulls the current CS paper listings from the arXiv RSS feed (`rss.arxiv.org/rss/cs`) and saves them to `papers.json`. The HTML page reads this file and displays papers in a rotating slideshow, shuffled for variety, cycling every 25 seconds.

Run `fetch_papers.py` periodically (e.g. via cron) to keep the display current. arXiv typically announces new papers on weekday mornings (US Eastern time).
