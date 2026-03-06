import requests
import feedparser
import os

WEBHOOK = os.getenv("FEISHU_WEBHOOK")

ARXIV_URL = "http://export.arxiv.org/rss/cs.AI"

feed = feedparser.parse(ARXIV_URL)

papers = []

for entry in feed.entries[:5]:
    title = entry.title
    link = entry.link
    summary = entry.summary[:200]

    papers.append(f"【{title}】\n{summary}...\n{link}")

message = "\n\n".join(papers)

data = {
    "msg_type": "text",
    "content": {
        "text": f"🤖 本周AI论文精选\n\n{message}"
    }
}

requests.post(WEBHOOK, json=data)
