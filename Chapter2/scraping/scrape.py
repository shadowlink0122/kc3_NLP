import sys, re, ssl
import codecs
from bs4 import BeautifulSoup
import urllib.request as req
import requests

# SSL証明書が正しくなくてもやってしまえって感じの力技
# (おすすめはできないけど仕方ない)
ssl._create_default_https_context = ssl._create_unverified_context

# ベースとなるURL
URL = "https://ja.wikipedia.org/wiki/"

# 情報収拾する先のリスト
urls = [
	u"不思議の国のアリス",
	u"ふしぎの国のアリス",
	u"鏡の国のアリス",
	u"地下の国のアリス",
]

# リクエストボディのヘッダ
headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
}

# ここからが本番
for url in urls:
	response = requests.get(url=URL+url)
	soup = BeautifulSoup(response.text.encode(response.encoding))
	source_set = soup.find_all("p")

	for a in source_set:
		a = a.text
		# a = re.match(r"[亜-熙ぁ-んァ-ヶ]", a)
		a = re.sub(r"[\s!-~]*", "", a)
		a = re.sub(r"。", "\n", a)
		sys.stdout.buffer.write(a.encode("utf-8"))
		sys.stdout.buffer.flush()

