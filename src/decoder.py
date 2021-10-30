# coding=utf-8
import cv2
import glob
import json
import codecs
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw

import sys
from os import path
pwd = path.split(path.realpath(__file__))[0]
p = path.split(pwd)[0]
sys.path.append(p)


from global_config import global_config

class Decoder(object):
    def __init__(self):
        print("Init Decoder ... ")
        self.global_config = global_config
        self.map = defaultdict(lambda : "<unk>")
        with codecs.open(global_config.saved_map, encoding="utf8") as f:
            map = json.load(f)
            for k, v in map.items():
                self.map[int(k)] = v.strip()
    #
    def decode(self, img_path):
        # read image
        img = cv2.imread(img_path)
        if img is None:
            print("ERROR to read image from " + img_path)
            return
        else:
            print("Succeed to read image from " + img_path)
        # mosaic
        ppr = global_config.pixel_per_block
        ppc = global_config.pixel_per_block
        # mark
        rows, cols, channels = img.shape
        b_rows = rows // ppr
        b_cols = cols // ppc
        #
        chars = []
        mosaic = np.zeros([b_rows, b_cols, 3])
        for i in range(b_rows):
            chars_tmp = []
            for j in range(b_cols):
                data = img[i*ppr: (i+1)*ppr, j*ppc: (j+1)*ppc, :]
                ave = np.round(data.mean(axis=0).mean(axis=0)).astype(int)
                mosaic[i][j] = ave
                char = self.map[(ave[0] * 256 + ave[1]) * 256 + 256]
                chars_tmp.append(char)
            chars.append(chars_tmp)
        return mosaic.astype(np.uint8), chars

if __name__ == "__main__":
    decoder = Decoder()

    for img_path in glob.glob("sample/origin/*.jpg"):
        print("Decode " + img_path + " ... ")
        mosaic_path = img_path.replace("origin/", "result/mosaic_")
        mosaic_char_path = img_path.replace("origin/", "result/mosaic_char_")
        char_path = img_path.replace("origin/", "result/char_").replace(".jpg", ".txt")

        #img_path = "sample/origin/1916333840.jpg"
        mosaic, chars = decoder.decode(img_path)

        s = "\r\n".join(["".join(x) for x in chars])
        with codecs.open(char_path, "w", encoding="utf8") as f:
            f.write(s)

        BLK_SIZE = global_config.pixel_per_block
        new_size = (mosaic.shape[0] * BLK_SIZE, mosaic.shape[1] * BLK_SIZE, 3)
        new_mosaic = np.zeros(new_size, dtype=np.uint8)
        for i in range(new_size[0]):
            for j in range(new_size[1]):
                new_mosaic[i][j] = mosaic[i // BLK_SIZE][j // BLK_SIZE]

        # img_s = Image.fromarray(mosaic[:, :, ::-1])
        # img_s.show()

        img_bg = Image.fromarray(new_mosaic[:, :, ::-1])
        img_bg.save(mosaic_path)
        # img_bg.show()
        draw = ImageDraw.Draw(img_bg)

        # 加载字体
        ttfont = ImageFont.truetype(global_config.font_file, BLK_SIZE)

        for i, char_line in enumerate(chars):
            text = "".join(char_line)
            draw.text((0, i*BLK_SIZE), text, font=ttfont)

        img_bg.save(mosaic_char_path)
        # img_bg.show()