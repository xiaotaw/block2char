#coding="utf8"
#统计新闻中各个汉字的频率，并保存到文件
import re
import glob
import codecs
from collections import Counter


text_dir = "/media/xt/8T/DATASETS/nlp_data/THUCNews/THUCNews/"
text_files = glob.glob(text_dir + "*/*.txt")
print("total text　num: " + str(len(text_files)))

c = Counter()
for i, file in enumerate(text_files):
    if (i % 1000 == 0):
        print("processing %d of %d" % (i, len(text_files)))
    with codecs.open(file, encoding="utf8") as f:
        text = f.read()
        clean_text = re.sub("\W", "", text)
        c.update(clean_text)


zh_f = codecs.open("sample/zh_vocab.txt", "w", encoding="utf8")
vocab = list(c.items())
vocab.sort(key=lambda x: x[1], reverse=True)

for word, freq in vocab:
    _ = zh_f.write("%s\t%d\n" % (word, freq))

zh_f.close()
