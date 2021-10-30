import json
import codecs
import numpy as np
from collections import defaultdict

import sys
from os import path
pwd = path.split(path.realpath(__file__))[0]
p = path.split(pwd)[0]
sys.path.append(p)


from global_config import global_config


class Learner(object):
    def __init__(self):
        self.global_config = global_config
        self.load_img_stat()
        self.load_vocab()
        self.linear_map()
        self.save_map()
    #
    def load_img_stat(self):
        print("Loading img pixel stat ... ")
        stat_list = []
        stat_f = codecs.open(global_config.img_stat_file, encoding="utf8")
        for line in stat_f:
            data = [int(x) for x in line.strip().rstrip(",").split(",")]
            assert(len(data) == 256), "read data error from" + \
                global_config.img_stat_file
            data = np.array(data)
            stat_list.append(data)
        img_stat = np.vstack(stat_list)
        img_stat = np.log(1 + img_stat.reshape(-1))
        pixel_map = list(filter(lambda x: x[1] != 0, enumerate(img_stat)))
        pixel_map.sort(reverse=True)
        self.pixel_map = pixel_map
    #
    def load_vocab(self):
        print("Loading character stat ... ")
        vocab_f = codecs.open(global_config.vocab_file)
        self.word_map = []
        for line in vocab_f:
            word, freq = line.strip().split()
            self.word_map.append([word, np.log(1 + int(freq))])
    #
    def linear_map(self):
        print("Calculate linear map between img pixel and character ... ")
        self.map = defaultdict(lambda x : "<unk>")
        linear_map_factor = np.ceil(1.0 * len(self.pixel_map) / len(self.word_map))
        for i, (pixel, _) in enumerate(self.pixel_map):
            word_idx = int(i / linear_map_factor)
            word = self.word_map[word_idx][0]
            self.map[pixel] = word

    def save_map(self):
        map_file = global_config.saved_map
        print("Save learned linear map into %s ... " % map_file)
        with codecs.open(map_file, "w", encoding="utf8") as f:
            json.dump(self.map, f)

if __name__ == "__main__":
    learner = Learner()