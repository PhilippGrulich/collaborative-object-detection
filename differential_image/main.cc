//
// Created by philipp on 12/24/17.
//

#include <iostream>
#include <thread>


#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/bgsegm.hpp"
#include <iostream>
#include <stdlib.h>     /* abs */

#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

inline
int blend(int input, int min) {
    return input - min < 0 ? 0 : input - min;
}

struct Cluster {
    int minX;
    int maxX;
    int minY;
    int maxY;

    Cluster(int minX, int maxX, int minY, int maxY)
            : minX(minX), minY(minY), maxX(maxX), maxY(maxY) // Create an object of type _book.
    {
    }
};

int main(int argc, char **argv) {


    //Mat fgMaskMOG2; //fg mask

    cv::Mat frame;
    std::vector<cv::Point> points;

    vector<Cluster> clusters;
    const int threshold = 100;


    std::clock_t start;
    start = std::clock();
    //update the background model

    frame = cv::imread("raw.png");
    cv::Mat diffImage = cv::imread("diff.png", 1);

    cv::Mat grayscaleMat(diffImage.size(), CV_8U);
    cv::Mat fgMaskMOG2(grayscaleMat.size(), grayscaleMat.type());
    cv::cvtColor(diffImage, grayscaleMat, cv::COLOR_BGR2GRAY);
    cv::threshold(grayscaleMat, fgMaskMOG2, 100, 255, cv::THRESH_BINARY);

    //cv::imwrite("/home/philipp/crop2/DIFF" + frameName, fgMaskMOG2);



    CV_Assert(fgMaskMOG2.isContinuous());
    int cells = fgMaskMOG2.cols * fgMaskMOG2.rows;
    int j;
    uchar *p;

    p = fgMaskMOG2.ptr<uchar>(0);
    for (j = 0; j < cells; j = j + 2) {
        //std::cout << "J: " << p[j] << std::endl;
        if (p[j]) {
            // std::cout << "J: " << j << std::endl;

            int x = j % fgMaskMOG2.cols;
            int y = j / fgMaskMOG2.cols;

            bool inNoCluster = true;
            for (auto &cluster : clusters) {

                if (blend(cluster.minX, threshold) <= x && cluster.maxX + threshold >= x &&
                    blend(cluster.minY, threshold) <= y && cluster.maxY + threshold >= y) {
                    if (cluster.maxX < x)
                        cluster.maxX = x;
                    else if (cluster.minX > x)
                        cluster.minX = x;

                    if (cluster.maxY < y)
                        cluster.maxY = y;
                    else if (cluster.minY > y)
                        cluster.minY = y;

                    inNoCluster = false;
                    break;
                }
            }
            if (inNoCluster) {

                //std::cout << "No Cluster " << point << "  " << std::endl;
                auto firstPoint = Cluster(x, x, y, y);
                clusters.push_back(firstPoint);
            }
        }


    }
    std::cout << "Time: " << (std::clock() - start) / (double) (CLOCKS_PER_SEC / 1000) << " ms" << std::endl;

    std::cout << clusters.size() << std::endl;


    for (size_t i = 0; i < clusters.size(); i++) {
        auto cluster = clusters[i];
        auto rec = Rect(cluster.minX, cluster.minY, cluster.maxX - cluster.minX, cluster.maxY - cluster.minY);
        std::cout << rec.height << " w: " << rec.width << std::endl;

        if (rec.height != 0 && rec.width != 0) {
            auto cropped = frame(rec);
            cv::imwrite("result/crop_" + std::to_string(i) + ".png", cropped);
            cv::rectangle(frame, rec, cv::Scalar(0, 255, 0));
        }
    }

    cv::imwrite("result/recFrame.png", frame);
    clusters.

            clear();

    points.

            clear();


    return 0;
}

