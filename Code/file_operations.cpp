#include <iostream>
#include <string>
#include <fstream>
//voids will return ints for "error codes" 0 for passing and -1 for failing
int create_file(std::string const& filename);

int main(int argc, char** argv)
{
    create_file("test.txt");
    
    return 0;
}

    //pconst & pass by reference
int create_file(std::string const& filename)
{
     // Create an ofstream object
    std::ofstream outFile(filename);

    // Check if the file was created successfully
    if (!outFile) {
        std::cerr << "Error: file could not be created." << std::endl;
        return -1;
    }

    // Write some text to the file
    outFile << "Hello, world!" << std::endl;

    // Close the file
    outFile.close();

    return 0;
}