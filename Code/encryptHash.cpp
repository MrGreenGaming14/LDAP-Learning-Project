#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <vector>

// Function to calculate the SHA-256 hash of a string
#include <openssl/sha.h>

// Function to encrypt a string using a Caesar cipher
std::string caesarCipherEncrypt(const std::string& input, int shift) {
    std::string encrypted;
    for (char c : input) {
        if (isalpha(c)) {
            char base = (islower(c)) ? 'a' : 'A';
            encrypted += static_cast<char>(((c - base + shift) % 26) + base);
        } else {
            encrypted += c;
        }
    }
    return encrypted;
}

int main() {
    unsigned char hash[SHA256_DIGEST_LENGTH]; 
    std::string user_input;
    int caesar_shift;

    std::cout << "Enter a string to hash and encrypt: ";
    std::getline(std::cin, user_input);

    // hashes the string using the SHA256 algorithm
    unsigned char* hashed_string = SHA256((unsigned char*)user_input.c_str(), user_input.length(), hash);
    
    std::cout << "Enter a Caesar cipher shift value (e.g., 3): ";
    std::cin >> caesar_shift;
    std::cin.ignore(); // Consume the newline character left in the input buffer

    // Encrypt the hashed string using a Caesar cipher
    std::string encrypted_string = caesarCipherEncrypt(reinterpret_cast<char *>(hashed_string), caesar_shift);

    std::cout << "Original Input: " << user_input << std::endl;
    std::cout << "SHA-256 Hash: " << hashed_string << std::endl;
    std::cout << "Caesar Cipher Encrypted: " << encrypted_string << std::endl;

    return 0;
}