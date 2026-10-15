import xml.etree.ElementTree as ET
from collections import defaultdict
from email.utils import parsedate_to_datetime

tree = ET.parse('podcast.xml')
root = tree.getroot()
channel = root.find('channel')
items = channel.findall('item')

print(f"Total episodios en podcast.xml: {len(items)}")
dates = defaultdict(list)
for it in items:
    title = it.find('title').text
    pubDate_str = it.find('pubDate').text if it.find('pubDate') is not None else 'No pubDate'
    try:
        dt = parsedate_to_datetime(pubDate_str)
        date_key = dt.strftime('%Y-%m-%d (%a)')
    except Exception:
        date_key = pubDate_str
    dates[date_key].append(title)

for d in sorted(dates.keys()):
    eps = dates[d]
    print(f"\n=== {d} -> {len(eps)} episodios ===")
    for e in eps:
        print(f"  * {e}")
