// Even when threading is completely disabled, OpenCV assumes the C++ library
// has been built with threading support, and typedefs (no-ops) these two
// symbols. To prevent an undefined symbol error, we define them here.
namespace std {
    class recursive_mutex {
    public:
        void lock() {}
        bool try_lock() { return true; }
        void unlock() {}
    };

    template <typename T>
    class lock_guard {
    public:
        explicit lock_guard(T&) {}
    };
}

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/ml.hpp>
#include <iostream>
#include <filesystem>

void loadImages(const std::string& folder, std::vector<cv::Mat>& data, std::vector<int>& labels) {
    int label = 0;
    for (const auto& entry : std::filesystem::directory_iterator(folder)) {
        if (entry.is_regular_file()) {

            std::cout << "Loading image: " << entry.path().string() << std::endl;
            cv::Mat img = cv::imread(entry.path().string(), cv::IMREAD_GRAYSCALE);
            if (!img.empty()) {
                cv::resize(img, img, cv::Size(64, 64));
                data.push_back(img.reshape(1, 1));
                labels.push_back(label);
            }
        }

        label++;
    }
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: <image_path>" << std::endl;
        return 1;
    }

    // Load images
    std::vector<cv::Mat> images;
    std::vector<int> labels;
    loadImages(argv[1], images, labels);

    // Convert data to a single matrix
    cv::Mat data;
    cv::vconcat(images, data);
    data.convertTo(data, CV_32F);

    // Perform PCA with 10 principal components
    cv::PCA pca(data, cv::Mat(), cv::PCA::DATA_AS_ROW, 10);
    cv::Mat pcaResult;
    pca.project(data, pcaResult);
    std::cout << "PCA on images succeded!" << std::endl;

    // Prepare labels for training
    cv::Mat labelsMat(labels);
    labelsMat.convertTo(labelsMat, CV_32S);

    // Train k-NN classifier with PCA result
    cv::Ptr<cv::ml::KNearest> knn = cv::ml::KNearest::create();
    knn->setDefaultK(3);
    knn->train(pcaResult, cv::ml::ROW_SAMPLE, labelsMat);
    std::cout << "Training k-NN classifier succeeded!" << std::endl;

    // Perform a prediction on the first sample as an example
    cv::Mat sample = pcaResult.row(0);
    cv::Mat response;
    knn->findNearest(sample, knn->getDefaultK(), response);
    std::cout << "Predicted label: " << response.at<float>(0, 0) << std::endl;

    return 0;
}
