import janome
from janome.tokenizer import Tokenizer
import os, re, json, random, sys

dict_file = "chatbot-data.json"
dic = {}
tokenizer = Tokenizer()

# 辞書に文章を登録する
def register_dic(words):
  global dic
  if len(words) == 0: return
  tmp = ["@"]
  for i in words:
    word = i.surface

    # 空文字、改行等はワードとして不適切
    if word == "" or word == "\r\n" or word == "\n": continue
    tmp.append(word)

    # 連続した単語数が３つ以下はやめてね。
    if len(tmp) < 3: continue

    # @以外の連続した３つの単語を辞書に登録
    if len(tmp) > 3: tmp = tmp[1:]
    set_word3(dic, tmp)

    if word == "。" or word == "?":
      tmp = ["@"]
      continue

  # データベースを更新
  json.dump(dic, open(dict_file, "w", encoding = "utf-8"))

# 辞書に連続した単語の出現数をカウント
def set_word3(dic, s3):
  w1, w2, w3 = s3
  if not w1 in dic: dic[w1] = {}
  if not w2 in dic[w1]: dic[w1][w2] = {}
  if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0

  dic[w1][w2][w3] += 1

# 文章を生成する
def make_sentence(head):
  if not head in dic: return ""
  ret = []
  # 先頭が'@'でなければ head からスタート
  if head != "@": ret.append(head)

  # 先頭の２単語を選ぶ
  top = dic[head]
  w1 = word_choice(top)
  w2 = word_choice(top[w1])
  # 選んだ単語を追加
  ret.append(w1)
  ret.append(w2)

  # ３つの目の単語を選びましょう
  # その単語が '。','?','' のいずれでもない間ループ
  while True:
    # 1,2番目の単語が辞書に入ってますか？
    # 入っているなら3つ目を選びましょう
    # 入っていないなら空文字にします。
    if w1 in dic and w2 in dic[w1]:
      w3 = word_choice(dic[w1][w2])
    else:
      w3 = ""
    ret.append(w3)

    if w3 == "。" or w3 == "?" or w3 == "": break

    # 先頭文字をずらします。
    w1, w2 = w2, w3
  
  # 文字列のリストを空文字で連結
  return "".join(ret)

# 辞書から単語を選びましょう。
def word_choice(sel):
  keys = sel.keys()
  return random.choice(list(keys))

# 返信する文章を作成
def make_reply(text):
  # textの最後の文字が '。','?','!'のいずれでもなければ'。'を追加
  if text[-1] != "。" or text[-1] != "？" or text[-1] != "！": text += "。"
  # 品詞ごとに分解
  words = tokenizer.tokenize(text)
  # 辞書に追加
  register_dic(words)

  # 文章の生成
  for w in words:
    word = w.surface
    ps = w.part_of_speech.split(",")[0]

    # 感動詞は 「 word + "。"」で返す。
    if ps == "感動詞":
      return word + "。"

    # 名詞か形容詞が来たら、それを開始文字として文章を生成
    if ps == "名詞" or ps == "形容詞":
      if word in dic: return make_sentence(word)

  # 何もなかったらランダムな文章にする。
  return make_sentence("@")

# データベースがあるならロードしちゃいましょう
if os.path.exists(dict_file):
  dic = json.load(open(dict_file, "r"))


