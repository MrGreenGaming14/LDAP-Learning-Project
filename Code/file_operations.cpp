#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <filesystem>
#include <unordered_map>
#include <functional>
#include <cstdlib>

//voids will return ints for "error codes" 0 for passing and -1 for failing
int create_file(std::string const& filename);
int parse_input(std::string& command, std::string& param);
int execute_command(std::string& command, std::string& param, 
    std::unordered_map<std::string, std::function<int(std::string)>>& commands);
int delete_file(std::string const& filename);

int main(int argc, char** argv)
{
    bool run = true;
    std::string command;
    std::string param;
        //maps commands to functions
    std::unordered_map<std::string, std::function<int(std::string)>> commands = {
        {"create_file", &create_file},
        {"delete_file", &delete_file},
        {"help", [param](std::string/*useless param for syntax reasons*/){
            std::cout << "Usage:  -[command] "
            << "[parameter, if applicable] " << std::endl
            << "\t-Type \"quit\" to quit." << std::endl
            << "\t-create_file [filename.extension]" << std::endl
            << "\t-delete_file [filename.extension]" << std::endl;

            return 0;
        }}
        //{"stop", &stop},
        //{"restart", &restart}
    };
    std::cout << "Welcome to \"Group G's File Sharing Emporium!! "
        << "(name subject to change.)\" " 
        << "Type \"help\" for a list of commands." << std::endl;
    
        //program loop
    while(run)
    {
        parse_input(command, param);
        if(command == "quit")
        {
            run = false;
            break;
        }
        //executes command
        execute_command(command, param, commands);
    }
    
    return 0;
}

    //pconst & pass by reference
int create_file(std::string const& filename)
{
     // Create an ofstream object
    std::ofstream outFile("../Files/" + filename);

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

int parse_input(std::string& command, std::string& param)
{
        //gets whole input
    std::getline(std::cin, command);
        //gets the command and param
    std::istringstream iss(command);
        //gets the command like cin
    iss >> command;
        //puts param in param
    param = iss.str().substr(command.size());
    if (!param.empty() && param[0] == ' ') {
        param.erase(0, 1); // Remove the leading space
    }

    return 0;
}

int execute_command(std::string& command, std::string& param, 
    std::unordered_map<std::string, std::function<int(std::string)>>& commands)
{
    auto it = commands.find(command);
    if (it != commands.end()) {
        //call the function associated with the command
        int result = it->second(param);
        if (result == 0) {
            std::cout << "Command executed successfully." << std::endl;
        } else {
            std::cout << "Command failed." << std::endl;
        }
    } else {
        std::cout << "Unknown command or input format." << std::endl;
    }

    return 0;
}

    //-1 if file does not exist, -2 for other unknown error
int delete_file(std::string const& filename)
{
    try {
        // Check if the file exists before attempting to delete it
        if (std::filesystem::exists("../Files/" + filename)) {
            // Delete the file
            std::filesystem::remove("../Files/" + filename);
            //std::cout << "File deleted successfully." << std::endl;
        } else {
            //std::cout << "File does not exist." << std::endl;
            return -1;
        }
    } catch (const std::filesystem::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -2;
    }
    
    return 0;
}