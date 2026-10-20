"""Notifie Bing (IndexNow) des pages du site après une mise en ligne.
Usage : python3 scripts/indexnow.py
"""
import json, urllib.request, re, os
KEY = "2d209ce2ecc59ffc4aba1a536853eeaa"
HOST = "www.bertrandcharpilloz.com"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(root, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, len(urls), "URL notifiées")
