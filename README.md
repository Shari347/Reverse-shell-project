# 🔐 Python Reverse Shell with Persistence

This project is a simple Python-based reverse shell with multi-client support and automatic persistence. It allows an attacker machine (Mac) to remotely control victim machines (Linux VMs) by executing system commands via a terminal shell.

> **Educational Use Only** — This tool is intended for ethical hacking and cybersecurity learning in controlled environments. Do not use this on any device you don't own or have explicit permission to test.

---

## 📂 Project Structure

- `client.py` – Reverse shell script run on the victim (Linux VM)
- `server.py` – Command & control server run on the attacker machine (Mac)

---

## 🧠 Features

- 🔁 Persistent reverse shell via cron job
- 🧵 Multi-client handling with thread-based sessions
- 📡 Remote command execution with output streaming
- 👻 Hidden client storage for stealth (`~/.config/.sysupdate/`)
- 🔄 Automatic reconnect if connection is dropped

---

## 🛠 Requirements

- Python 3.x
- Mac (attacker machine)
- Linux Virtual Machine (victim machine)
- VirtualBox or similar virtualization platform

---

## ⚙️ How It Works

### `client.py` (Victim Side)
- Connects to the attacker's IP and port using TCP sockets
- Waits for system commands from the attacker
- Executes them via subprocess and sends output back
- Installs itself on first run to a hidden directory and sets a cron job for persistence

### `server.py` (Attacker Side)
- Listens for incoming connections from clients
- Maintains a list of connected clients and allows switching between them
- Sends commands and receives results from selected client

---

## 🔧 Setup Instructions

### ✅ Pre-Setup
1. Use **Bridged Adapter** networking in VirtualBox for the VM
2. Verify both Mac and VM are on the same network
3. Ensure Python 3 is installed on both systems

### 📍 Get IP Addresses
- On Mac (attacker): `ipconfig getifaddr en0`
- On VM (victim): `ip a`

### 📥 Transfer `client.py` to VM
**Option A:**
```bash
scp client.py username@<vm-ip>:/home/username/
```

**Option B:** Use shared folders via VirtualBox

### 📝 Configure `client.py`
- Edit `ATTACKER_IP` to match your Mac’s local IP

### ▶️ Run
**On your Mac (attacker):**
```bash
python3 server.py
```
**On your VM (victim):**
```bash
python3 client.py
```

You’ll see the client connect back and a shell will open for commands.

### 🔁 Test Persistence
1. Reboot your VM:
```bash
sudo reboot
```
2. Leave `server.py` running
3. After boot, the VM will auto-connect again

---

## 🛡 Legal Disclaimer
This tool is for educational and authorized penetration testing only. Using it against systems without permission is illegal and unethical.

---

## 📎 License
MIT License — free for use in ethical and learning contexts.

---

## 🙋‍♂️ Author
**Sharihan Hossain**  
Aspiring Red Teamer & Cybersecurity Enthusiast  
GitHub: [github.com/Shari347](https://github.com/Shari347)

