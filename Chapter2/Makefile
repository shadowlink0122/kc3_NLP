default:
	make corpus
	make train
	make gen

corpus:sc wa data

# スクレイピング
sc:
	python3 scraping/scrape.py > corpus/raw.txt

# 分ち書き
wa:
	mecab -b 100000 -Owakati corpus/raw.txt -o corpus/wakati.txt

# 学習データに整形
data:
	python3 corpus/generate.py

# 学習
train:
	python3 train.py

# 文章の生成
gen:
	python3 generate.py
