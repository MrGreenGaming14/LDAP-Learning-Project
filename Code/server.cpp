#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
    //above for sockets
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <filesystem>
#include <unordered_map>
#include <functional>
#include <cstdlib>
    //includes from client just in case

int main(int argc, char** argv)
{
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(1234); // Port number
    server_address.sin_addr.s_addr = INADDR_ANY;

    std::cout << "Server: binding" << std::endl;
    bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address));
    std::cout << "Server: listening" << std::endl;
    listen(server_socket, 5);

    int client_socket = accept(server_socket, NULL, NULL);

    char buffer[1024];
    std::ofstream output_file("received_file.txt", std::ios::binary);
    std::cout << "Server: entering write loop" << std::endl;
    while (int bytes_received = recv(client_socket, buffer, 1024, 0) > 0) {
        output_file.write(buffer, bytes_received);
    }

    output_file.close();
    close(client_socket);
    close(server_socket);

    return 0;
}