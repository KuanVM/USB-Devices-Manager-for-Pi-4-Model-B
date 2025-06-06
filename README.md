# EmbeddedOS USB Management Project

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Building Kernel Modules (Optional)](#building-kernel-modules-optional)
- [Running the DBus Service](#running-the-dbus-service)
- [Using the GUI](#using-the-gui)
- [Using the CLI Tools](#using-the-cli-tools)
- [Running as a Systemd Service](#running-as-a-systemd-service)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## Overview
This project provides a complete USB device management solution for embedded Linux systems (e.g., Raspberry Pi 4). It includes:
- Kernel modules for USB device detection (optional)
- A DBus service for USB management
- A Python GUI for user-friendly USB control
- CLI tools for scripting and automation
- Plugin support for device-specific actions

---

## Requirements
- **Operating System:** Linux (tested on Ubuntu, Raspberry Pi OS)
- **Python:** 3.6+
- **System Packages:**
  - `python3-gi` (PyGObject)
  - `python3-dbus` (dbus-python)
  - `udisks2`
  - `systemd` (for service management)
  - `build-essential`, `linux-headers-$(uname -r)` (for kernel modules, optional)
- **Python Packages:**
  - `pyudev`

**Install all requirements:**
```bash
sudo apt update
sudo apt install python3-gi python3-dbus udisks2 systemd build-essential linux-headers-$(uname -r) python3-pip
pip3 install pyudev
```

---

## Project Structure
```
EmbeddedOS_Project-main/
├── usb_manager_gui.py         # Python GUI
├── usb_ids.txt               # USB device database
├── usb_management/           # Core management scripts & plugins
├── others/                   # Kernel modules (optional)
├── cli/                      # CLI tools
├── systemd/                  # Systemd service files
└── README.md                 # This guide
```

---

## Setup & Installation
1. **Clone or copy the project to your Linux machine.**
2. **Install all requirements** (see above).
3. **(Optional) Edit `usb_ids.txt`** to add your own device whitelist/labels.

---

## Building Kernel Modules (Optional)
If you want to use the custom kernel modules for USB device detection:
```bash
cd others
make clean
make
```
**Load a module:**
```bash
sudo insmod usb_audio_driver.ko
sudo insmod usb_storage_driver.ko
sudo insmod usb_hid_driver.ko
sudo insmod usb_mouse_driver.ko
sudo insmod usb_video_driver.ko
```
**Check kernel log:**
```bash
dmesg | tail
```
> **Note:** Most users do not need to load these modules unless you want to experiment with custom drivers.

---

## Running the DBus Service
You can run the DBus service directly or as a systemd service.

### **A. Run Directly (for testing)**
```bash
cd usb_management
python3 dbus_service.py
```

### **B. Run as a Systemd Service (recommended for production)**
1. Edit `systemd/dbus.service` and set the correct absolute path for `ExecStart`:
   ```
   ExecStart=/usr/bin/python3 /ABSOLUTE/PATH/TO/EmbeddedOS_Project-main/usb_management/dbus_service.py
   ```
2. Copy and enable the service:
   ```bash
   sudo cp systemd/dbus.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable dbus
   sudo systemctl start dbus
   sudo systemctl status dbus
   ```

---

## Using the GUI
1. **Ensure the DBus service is running** (see above).
2. **Run the GUI:**
   ```bash
   python3 usb_manager_gui.py
   ```
3. **Features:**
   - View all connected USB devices
   - Mount/unmount devices
   - Refresh device list
   - Get error messages if DBus is not running or device actions fail

---

## Using the CLI Tools
All CLI scripts are in the `cli/` directory. Example usage:

- **List USB devices:**
  ```bash
  python3 cli/usb_list.py
  ```
- **Mount a device:**
  ```bash
  python3 cli/usb_mount.py <serial|devpath>
  ```
- **Unmount a device:**
  ```bash
  python3 cli/usb_unmount.py <serial|devpath>
  ```
- **Check device status:**
  ```bash
  python3 cli/usb_status.py <serial|devpath>
  ```

---

## Running as a Systemd Service (usb_classifier)
If you want to use the USB classifier daemon:
1. Edit `systemd/usb_classifier.service` and set the correct path for `ExecStart`:
   ```
   ExecStart=/usr/bin/python3 /ABSOLUTE/PATH/TO/EmbeddedOS_Project-main/usb_management/usb_classify.py
   ```
2. Copy and enable the service:
   ```bash
   sudo cp systemd/usb_classifier.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable usb_classifier
   sudo systemctl start usb_classifier
   sudo systemctl status usb_classifier
   ```

---

## Troubleshooting
- **Permission denied for log files:**
  - Run scripts with `sudo` or change log file path to a user-writable location.
- **DBus connection errors in GUI:**
  - Make sure the DBus service is running.
- **Module format errors:**
  - Rebuild kernel modules with the correct kernel headers for your system.
- **Device not showing up:**
  - Check `usb_ids.txt` and system logs (`dmesg`, `journalctl`).
- **GUI does not update:**
  - Click "Refresh" or restart the GUI after plugging/unplugging devices.

---

## Credits
- Project by QQP Group & contributors
