import feedparser
import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

DISCORD = os.environ["DISCORD_WEBHOOK"]

ARXIV_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.RO&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending"

def fetch_papers():
    feed = feedparser.parse(ARXIV_URL)

    papers = []

    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        })

    return papers


def analyze(papers):

    text = ""

    for p in papers:
        text += f"""
Title: {p['title']}
Link: {p['link']}
Abstract: {p['summary']}
"""

    prompt = f"""
你是顶级AI研究战略分析师。

从下面论文中挑选真正有技术突破的10篇。

输出格式必须是：

Top 10 跨越性技术

每篇结构：

1. 论文标题（英文）
arXiv链接

核心突破
- 中文解释

技术意义
- 中文解释

论文列表：

{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def send_discord(text):

    data = {
        "content": f"🧠 Weekly AI Breakthrough Radar\n\n{text}"
    }

    requests.post(DISCORD, json=data)


if __name__ == "__main__":

    papers = fetch_papers()

    report = analyze(papers)

    send_discord(report)
