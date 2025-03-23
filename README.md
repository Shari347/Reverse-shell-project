# Python Reverse Shell with Persistence

This project is a Python-based reverse shell with multi-client support and automatic persistence. It allows an attacker machine (Mac) to remotely control one or more victim machines (Linux VMs) by executing system commands via a terminal shell.

> **Educational Use Only** — This tool is intended for ethical hacking and cybersecurity learning in controlled environments. Do not use this on any device you don't own or have explicit permission to test.

---

## Project Structure

- `client.py` – Reverse shell script run on each victim machine (Linux VM)
- `server.py` – Command & control server run on the attacker machine (Mac)

---

## Features

- Persistence via cron job (auto-connects after reboot)
- Multi-client handling (control multiple VMs)
- Remote command execution with output handling
- Hidden storage of client script (`~/.config/.sysupdate/`)
- Reconnect loop if the connection fails

---

## Requirements

- Python 3.x (installed on both Mac and Linux VMs)
- macOS machine (attacker)
- 2 or more Linux Virtual Machines (victims)
- VirtualBox or similar (with networking configured properly)

---

## ⚙️ How It Works

### `client.py` (Victim Side)
- Connects to the attacker's IP and port using a TCP socket
- Waits for commands, executes them, and sends output back
- Copies itself to a hidden folder and creates a `cron` job to run on startup

### `server.py` (Attacker Side)
- Listens for incoming connections from multiple clients
- Presents a list of connected machines to interact with
- Sends commands and displays responses in real time

---

## Setup Instructions (Full Walkthrough)

### 1. Setup Virtual Machine Network (IMPORTANT)

This is **required** for your Mac and VM(s) to see each other.

#### On VirtualBox:
1. Shut down each VM.
2. Go to **Settings > Network**.
3. Set **Adapter 1** to:
   - **Attached to:** `Bridged Adapter`
   - **Name:** usually `en0: Wi-Fi (AirPort)` if using Wi-Fi
4. Click OK and **start the VM**.

IMPORTANT: Please make sure to repeat this setup for **each VM** you want to use.

---

### 2. Find IP Addresses

#### On Mac (attacker):
```bash
ipconfig getifaddr en0
```
This is your `ATTACKER_IP` you will paste into `client.py`

#### On Each VM (victim):
```bash
ip a
```
✅ Check that the IP starts with something like `192.168.x.x` and is in the same range as your Mac

To test:
```bash
ping <mac-ip-address>
```
You should get replies ✅

---

### 📥 3. Transfer `client.py` to Each VM

#### Option A: **SCP (Secure Copy)**
On your Mac:
```bash
scp client.py username@<vm-ip>:/home/username/
```
Replace `username` and `<vm-ip>` with your VM's actual info.
You'll be prompted for your VM password.

#### Option B: **Shared Folder (Easier for many VMs)**
1. In VirtualBox: Settings > Shared Folders
2. Add a folder from your Mac (e.g. Desktop or Documents)
3. Inside the VM, access it:
```bash
sudo mount -t vboxsf SharedFolderName /mnt
cp /mnt/client.py ~/client.py
```
✅ Now you can run `client.py` inside the VM

---

### 4. Edit `client.py`
Open the script on each VM and update:
```python
ATTACKER_IP = "your-mac-ip"
```
✅ This tells the VM where to connect

Leave the rest of the code unchanged. It already includes auto-persistence.

---

### 🖥️ 5. Start the Server on Your Mac
Open Terminal and run:
```bash
python3 server.py
```
You should see:
```
[*] Listening for connections on 0.0.0.0:9999...
```
✅ This means the server is ready.

---

### 🤖 6. Run `client.py` on Each VM
In each VM terminal:
```bash
python3 client.py
```
✅ After a few seconds, your Mac should print:
```
[+] New client from 192.168.x.x
```
You’ll see all connected VMs listed with an index number.

---

### 💬 7. Use the Reverse Shell
Once clients are connected:
- You can select a client by index (e.g. `0`, `1`, `2`)
- Type shell commands like `whoami`, `ls`, `hostname`, `pwd`
- Get command output in real time
- Type `quit` to close a session and return to the menu

---

### 🔁 8. Test Persistence (Auto-Reconnect After Reboot)

1. Reboot the VM:
```bash
sudo reboot
```
2. Keep `server.py` running on your Mac
3. Wait ~10–20 seconds after boot
4. The client will **auto-connect back** due to the cron job added during the first run of `client.py`

✅ You will see:
```
[+] New client from 192.168.x.x
```
again — without needing to manually run anything on the VM

---

## Tips

- Make sure no firewall is blocking port `9999`
- Keep VM usernames consistent for easier path management
- You can test with 2–3 VMs at the same time for full multi-client control

---

## 🛡 Legal Disclaimer
This tool is for educational and authorized penetration testing only. Using it against systems without permission is illegal and unethical.

---

## License
MIT License — free to use in ethical and learning contexts.

---

## 🙋‍♂️ Author
**Sharihan Hossain**  
Aspiring Red Teamer & Cybersecurity Enthusiast  
GitHub: [github.com/Shari347](https://github.com/Shari347)

