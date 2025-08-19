import socket
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csiread
import os

# Selected subcarriers and history length
selected_subcarriers = [5, 10, 15, 20, 25, 29]
history_length = 100
subcarrier_history = {sc: [] for sc in selected_subcarriers}

# Set up plot
fig, ax = plt.subplots(figsize=(10, 6))
lines = {sc: ax.plot([], [], label=f"Subcarrier {sc}")[0] for sc in selected_subcarriers}
ax.set_xlim(0, history_length)
ax.set_ylim(0, 1)
ax.set_title("Real-Time CSI Magnitude Over Time")
ax.set_xlabel("Packet Index")
ax.set_ylabel("Magnitude")
ax.legend()
ax.grid(True)
plt.tight_layout()

# Temporary file to store CSI data
temp_csi_file = "temp_csi.dat"
buffer_lock = threading.Lock()


def start_csi_server(host='0.0.0.0', port=8090):
    # Create the file immediately so it exists
    with open(temp_csi_file, 'wb') as f:
        pass  # Just create an empty file

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening for CSI data on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    try:
        with open(temp_csi_file, 'ab') as f:  # Append mode
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                with buffer_lock:
                    f.write(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()


def update(frame):
    with buffer_lock:
        try:
            csidata = csiread.Intel(temp_csi_file, nrxnum=3, ntxnum=2, pl_size=10)
            csidata.read()
            csi = csidata.get_scaled_csi()
        except Exception as e:
            print(f"Error parsing CSI data: {e}")
            return list(lines.values())

    if len(csi) == 0:
        return list(lines.values())

    latest_packet = csi[-1]
    for sc in selected_subcarriers:
        magnitude = np.mean(np.abs(latest_packet[sc]))
        subcarrier_history[sc].append(magnitude)
        if len(subcarrier_history[sc]) > history_length:
            subcarrier_history[sc].pop(0)

    for sc in selected_subcarriers:
        lines[sc].set_data(range(len(subcarrier_history[sc])), subcarrier_history[sc])

    ax.set_xlim(0, max(len(subcarrier_history[sc]) for sc in selected_subcarriers))
    max_mag = max(max(subcarrier_history[sc]) for sc in selected_subcarriers)
    ax.set_ylim(0, max_mag * 1.2 if max_mag > 0 else 1)

    return list(lines.values())

# Start the server in a separate thread
server_thread = threading.Thread(target=start_csi_server, daemon=True)
server_thread.start()

# Start the animation
ani = FuncAnimation(fig, update, interval=200, blit=False)
plt.show()

