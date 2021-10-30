/**
 * @file statistic_image_pixel.cc
 * @author xiaotaw (xiaotaw@qq.com)
 * @brief 统计COCO中11万张图片的像素分布，保存为img_stat.txt
 * @version 0.1
 * @date 2021-10-24
 *
 * @copyright Copyright (c) 2021
 *
 */
#include <boost/filesystem.hpp>
#include <chrono>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <string>

std::string image_dir = "/media/xt/8T/DATASETS/COCO_2017/coco/train2017/";

void getFiles(const std::string &directory,
              std::vector<std::string> &image_files,
              std::vector<std::string> &name);

void countImagePixel(const std::vector<std::string> &image_files,
                     std::vector<std::size_t> &count);

int main() {
  std::vector<std::string> image_files, name;
  getFiles(image_dir, image_files, name);
  std::cout << "image num: " << image_files.size() << std::endl;

  std::vector<std::size_t> count(256 * 256 * 256, 0);
  countImagePixel(image_files, count);

  const std::string out_file = "img_stat.txt";
  std::ofstream ofs(out_file, std::ios::out);
  if (!ofs.is_open()) {
    std::cout << "Error to open " << out_file;
  }

  for (int i = 0; i < count.size();) {
    ofs << count[i] << ",";
    if (++i % 256 == 0) {
      ofs << std::endl;
    }
  }
  ofs.close();

  return 0;
}

void getFiles(const std::string &directory,
              std::vector<std::string> &image_files,
              std::vector<std::string> &name) {
  namespace fs = boost::filesystem;
  fs::path fullpath(directory);
  if (!fs::exists(fullpath)) {
    std::cout << "full path not exists! " << fullpath << std::endl;
  }
  fs::directory_iterator end_iter;
  for (fs::directory_iterator iter(fullpath); iter != end_iter; iter++) {
    if (fs::is_directory(*iter)) {
    } else {
      std::string file = iter->path().string();
      image_files.emplace_back(iter->path().string());
      fs::path filePath(file);
      name.emplace_back(filePath.stem().string());
    }
  }
}

void countImagePixel(const std::vector<std::string> &image_files,
                     std::vector<std::size_t> &count) {

  auto t0 = std::chrono::steady_clock::now();
  auto t1 = t0;
  for (int i = 0; i < image_files.size(); ++i) {
    if (i % 1000 == 0) {
      t1 = std::chrono::steady_clock::now();
      double dr = std::chrono::duration<double>(t1 - t0).count();
      std::cout << "process " << i << " of " << image_files.size()
                << ", passed " << dr << " seconds" << std::endl;
    }
    cv::Mat img = cv::imread(image_files[i]);
    if (img.empty()) {
      std::cout << "failed to read " << i << "th img: " << image_files[i]
                << std::endl;
    }
    for (int i = 0; i < img.rows; ++i) {
      cv::Vec3b *pixrow = img.ptr<cv::Vec3b>(i);
      for (int j = 0; j < img.cols; ++j) {
        const cv::Vec3b &pix = pixrow[j];
        count[(pix[0] * 256 + pix[1]) * 256 + pix[2]] += 1;
      }
    }
  }
}