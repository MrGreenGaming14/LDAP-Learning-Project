#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <filesystem>
#include <unordered_map>
#include <functional>

//voids will return ints for "error codes" 0 for passing and -1 for failing
int create_file(std::string const& filename);
int parse_input(std::string const& command, std::string const& param);

int main(int argc, char** argv)
{
    bool run = true;
    std::string command;
    std::string param;
        //maps commands to functions
    std::unordered_map<std::string, std::function<int(std::string)>> commands = {
        {"create_file", &create_file},
        {"help", [param](std::string/*useless param for syntax reasons*/){
            std::cout << "Usage: [command] "
            << "[parameter, if applicable] " << std::endl;
            return 0;
        }}
        //{"stop", &stop},
        //{"restart", &restart}
    };
    std::cout << "Welcome to \"Group G's File Sharing Emporium!! "
        << "(name subject to change.)\" " 
        << "Type \"help\" for a list of commands." << std::endl;
    
    while(run)
    {
        command.erase(); param.erase(); //clear commands
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
        if(command == "quit")
        {
            run = false;
            break;
        }
        //executes command
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