import requests
import feedparser
import os

FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK")

ARXIV_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.RO+OR+cat:cs.DC&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending"

feed = feedparser.parse(ARXIV_URL)

papers = []

for entry in feed.entries[:20]:
    papers.append({
        "title": entry.title,
        "summary": entry.summary[:200],
        "link": entry.link
    })

def generate_report(papers):

    report = "🧠 Weekly AI Breakthrough Radar\n\n"
    report += "Top 10 跨越性技术\n\n"

    for i,p in enumerate(papers[:10]):

        report += f"{i+1}. {p['title']}\n"
        report += f"📎 {p['link']}\n"
        report += f"{p['summary']}\n\n"

    report += "📊 本周AI趋势\n"
    report += "- GPU 调度系统\n"
    report += "- Agent系统\n"
    report += "- 机器人学习\n"
    report += "- 高效训练\n"

    return report


report = generate_report(papers)

requests.post(
    FEISHU_WEBHOOK,
    json={
        "msg_type": "text",
        "content": {"text": report}
    }
)
