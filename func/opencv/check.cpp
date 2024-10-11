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
#include <iostream>

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: <image_name_in.bmp> <image_name_out.bmp>" << std::endl;
        return 1;
    }

    // Load an image
    cv::Mat img = cv::imread(argv[1], cv::IMREAD_COLOR);
    if (img.empty()) {
        std::cerr << "Error: Could not load image!" << std::endl;
        return -1;
    }

    // Convert the image to grayscale
    cv::Mat gray;
    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);

    // Save the grayscale image
    cv::imwrite(argv[2], gray);
    std::cout << "Image has been converted to grayscale and saved as " << argv[2] << std::endl;

    return 0;
}
