# 统计图片像素与汉字的频率分布，并作图分析
import codecs
import numpy as np
from matplotlib import pyplot as plt

# 读取图片像素的频率数据
stat_list = []
stat_f = codecs.open("assets/img_stat.txt", encoding="utf8")
for line in stat_f:
  data = [int(x) for x in line.strip().rstrip(",").split(",")]
  assert(len(data) == 256), "read data error from　assets/img_stat.txt"
  data = np.array(data)
  stat_list.append(data)


img_stat = np.vstack(stat_list).reshape(-1)

pixel_log_freq = np.log(1 + img_stat)
pixel_log_freq = sorted(pixel_log_freq, reverse=True)
pixel_log_freq = filter(lambda x : x>0, pixel_log_freq)


#　读取汉字的频率数据
vocab_f = codecs.open("assets/zh_vocab.txt")
word_freq = []
for line in vocab_f:
    word, freq = line.strip().split()
    word_freq.append([word, int(freq)])


w_freq = [np.log(1 + x[1]) for x in word_freq]

#　作图分析
plt.subplot(211)
plt.plot(pixel_log_freq)
plt.subplot(212)
plt.plot(w_freq)
plt.savefig("assets/pixel_char_freq.png")
plt.show()