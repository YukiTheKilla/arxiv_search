import requests
import xml.etree.ElementTree as ET
import json
import os
import time
import urllib.parse

def get_arxiv_articles(query, batch_size=100, max_total=1000):
    start = 0
    all_entries = []
    while True:
        url = f"https://export.arxiv.org/api/query?search_query={query}&start={start}&max_results={batch_size}"
        r = requests.get(url)
        root = ET.fromstring(r.text)
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        entries = []
        for e in root.findall('a:entry', ns):
            entries.append({
                "id": e.findtext('a:id', default='', namespaces=ns),
                "title": e.findtext('a:title', default='', namespaces=ns).strip(),
                "summary": e.findtext('a:summary', default='', namespaces=ns).strip(),
                "published": e.findtext('a:published', default='', namespaces=ns),
                "updated": e.findtext('a:updated', default='', namespaces=ns),
                "authors": [a.findtext('a:name', default='', namespaces=ns) for a in e.findall('a:author', ns)]
            })
        if not entries:
            break
        all_entries.extend(entries)
        start += batch_size
        print(f"Saved {len(all_entries[:max_total])} entries")
        if len(all_entries) >= max_total:
            break
        time.sleep(3)
    return all_entries[:max_total]

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    queries = [
        "id:1706.03762"
    ]
    combined_entries = {}
    for q in queries:
        results = get_arxiv_articles(q, batch_size=760, max_total=4000)
        for r in results:
            combined_entries[r["id"]] = r
    with open("data/arxiv_attention_is_all_you_need.json", "w", encoding="utf-8") as f:
        json.dump(list(combined_entries.values()), f, ensure_ascii=False, indent=2)
    print(f"Saved {len(combined_entries)} unique entries")

    os.makedirs("data", exist_ok=True)
    queries = [
        "all:transformer AND all:attention"
    ]
    combined_entries = {}
    for q in queries:
        results = get_arxiv_articles(q, batch_size=760, max_total=4000)
        for r in results:
            combined_entries[r["id"]] = r
    with open("data/arxiv_attention_is_all_you_need_data.json", "w", encoding="utf-8") as f:
        json.dump(list(combined_entries.values()), f, ensure_ascii=False, indent=2)
    print(f"Saved {len(combined_entries)} unique entries")
