# csi_plotting_realtime
Real-time visualization of Channel State Information (CSI) data.

# Overview
This project captures CSI data from an Intel Wi-Fi card and plots it in real time using Python.
It is useful for wireless research, signal analysis, and real-time monitoring of CSI streams.

# Prerequisites

- A router with unencrypted Wi-Fi and 5 GHz enabled.
- A PC connected to the unencrypted network.
- A second device connected to the unencrypted network.
- Intel 5300 Wi-Fi card for CSI data collection.
- Python 3.x installed.


# Steps to Plot CSI Data
### 1. Compile and Run the CSI Capture Program
Compile the provided C file:
```
gcc -o log_to_server_2 log_to_server_2.c
sudo ./log_to_server_2
```

### 2. Install Python Dependencies
Install all required libraries from requirements.txt:
```
pip install -r requirements.txt
```

### 3. Run the Real-Time Plotting Script
Execute the Python script:
```
python3 csirealtime.py
```

# Generate Wi-Fi Traffic for CSI Collection
To ensure continuous CSI data, generate traffic using iperf3:
On the PC (Server):
```
iperf3 -s -B <ip-address-of-pc>
```

On the other device in the same network (Client):
```
iperf3 -c <ip-address-of-pc> -u -b 100M -P 10 -t 180
```

Now data should be displayed.

# Attribution
The log_to_server_2.c script in this repository is adapted from the original work by Lubingxian: [Github Repo](https://github.com/lubingxian/Realtime-processing-for-csitool)
