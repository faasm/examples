#include <tless_abe.h>
#include <iostream>
#include <string>

int main()
{
    // Create temporary encryption context for this test
    auto& ctx = tless::abe::CpAbeContextWrapper::get(tless::abe::ContextFetchMode::Create);

    // Prepare encryption
    std::string plainText = "dance like no one's watching, encrypt like everyone is!";
    std::string policy = "\"A\" and \"B\"";
    auto cipherText = ctx.cpAbeEncrypt(policy, plainText);

    // Prepare decryption
    std::vector<std::string> attributes = {"A", "B"};
    auto actualPlainText = ctx.cpAbeDecrypt(attributes, cipherText);

    // Compare
    std::string actualPlainTextStr;
    actualPlainTextStr.assign(reinterpret_cast<char*>(actualPlainText.data()), actualPlainText.size());
    if (plainText != actualPlainTextStr) {
        std::cerr << "Encryption/decryption test failed!" << std::endl;
        return -1;
    }

    std::cout << "Encryption worked!" << std::endl;
    return 0;
}
