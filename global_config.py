#coding=utf-8
import os

class GlobalConfig(object):
    def __init__(self):
        self.src_dir = os.path.split(os.path.realpath(__file__))[0]
        self.assets_dir = os.path.join(self.src_dir, "assets")
        self.img_stat_file = os.path.join(self.assets_dir, "img_stat.txt")
        self.vocab_file = os.path.join(self.assets_dir, "zh_vocab.txt")
        self.saved_map = os.path.join(self.assets_dir, "learned_map.json")
        # 字体文件
        self.font_file = os.path.join(self.assets_dir, "bsmi00lp.ttf")

global_config = GlobalConfig()

# the number of pixel in each color block, it was set between 59 and 69
global_config.pixel_per_block = 66
