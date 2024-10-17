#include <faasm/faasm.h>
#include <faasm/input.h>

// TFLite header files
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/optional_debug_tools.h"

// Helper header files
/*
#include "get_top_n.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize2.h"
*/

#define INPUT_FILE_PATH "faasm://tflite/sample_model.tflite"
#define INPUT_IMAGE_PATH "faasm://tflite/bus_photo.jpg"
#define TFLITE_MINIMAL_CHECK(x)                                                \
    if (!(x)) {                                                                \
        fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__);               \
        exit(1);                                                               \
    }

#include <iostream>

std::unique_ptr<tflite::Interpreter> LoadModel(const std::string& modelPath) {
    // Load model from file
    std::unique_ptr<tflite::FlatBufferModel> model =
      tflite::FlatBufferModel::BuildFromFile(modelPath.c_str());
    TFLITE_MINIMAL_CHECK(model != nullptr);

    // Build the interpreter with the InterpreterBuilder.
    tflite::ops::builtin::BuiltinOpResolver resolver;
    tflite::InterpreterBuilder builder(*model, resolver);
    std::unique_ptr<tflite::Interpreter> interpreter;
    builder(&interpreter);
    TFLITE_MINIMAL_CHECK(interpreter != nullptr);

    // Allocate tensor buffers.
    TFLITE_MINIMAL_CHECK(interpreter->AllocateTensors() == kTfLiteOk);

    return interpreter;
}

/*
void PreprocessImage(const std::string& image_path, std::vector<uint8_t>& out_data, int target_width, int target_height) {
    int width, height, channels;
    uint8_t* image_data = stbi_load(image_path.c_str(), &width, &height, &channels, 3);
    if (!image_data) {
        std::cerr << "Failed to load image" << std::endl;
        return;
    }

    std::vector<uint8_t> resized_image(target_width * target_height * 3);
    stbir_resize_uint8_linear(image_data, width, height, 0, resized_image.data(), target_width, target_height, 0, (stbir_pixel_layout)3);

    stbi_image_free(image_data);

    out_data = std::move(resized_image);
}

void NormalizeAndFlatten(const std::vector<uint8_t>& image_data, std::vector<float>& normalized_data) {
    normalized_data.reserve(image_data.size());
    for (auto pixel : image_data) {
        normalized_data.push_back(pixel / 255.0f);
    }
}

void DetectObjects(tflite::Interpreter* interpreter, const std::vector<float>& input_data) {
    float* input = interpreter->typed_input_tensor<float>(0);
    std::copy(input_data.begin(), input_data.end(), input);

    std::cout << "Invoking interpreter in a loop" << std::endl;
    for (int i = 0; i < 10; i++) {
        std::cout << "Invocation " << i + 1 << "/10..." << std::endl;
        if (interpreter->Invoke() != kTfLiteOk) {
            std::cerr << "Failed to invoke interpreter" << std::endl;
            return;
        }
    }

    std::cout << "Finished invoking interpreter!" << std::endl;
    auto outputs = interpreter->outputs();
    if (outputs.size() == 0) {
        std::cerr << "Empty result from interpreter!" << std::endl;
        return;
    }

    int output = outputs[0];
    TfLiteIntArray *output_dims = interpreter->tensor(output)->dims;

    // assume output dims to be something like (1, 1, ... ,size)

    const float threshold = 0.001f;
    std::vector<std::pair<float, int>> top_results;
    auto output_size = output_dims->data[output_dims->size - 1];

    tflite::label_image::get_top_n<float>(
            interpreter->typed_output_tensor<float>(0),
            output_size,
            5,
            threshold,
            &top_results,
            true
    );


    if (top_results.empty()) {
        std::cerr << "No top results found!" << std::endl;
        return;
    } else {
        std::cout << "Found " << top_results.size() << " top results!" << std::endl;
    }
}
*/

int main(int argc, char** argv)
{
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <model_path> <image_path>" << std::endl;
        return 1;
    }

    auto interpreter = LoadModel(argv[1]);
    printf("=== Pre-invoke Interpreter State ===\n");
    // tflite::PrintInterpreterState(interpreter.get());

    /* Uncomment to print the image size for PreprocessImage
    const TfLiteTensor* input_tensor = interpreter->input_tensor(0);
    int input_height = input_tensor->dims->data[1];
    int input_width = input_tensor->dims->data[2];
    int input_channels = input_tensor->dims->data[3];
    std::cout << "Input size: " << input_height << "x" << input_width << "x" << input_channels << std::endl;
    */

    /*
    std::vector<uint8_t> image_data;
    PreprocessImage(argv[2], image_data, 224, 224);  // Adjust to match the model input size

    std::vector<float> normalized_data;
    NormalizeAndFlatten(image_data, normalized_data);

    DetectObjects(interpreter.get(), normalized_data);
    */


    return 0;
}
