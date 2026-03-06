import requests
import feedparser
import os

WEBHOOK = os.environ["FEISHU_WEBHOOK"]

feed = feedparser.parse("https://arxiv.org/rss/cs.AI")

papers = feed.entries[:5]

text = "🚀 本周AI论文精选\n\n"

for p in papers:
    text += f"📄 {p.title}\n"
    text += f"{p.link}\n\n"

data = {
    "msg_type": "text",
    "content": {
        "text": text
    }
}

requests.post(WEBHOOK, json=data)
