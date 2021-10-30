# 简介
- 统计一个图片集合中的像素，与一个集合中的汉字，根据出现频率，生成对应关系（仿照原始密码破译原理）。
- 给一张或一系列图片，按一定的大小划分成正方形，并计算块内像素平均值，代替原来的图像，形成马赛克图片
- 根据上述对应关系，将色块的像素均值”破译“成汉字，并将汉字显示在色块中。


# 统计数据
- 使用`statitic_news_word.py`
- 数据来源为THUCNews中的80万篇新闻
- 依赖re, glob,　codecs



# 统计图像像素数据库
- 使用`statistic_image_pixel`
- 数据来源为coco中11万张图像
- 依赖opencv和booost

```bash
mkdir build && cd build
cmake .. && make 
cd ..
./build/statistic_image_pixel
```

# 需创建conda环境
```bash
conda create -y -n block2charpy3 python=3
conda activate block2charpy3
conda install -y matplotlib
conda install -y opencv
conda install -y pillow
```

# 使用
- 将jpg格式的图片放入sample/origin中
- 运行脚本
```bash
conda activate block2char
python src/decoder.py
```
- 在sample/result中可以看到:
  - 马赛克图片
  - 马赛克＋字图片
  - 汉字txt文件