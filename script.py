import requests
import feedparser
import os

WEBHOOK = os.environ.get("FEISHU_WEBHOOK")

feed = feedparser.parse("https://export.arxiv.org/rss/cs.AI")

papers = []

for entry in feed.entries[:5]:
    title = entry.title
    link = entry.link
    papers.append(f"- {title}\n{link}")

text = "📚 本周 AI 新论文\n\n" + "\n\n".join(papers)

data = {
    "msg_type": "text",
    "content": {
        "text": text
    }
}

requests.post(WEBHOOK, json=data)
